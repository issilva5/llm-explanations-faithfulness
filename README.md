# Faithfulness in Black-Box LLM-based Recommender Systems' Explanations

This repositories holds the code used in the experiments of Chapter 5 of my master thesis.

# Setting the environment

## Python

The code was written in [Python 3.12](https://www.python.org/downloads/release/python-3120/), there's no guarantees it will run in previous or future versions.

## R

The analysis scripts were written in [R 4.4.2](https://cran.r-project.org), there's no guarantees it will run in previous or future versions.

## Installing the required libraries

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```R
install.packages("tidyverse")
install.packages("reticulate")
install.packages("kableExtra")
```

## .env

In order to run the code, you will need to create a `.env` file, following this example:

```sh
OPENAI_KEY=sk- # Key to OpenAI API (openai.com)
GROQ_KEY=gsk_ # Key to GroqAI API (groqai.com)
```

# Directories

## The `data` directory

This directory holds the input data for all three domains - books (dir. `bookrec`), movies (dir. `movies`), and playlists (dir. `spotify_mpd`) - inside the respective subdirectory. The data is stored in a file called `data.csv`, in each subdirectory.

Each subdirectory also holds a `recommendations.zip` file, this file contain all the recommendations obtained for all models and coalitions.

## The `src` directory

This directory holds the structuring code for all the process: getting recommendations, calculating shapley values, and getting the rankings from the explanations.

## The `scripts` directory

This directory holds a series of subdirectories containing the scripts to run each step of the experiment:

- `recommendation` holds the scripts that will get the recommendations for all possible coalitions from the input data.
- `explanation` holds the scripts that will get the explanations for the full-coalition recommendations.
- `shapley` holds the scripts that compute the shapley values for each recommendation. Its outputs are in the `shapley` subdirectory of `processed_data`.
- `ranking_explanations` holds the scripts that output the rankings of the input features according to the embedded importance in the explanation. Its outputs are in the `ranking_explanations` subdirectory of `processed_data`.
- `metrics` holds the scripts to compute our evaluations metrics *recall*, *precision*, *f1* and *weighted coverage at top-K*. It also holds the scripts to produce Table 5.2 and Figure 5.1. Its outputs are in the `metrics` subdirectory of `processed_data`.
- `utils` hold a script that will read the recommendations saved a json and convert it to a CSV format. Its outputs are in the `recommendations` subdirectory of `processed_data`.

## The `processed_data` directory

It stores the outputs of the above detailed scripts.

# Running the scripts

Some scripts require to run in the root directory of this repository, thus if it fails to run, try moving it to the root dir. In case of doubt contact me at [itallo@copin.ufcg.edu.br](mailto:itallo@copin.ufcg.edu.br).