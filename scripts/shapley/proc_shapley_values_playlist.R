library(tidyverse)

recommendations <- read_csv("processed_data/recommendations/recommendations_playlist.csv")
shapley_values <- read_csv("processed_data/shapley/shapley_values_playlist.csv")
data <- read_csv("data/spotify_mpd/data.csv")

recommendations <- recommendations %>%
  separate_wider_delim(
    title,
    delim = " - by ",
    names = c("title", "artist"),
    too_few = "align_start",
    names_sep = "_"
  ) %>%
  mutate(artist = ifelse(is.na(title_artist), artist, title_artist)) %>%
  select(everything(), title = title_title, -title_artist)

data <- data %>%
  unite(track_name, artist_name, col = "song", sep = " - by ") %>%
  mutate(tid = as.character(glue::glue_col("song_{tid+1}"))) %>%
  pivot_wider(id_cols = c(pid, playlist_name), names_from = tid, values_from = song) %>%
  pivot_longer(cols = c(-pid), names_to = "variable", values_to = "variable_value")

shapley_values <- shapley_values %>%
  separate_wider_delim(
    recommendation,
    delim = " - by ",
    names = c("title", "artist"),
    too_many = "drop",
    cols_remove = F
  ) %>%
  mutate(title = trimws(title), artist = trimws(artist)) %>%
  left_join(
    recommendations %>% select(pid, model, title, artist, positive, explanation),
    by = c("pid", "model", "title", "artist")
  ) %>%
  left_join(data, by = c("pid", "variable"))

shapley_values %>%
  write_csv("processed_data/shapley/shapley_values_playlist.csv")

