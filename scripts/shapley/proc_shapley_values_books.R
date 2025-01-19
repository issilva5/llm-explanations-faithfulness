library(tidyverse)

recommendations <- read_csv("processed_data/recommendations/recommendations_books.csv")
shapley_values <- read_csv("processed_data/shapley/shapley_values_books.csv")
data <- read_csv("data/bookrec/data.csv")

data <- data %>%
  select(user_id, book_title, book_author, liked) %>%
  unite(book_title, book_author, col = "book", sep = " - by ") %>%
  pivot_wider(id_cols = c(user_id), names_from = liked, values_from = book, values_fn = list) %>%
  unnest_wider(col = "FALSE", names_repair = "unique", names_sep = "_") %>%
  unnest_wider(col = "TRUE", names_repair = "unique", names_sep = "_") %>%
  rename(disliked_book_1 = FALSE_1, disliked_book_2 = FALSE_2, disliked_book_3 = FALSE_3,
         liked_book_1 = TRUE_1, liked_book_2 = TRUE_2, liked_book_3 = TRUE_3) %>%
  pivot_longer(cols = c(-user_id), names_to = "variable", values_to = "variable_value")

shapley_values <- 
  shapley_values %>%
  separate_wider_delim(
    recommendation,
    delim = " - by ",
    names = c("title", "author"),
    too_many = "drop",
    cols_remove = F
  ) %>%
  mutate(title = trimws(title), author = trimws(author)) %>%
  left_join(
    recommendations %>% select(uid, model, title, author, positive, explanation),
    by = c("uid", "model", "title", "author")
  ) %>%
  left_join(data %>% select(uid = user_id, everything()), by = c("uid", "variable"))

shapley_values %>%
  write_csv("processed_data/shapley/proc_shapley_values_books.csv")
