# Netflix Data Analysis

Exploratory Data Analysis of Netflix Movies and TV Shows using Python, Pandas and Matplotlib.

## Project overview

This project analyzes Netflix's movie and TV show listings, cleans missing text values for analysis, summarizes content trends, and generates nine visualizations.

## Analysis sections

The script contains these 11 numbered analysis sections:

1. **Load dataset** — reads the CSV, previews records, and reports its dimensions and columns.
2. **Data cleaning** — fills missing values in selected text and metadata columns with `Unknown`, then reports missing values, duplicates, and the final shape. Duplicate rows are reported, not removed.
3. **Movies vs. TV shows** — compares the number of titles by content type.
4. **Year-wise content analysis** — charts release counts from 2000 onward.
5. **Top 10 countries** — ranks countries by listed title count.
6. **Country-wise movies vs. TV shows** — compares both content types across the 10 countries with the most listings.
7. **Top 10 genres** — ranks genres from the `listed_in` field.
8. **Movie duration analysis** — summarizes and plots movie durations in minutes.
9. **TV show seasons analysis** — counts shows by number of seasons.
10. **Content ratings analysis** — charts titles by content rating.
11. **Top 10 directors** — ranks directors by listed title count.

The script also prints a final set of business insights based on these analyses.

## Dataset

The dataset is [`netflix_titles.csv`](https://www.kaggle.com/datasets/shivamb/netflix-shows), published on Kaggle as **Netflix Movies and TV Shows** by Shivam Bansal. Kaggle's dataset metadata identifies its license as **CC0: Public Domain**. The CSV is included under that declared license; see the linked source for dataset details.

The CSV is included in this project. The script expects `netflix_titles.csv` in the project root, next to `main.py`.

## Requirements and run

Use Python 3.13 or a compatible version, then install the dependencies and run the script from the project root:

```bash
python -m pip install -r requirements.txt
python main.py
```

The script saves nine PNG charts in `graphs/` and displays the plots after analysis.

## Visualizations

![Movies vs. TV shows](graphs/movies_vs_tv_shows.png)

![Netflix yearly trend](graphs/netflix_yearly_trend.png)

![Top 10 countries](graphs/top_10_countries.png)

![Country-wise content analysis](graphs/country_wise_content_analysis.png)

![Top 10 genres](graphs/top_10_genres.png)

![Movie duration](graphs/movie_duration.png)

![TV show seasons](graphs/tv_show_seasons.png)

![Content ratings](graphs/content_ratings.png)

![Top 10 directors](graphs/top_10_directors.png)

## Repository topics

`python` · `pandas` · `matplotlib` · `data-analysis` · `eda` · `data-visualization` · `netflix`
