library(tidyverse)
library(reticulate)

# Reading the data
shapley_values <- read_csv("processed_data/shapley/proc_shapley_values_books.csv")
gpt_rankings <- read_csv("processed_data/ranking_explanations/ranking_from_explanations_books.csv")

# F1-Score

shapley_values_f1 <- shapley_values %>%
  mutate(across(c(
    title, author, explanation, variable_value
  ), tolower)) %>%
  mutate(across(
    c(title, author, explanation, variable_value),
    \(x) gsub("\\.|'|!|\\*", "", x)
  )) %>%
  mutate(across(
    c(title, author, explanation, variable_value),
    \(x) gsub("&", "and", x)
  )) %>%
  mutate(across(
    c(title, author, explanation, variable_value),
    \(x) gsub("\\$", "s", x)
  )) %>%
  mutate(across(c(title, author, variable_value), \(x) gsub("\\(.*\\)", "", x))) %>%
  mutate(across(
    c(title, author, explanation, variable_value),
    \(x) gsub("\\(|\\)", "", x)
  ))

f1_score_per_recommendation <- shapley_values_f1 %>%
  separate_wider_delim(
    cols = variable_value,
    delim = " - by ",
    names = c("variable_title", "variable_author"),
    too_few = "align_start"
  ) %>%
  mutate(
    start_position_title = str_locate(explanation, variable_title)[, 1],
    start_position_author = str_locate(explanation, variable_author)[, 1],
    citation = coalesce(start_position_title, start_position_author)
  ) %>%
  mutate(
    cited = !is.na(citation),
    relevant = value > 0,
    cited_relevant = cited & relevant
  ) %>%
  group_by(model, uid, recommendation, positive, explanation) %>%
  summarise(
    cited = sum(cited),
    relevant = sum(relevant),
    cited_relevant = sum(cited_relevant),
    .groups = "drop"
  ) %>%
  mutate(
    recall = coalesce(cited_relevant / relevant, 0),
    precision = coalesce(cited_relevant / cited, 0),
    f1 = 2 * recall * precision / (recall + precision)
  ) %>%
  select(model, uid, recommendation, positive, recall, precision, f1)

# Weighted Coverage@3

gpt_rankings <- gpt_rankings %>%
  mutate(ranking = lapply(ranking, py_eval)) %>%
  unnest_longer(c(ranking)) %>%
  unnest_wider(c(ranking)) %>%
  group_by(uid, model, recommendation) %>%
  mutate(rank = row_number())

shapley_rankings <- shapley_values %>% select(model,
                                              uid,
                                              recommendation,
                                              variable,
                                              variable_value,
                                              value,
                                              positive)
shapley_rankings <- shapley_rankings %>%
  arrange(model, uid, recommendation, -value) %>%
  group_by(uid, model, recommendation) %>%
  mutate(rank = row_number())

wcoverage3_score_per_recommendation <- gpt_rankings %>%
  select(name, model, uid, recommendation, gpt_r = rank) %>%
  left_join(
    shapley_rankings %>%
      select(
        name = variable,
        model,
        uid,
        recommendation,
        positive,
        shap_r = rank,
        shap_v = value
      ),
    by = join_by(name, model, uid, recommendation)
  ) %>%
  ungroup() %>%
  filter(gpt_r <= 3) %>%
  group_by(model, uid, recommendation) %>%
  summarise(wcoverage = sum(shap_v * 1 / gpt_r), .groups = "drop")

metrics <- left_join(
  f1_score_per_recommendation,
  wcoverage3_score_per_recommendation,
  by = join_by(uid, model, recommendation)
) %>% write_csv("processed_data/metrics/metrics_book.csv")
