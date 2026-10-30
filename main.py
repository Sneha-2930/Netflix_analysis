
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# NETFLIX DATA ANALYSIS PROJECT
# ==========================================

project_folder = Path(__file__).parent
graph_folder = project_folder / "graphs"
graph_folder.mkdir(exist_ok=True)

# 1. LOAD DATASET
# ==========================================

file_path = project_folder / "netflix_titles.csv"
df = pd.read_csv(file_path)

print("\n========== NETFLIX DATASET ==========")

print("\nFirst 5 records:")
print(df.head())

print("\nDataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())


# 2. DATA CLEANING
# ==========================================

print("\n========== DATA CLEANING ==========")

print("\nMissing values before cleaning:")
print(df.isnull().sum())

text_columns = [
    "director",
    "cast",
    "country",
    "listed_in",
    "description"
]

for column in text_columns:
    df[column] = df[column].fillna("Unknown")

other_columns = [
    "date_added",
    "rating",
    "duration"
]

for column in other_columns:
    df[column] = df[column].fillna("Unknown")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nTotal missing values:",
      df.isnull().sum().sum())

print("Total duplicate rows:",
      df.duplicated().sum())

print("Final dataset shape:", df.shape)


# 3. MOVIES VS TV SHOWS
# ==========================================

print("\n========== MOVIES VS TV SHOWS ==========")

content_counts = df["type"].value_counts()
print(content_counts)

plt.figure(figsize=(8, 5))

bars = plt.bar(
    content_counts.index,
    content_counts.values
)

plt.title("Movies vs TV Shows on Netflix")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.bar_label(bars, padding=3)

plt.tight_layout()

plt.savefig(
    graph_folder / "movies_vs_tv_shows.png",
    dpi=300
)


# 4. YEAR-WISE CONTENT ANALYSIS
# ==========================================

print("\n========== YEAR-WISE ANALYSIS ==========")

year_counts = (
    df["release_year"]
    .value_counts()
    .sort_index()
)

print(year_counts)

recent_years = year_counts[year_counts.index >= 2000]

plt.figure(figsize=(12, 5))

plt.plot(
    recent_years.index,
    recent_years.values,
    marker="o"
)

plt.title("Netflix Content Released Over the Years")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    graph_folder / "netflix_yearly_trend.png",
    dpi=300
)


# 5. TOP 10 COUNTRIES
# ==========================================

print("\n========== TOP 10 COUNTRIES ==========")

countries = (
    df[df["country"] != "Unknown"]["country"]
    .str.split(",")
    .explode()
    .str.strip()
)

country_counts = countries.value_counts().head(10)
print(country_counts)

plt.figure(figsize=(10, 6))

bars = plt.barh(
    country_counts.index[::-1],
    country_counts.values[::-1]
)

plt.title("Top 10 Countries Producing Netflix Content")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.bar_label(bars, padding=3)

plt.tight_layout()

plt.savefig(
    graph_folder / "top_10_countries.png",
    dpi=300
)


# 6. COUNTRY-WISE MOVIES VS TV SHOWS ANALYSIS
# ==========================================

print("\n========== COUNTRY-WISE CONTENT ANALYSIS ==========")

country_type_df = df[
    df["country"] != "Unknown"
].copy()

# Split multiple countries into separate rows
country_type_df["country"] = (
    country_type_df["country"].str.split(",")
)

country_type_df = country_type_df.explode("country")

# Remove extra spaces
country_type_df["country"] = (
    country_type_df["country"].str.strip()
)

# Count Movies and TV Shows country-wise
country_type_counts = country_type_df.groupby(
    ["country", "type"]
).size().unstack(fill_value=0)

# Ensure both content types are available
country_type_counts = country_type_counts.reindex(
    columns=["Movie", "TV Show"],
    fill_value=0
)

# Calculate total content
country_type_counts["Total"] = (
    country_type_counts["Movie"]
    + country_type_counts["TV Show"]
)

# Select top 10 countries
top_10_country_type = country_type_counts.sort_values(
    by="Total",
    ascending=False
).head(10)

print("\nTop 10 Countries: Movies vs TV Shows")
print(top_10_country_type)

# Prepare data for graph
plot_data = top_10_country_type.drop(
    columns=["Total"]
)

plot_data.plot(
    kind="bar",
    figsize=(12, 6),
    width=0.8
)

plt.title("Movies vs TV Shows by Top 10 Countries")
plt.xlabel("Countries")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Content Type")
plt.tight_layout()

plt.savefig(
    graph_folder / "country_wise_content_analysis.png",
    dpi=300
)

# Country-wise insights
print("\nCountry with most Movies:",
      top_10_country_type["Movie"].idxmax())

print("Country with most TV Shows:",
      top_10_country_type["TV Show"].idxmax())


# 7. TOP 10 GENRES
# ==========================================

print("\n========== TOP 10 GENRES ==========")

genres = (
    df["listed_in"]
    .str.split(",")
    .explode()
    .str.strip()
)

genre_counts = (
    genres[genres != "Unknown"]
    .value_counts()
    .head(10)
)

print(genre_counts)

plt.figure(figsize=(10, 6))

bars = plt.barh(
    genre_counts.index[::-1],
    genre_counts.values[::-1]
)

plt.title("Top 10 Netflix Genres")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.bar_label(bars, padding=3)

plt.tight_layout()

plt.savefig(
    graph_folder / "top_10_genres.png",
    dpi=300
)


# 8. MOVIE DURATION ANALYSIS
# ==========================================

print("\n========== MOVIE DURATION ANALYSIS ==========")

movies = df[df["type"] == "Movie"].copy()

movies["duration_minutes"] = pd.to_numeric(
    movies["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

print("\nAverage movie duration:",
      round(movies["duration_minutes"].mean(), 2),
      "minutes")

print("\nMovie duration statistics:")
print(movies["duration_minutes"].describe())

plt.figure(figsize=(10, 5))

plt.hist(
    movies["duration_minutes"].dropna(),
    bins=20,
    edgecolor="black"
)

plt.title("Distribution of Netflix Movie Durations")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(
    graph_folder / "movie_duration.png",
    dpi=300
)


# 9. TV SHOW SEASONS ANALYSIS
# ==========================================

print("\n========== TV SHOW SEASONS ANALYSIS ==========")

tv_shows = df[df["type"] == "TV Show"].copy()

tv_shows["seasons"] = pd.to_numeric(
    tv_shows["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

season_counts = (
    tv_shows["seasons"]
    .value_counts()
    .sort_index()
)

print("\nTV Shows by number of seasons:")
print(season_counts)

plt.figure(figsize=(10, 5))

bars = plt.bar(
    season_counts.index.astype(str),
    season_counts.values
)

plt.title("Netflix TV Shows by Number of Seasons")
plt.xlabel("Number of Seasons")
plt.ylabel("Number of TV Shows")
plt.bar_label(bars, padding=3)

plt.tight_layout()

plt.savefig(
    graph_folder / "tv_show_seasons.png",
    dpi=300
)


# 10. CONTENT RATINGS ANALYSIS
# ==========================================

print("\n========== CONTENT RATINGS ==========")

rating_counts = (
    df[df["rating"] != "Unknown"]["rating"]
    .value_counts()
)

print(rating_counts)

plt.figure(figsize=(12, 6))

bars = plt.bar(
    rating_counts.index,
    rating_counts.values
)

plt.title("Netflix Content Ratings Distribution")
plt.xlabel("Content Rating")
plt.ylabel("Number of Titles")

plt.xticks(rotation=45)
plt.bar_label(bars, padding=3)

plt.tight_layout()

plt.savefig(
    graph_folder / "content_ratings.png",
    dpi=300
)


# 11. TOP 10 DIRECTORS
# ==========================================

print("\n========== TOP 10 DIRECTORS ==========")

directors = (
    df[df["director"] != "Unknown"]["director"]
    .str.split(",")
    .explode()
    .str.strip()
)

director_counts = directors.value_counts().head(10)
print(director_counts)

plt.figure(figsize=(10, 6))

bars = plt.barh(
    director_counts.index[::-1],
    director_counts.values[::-1]
)

plt.title("Top 10 Directors on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Director")
plt.bar_label(bars, padding=3)

plt.tight_layout()

plt.savefig(
    graph_folder / "top_10_directors.png",
    dpi=300
)


# FINAL BUSINESS INSIGHTS
# ==========================================

print("\n========== FINAL BUSINESS INSIGHTS ==========")

print("Total Netflix Titles:", len(df))

if not content_counts.empty:
    print("Most common content type:",
          content_counts.idxmax())

if not year_counts.empty:
    print("Year with most releases:",
          year_counts.idxmax())

if not country_counts.empty:
    print("Top producing country:",
          country_counts.idxmax())

if not genre_counts.empty:
    print("Most common genre:",
          genre_counts.idxmax())

if not rating_counts.empty:
    print("Most common rating:",
          rating_counts.idxmax())

if not director_counts.empty:
    print("Director with most listed titles:",
          director_counts.idxmax())

if not top_10_country_type.empty:
    print("Country with most Movies:",
          top_10_country_type["Movie"].idxmax())

    print("Country with most TV Shows:",
          top_10_country_type["TV Show"].idxmax())

print("\nAverage Movie Duration:",
      round(movies["duration_minutes"].mean(), 2),
      "minutes")

print("\n========== PROJECT COMPLETED ==========")

print("All analysis and graphs have been generated!")


# DISPLAY ALL GRAPHS TOGETHER
# ==========================================

plt.show()