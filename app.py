import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Content Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main {
            background-color: #f7f7f7;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .title {
            font-size: 42px;
            font-weight: 800;
            text-align: center;
            color: #E50914;
            margin-bottom: 0px;
        }

        .subtitle {
            font-size: 17px;
            text-align: center;
            color: #555555;
            margin-bottom: 30px;
        }

        .kpi-card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
            border: 1px solid #eeeeee;
        }

        .kpi-title {
            color: #666666;
            font-size: 14px;
            font-weight: 600;
        }

        .kpi-value {
            color: #E50914;
            font-size: 30px;
            font-weight: 800;
            margin-top: 5px;
        }

        h2, h3 {
            color: #222222;
        }

        section[data-testid="stSidebar"] {
            background-color: #111111;
        }

        section[data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("netflix_titles.csv")
    except FileNotFoundError:
        st.error(
            "netflix_titles.csv was not found. "
            "Place the CSV file in the same folder as app.py."
        )
        st.stop()

    # Remove duplicate records
    df = df.drop_duplicates()

    # Convert date_added to datetime
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    # Clean text fields
    text_columns = [
        "type",
        "title",
        "director",
        "cast",
        "country",
        "rating",
        "listed_in",
        "description"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    # Numeric columns
    if "release_year" in df.columns:
        df["release_year"] = pd.to_numeric(
            df["release_year"],
            errors="coerce"
        )

    # Extract additional date information
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month
    df["month_name"] = df["date_added"].dt.month_name()

    # Content age relative to release year
    df["content_age"] = (
        df["date_added"].dt.year - df["release_year"]
    )

    return df


df = load_data()

# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">🎬 NETFLIX CONTENT ANALYTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive visualization and analysis of Netflix Movies and TV Shows'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🎯 Filters")

# Content type
type_options = sorted(df["type"].dropna().unique().tolist())

selected_types = st.sidebar.multiselect(
    "Content Type",
    options=type_options,
    default=type_options
)

# Country
country_series = (
    df["country"]
    .dropna()
    .astype(str)
    .str.split(", ")
    .explode()
)

country_options = sorted(
    [
        country for country in country_series.unique()
        if country != "Unknown"
    ]
)

selected_countries = st.sidebar.multiselect(
    "Country",
    options=country_options,
    default=[]
)

# Rating
rating_options = sorted(
    [
        rating for rating in df["rating"].dropna().unique()
        if rating != "Unknown"
    ]
)

selected_ratings = st.sidebar.multiselect(
    "Rating",
    options=rating_options,
    default=[]
)

# Release year
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

year_range = st.sidebar.slider(
    "Release Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_types:
    filtered_df = filtered_df[
        filtered_df["type"].isin(selected_types)
    ]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= year_range[0]) &
    (filtered_df["release_year"] <= year_range[1])
]

if selected_ratings:
    filtered_df = filtered_df[
        filtered_df["rating"].isin(selected_ratings)
    ]

if selected_countries:
    country_pattern = "|".join(
        [country.replace("(", r"\(").replace(")", r"\)") 
         for country in selected_countries]
    )

    filtered_df = filtered_df[
        filtered_df["country"]
        .fillna("")
        .str.contains(country_pattern, case=False, regex=True)
    ]

# ============================================================
# KPI SECTION
# ============================================================

total_titles = len(filtered_df)

total_movies = len(
    filtered_df[filtered_df["type"] == "Movie"]
)

total_tv = len(
    filtered_df[filtered_df["type"] == "TV Show"]
)

unique_countries = (
    filtered_df["country"]
    .str.split(", ")
    .explode()
    .replace("Unknown", np.nan)
    .nunique()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TOTAL TITLES</div>
            <div class="kpi-value">{total_titles:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">MOVIES</div>
            <div class="kpi-value">{total_movies:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TV SHOWS</div>
            <div class="kpi-value">{total_tv:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">COUNTRIES</div>
            <div class="kpi-value">{unique_countries:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ROW 1 - CONTENT TYPE & RELEASE YEAR
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# Content Type Distribution
# ------------------------------------------------------------

with col1:

    type_counts = (
        filtered_df["type"]
        .value_counts()
        .reset_index()
    )

    type_counts.columns = ["type", "count"]

    fig_type = px.pie(
        type_counts,
        names="type",
        values="count",
        hole=0.5,
        title="Movies vs TV Shows"
    )

    fig_type.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig_type.update_layout(
        height=420,
        legend_title_text="Content Type"
    )

    st.plotly_chart(
        fig_type,
        use_container_width=True
    )

# ------------------------------------------------------------
# Release Year Distribution
# ------------------------------------------------------------

with col2:

    release_counts = (
        filtered_df
        .groupby(["release_year", "type"])
        .size()
        .reset_index(name="count")
    )

    fig_release = px.line(
        release_counts,
        x="release_year",
        y="count",
        color="type",
        markers=True,
        title="Content Production by Release Year"
    )

    fig_release.update_layout(
        height=420,
        xaxis_title="Release Year",
        yaxis_title="Number of Titles",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_release,
        use_container_width=True
    )

# ============================================================
# ROW 2 - CONTENT ADDED TO NETFLIX
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# Titles Added by Year
# ------------------------------------------------------------

with col1:

    added_by_year = (
        filtered_df
        .dropna(subset=["year_added"])
        .groupby("year_added")
        .size()
        .reset_index(name="count")
    )

    fig_added = px.bar(
        added_by_year,
        x="year_added",
        y="count",
        title="Titles Added to Netflix by Year",
        labels={
            "year_added": "Year",
            "count": "Titles Added"
        }
    )

    fig_added.update_layout(height=420)

    st.plotly_chart(
        fig_added,
        use_container_width=True
    )

# ------------------------------------------------------------
# Rating Distribution
# ------------------------------------------------------------

with col2:

    rating_counts = (
        filtered_df["rating"]
        .value_counts()
        .reset_index()
    )

    rating_counts.columns = ["rating", "count"]

    rating_counts = rating_counts.sort_values(
        "count",
        ascending=True
    )

    fig_rating = px.bar(
        rating_counts,
        x="count",
        y="rating",
        orientation="h",
        title="Content Rating Distribution",
        labels={
            "rating": "Rating",
            "count": "Titles"
        }
    )

    fig_rating.update_layout(height=420)

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )

# ============================================================
# GENRE ANALYSIS
# ============================================================

st.header("🎭 Genre Analysis")

genre_data = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .reset_index()
)

genre_data.columns = ["genre", "count"]

top_genres = genre_data.head(15).sort_values(
    "count",
    ascending=True
)

fig_genre = px.bar(
    top_genres,
    x="count",
    y="genre",
    orientation="h",
    title="Top 15 Netflix Genres",
    labels={
        "genre": "Genre",
        "count": "Number of Titles"
    }
)

fig_genre.update_layout(
    height=550
)

st.plotly_chart(
    fig_genre,
    use_container_width=True
)

# ============================================================
# COUNTRY ANALYSIS
# ============================================================

st.header("🌍 Country Analysis")

country_data = (
    filtered_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .replace("Unknown", np.nan)
    .dropna()
    .value_counts()
    .reset_index()
)

country_data.columns = ["country", "count"]

top_countries = country_data.head(15).sort_values(
    "count",
    ascending=True
)

fig_country = px.bar(
    top_countries,
    x="count",
    y="country",
    orientation="h",
    title="Top 15 Countries by Number of Titles",
    labels={
        "country": "Country",
        "count": "Titles"
    }
)

fig_country.update_layout(
    height=550
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# ============================================================
# MAP
# ============================================================

st.header("🗺️ Global Netflix Distribution")

map_data = country_data.copy()

fig_map = px.choropleth(
    map_data,
    locations="country",
    locationmode="country names",
    color="count",
    hover_name="country",
    color_continuous_scale="Reds",
    title="Netflix Titles by Country"
)

fig_map.update_layout(
    height=600
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# ============================================================
# TOP DIRECTORS
# ============================================================

st.header("🎥 Top Directors")

director_data = (
    filtered_df["director"]
    .dropna()
    .loc[lambda x: x != "Unknown"]
    .value_counts()
    .reset_index()
)

director_data.columns = ["director", "count"]

top_directors = director_data.head(10).sort_values(
    "count",
    ascending=True
)

fig_directors = px.bar(
    top_directors,
    x="count",
    y="director",
    orientation="h",
    title="Top 10 Directors",
    labels={
        "director": "Director",
        "count": "Number of Titles"
    }
)

fig_directors.update_layout(
    height=450
)

st.plotly_chart(
    fig_directors,
    use_container_width=True
)

# ============================================================
# TOP ACTORS
# ============================================================

st.header("⭐ Top Actors")

actor_data = (
    filtered_df["cast"]
    .dropna()
    .loc[lambda x: x != "Unknown"]
    .str.split(", ")
    .explode()
    .value_counts()
    .reset_index()
)

actor_data.columns = ["actor", "count"]

top_actors = actor_data.head(15).sort_values(
    "count",
    ascending=True
)

fig_actors = px.bar(
    top_actors,
    x="count",
    y="actor",
    orientation="h",
    title="Top 15 Actors",
    labels={
        "actor": "Actor",
        "count": "Number of Titles"
    }
)

fig_actors.update_layout(
    height=550
)

st.plotly_chart(
    fig_actors,
    use_container_width=True
)

# ============================================================
# MOVIE DURATION ANALYSIS
# ============================================================

st.header("⏱️ Movie Duration Analysis")

movies = filtered_df[
    filtered_df["type"] == "Movie"
].copy()

if not movies.empty:

    # Extract numeric duration
    movies["duration_minutes"] = pd.to_numeric(
        movies["duration"]
        .astype(str)
        .str.extract(r"(\d+)")[0],
        errors="coerce"
    )

    duration_data = movies.dropna(
        subset=["duration_minutes"]
    )

    if not duration_data.empty:

        fig_duration = px.histogram(
            duration_data,
            x="duration_minutes",
            nbins=30,
            title="Distribution of Movie Durations",
            labels={
                "duration_minutes": "Duration (Minutes)"
            }
        )

        fig_duration.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_duration,
            use_container_width=True
        )

        avg_duration = duration_data[
            "duration_minutes"
        ].mean()

        median_duration = duration_data[
            "duration_minutes"
        ].median()

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Average Movie Duration",
                f"{avg_duration:.1f} minutes"
            )

        with c2:
            st.metric(
                "Median Movie Duration",
                f"{median_duration:.1f} minutes"
            )

    else:
        st.info(
            "No movie duration data available for the selected filters."
        )

else:
    st.info(
        "Select Movie under Content Type to view duration analysis."
    )

# ============================================================
# TV SHOW SEASONS ANALYSIS
# ============================================================

st.header("📺 TV Show Season Analysis")

tv_shows = filtered_df[
    filtered_df["type"] == "TV Show"
].copy()

if not tv_shows.empty:

    tv_shows["seasons"] = pd.to_numeric(
        tv_shows["duration"]
        .astype(str)
        .str.extract(r"(\d+)")[0],
        errors="coerce"
    )

    season_data = tv_shows.dropna(
        subset=["seasons"]
    )

    if not season_data.empty:

        season_counts = (
            season_data["seasons"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        season_counts.columns = [
            "seasons",
            "count"
        ]

        fig_seasons = px.bar(
            season_counts,
            x="seasons",
            y="count",
            title="TV Shows by Number of Seasons",
            labels={
                "seasons": "Number of Seasons",
                "count": "Number of TV Shows"
            }
        )

        fig_seasons.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_seasons,
            use_container_width=True
        )

    else:
        st.info(
            "No season information available for the selected filters."
        )

else:
    st.info(
        "Select TV Show under Content Type to view season analysis."
    )

# ============================================================
# MONTHLY ADDITIONS
# ============================================================

st.header("📅 Monthly Content Additions")

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly_data = (
    filtered_df[
        filtered_df["month_name"].notna()
    ]["month_name"]
    .value_counts()
    .reindex(month_order)
    .fillna(0)
    .reset_index()
)

monthly_data.columns = [
    "month",
    "count"
]

fig_month = px.bar(
    monthly_data,
    x="month",
    y="count",
    title="Titles Added by Month",
    labels={
        "month": "Month",
        "count": "Titles Added"
    }
)

fig_month.update_layout(
    height=450,
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# ============================================================
# CONTENT AGE ANALYSIS
# ============================================================

st.header("📊 Content Age Analysis")

age_data = filtered_df[
    filtered_df["content_age"].notna()
].copy()

age_data = age_data[
    (age_data["content_age"] >= 0) &
    (age_data["content_age"] <= 50)
]

if not age_data.empty:

    fig_age = px.histogram(
        age_data,
        x="content_age",
        color="type",
        nbins=30,
        title="Age of Content When Added to Netflix",
        labels={
            "content_age": "Years Between Release and Netflix Addition",
            "count": "Titles"
        }
    )

    fig_age.update_layout(
        height=450
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True
    )

# ============================================================
# SEARCH TITLES
# ============================================================

st.header("🔎 Search Netflix Titles")

search_query = st.text_input(
    "Search by title",
    placeholder="Enter a movie or TV show title..."
)

if search_query:

    search_results = filtered_df[
        filtered_df["title"]
        .str.contains(
            search_query,
            case=False,
            na=False
        )
    ]

    st.write(
        f"Found **{len(search_results)}** matching title(s)."
    )

    display_columns = [
        "show_id",
        "title",
        "type",
        "director",
        "country",
        "release_year",
        "rating",
        "duration",
        "listed_in",
        "description"
    ]

    available_columns = [
        col for col in display_columns
        if col in search_results.columns
    ]

    st.dataframe(
        search_results[available_columns],
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# DATA TABLE
# ============================================================

with st.expander("📋 View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# DOWNLOAD DATA
# ============================================================

st.header("⬇️ Export Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="netflix_filtered_data.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        <b>Netflix Content Analytics Dashboard</b><br>
        Built using Python, Pandas, Streamlit and Plotly
    </div>
    """,
    unsafe_allow_html=True
)