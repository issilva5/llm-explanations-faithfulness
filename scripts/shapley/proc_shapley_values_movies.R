library(tidyverse)

recommendations <- read_csv("processed_data/recommendations/recommendations_movies.csv")
shapley_values <- read_csv("processed_data/shapley/shapley_values_movies.csv")
data <- read_csv("data/movies/data.csv")

data <- data %>%
  select(prolificPID, movie = movieTitle, liked) %>%
  pivot_wider(id_cols = c(prolificPID), names_from = liked, values_from = movie, values_fn = list) %>%
  unnest_wider(col = "FALSE", names_repair = "unique", names_sep = "_") %>%
  unnest_wider(col = "TRUE", names_repair = "unique", names_sep = "_") %>%
  rename(disliked_movie_1 = FALSE_1, disliked_movie_2 = FALSE_2, disliked_movie_3 = FALSE_3,
         liked_movie_1 = TRUE_1, liked_movie_2 = TRUE_2, liked_movie_3 = TRUE_3) %>%
  pivot_longer(cols = c(-prolificPID), names_to = "variable", values_to = "variable_value")

shapley_values <- 
  shapley_values %>%
  mutate(title = trimws(recommendation)) %>%
  left_join(
    recommendations %>% select(uid, model, title, positive, explanation),
    by = c("uid", "model", "title")
  ) %>%
  left_join(data %>% select(uid = prolificPID, everything()), by = c("uid", "variable"))

shapley_values %>%
  write_csv("processed_data/shapley/proc_shapley_values_movies.csv")

