# 🎬 Netflix Content Visualization

An interactive data visualization dashboard for analyzing Netflix Movies and TV Shows using Python, Pandas, Plotly, and Streamlit.

## 📌 Project Overview

The Netflix Content Visualization project analyzes a dataset containing Netflix movies and television shows.

The dashboard provides interactive visualizations that help users understand:

- The distribution of Movies and TV Shows
- Content release trends
- Netflix content additions over time
- Popular genres
- Content ratings
- Country-wise content distribution
- Top directors
- Top actors
- Movie duration
- TV show seasons
- Monthly content additions
- Age of content when added to Netflix

Users can apply filters and interact with the charts to explore the dataset.

---

## 🎯 Objectives

The main objectives of this project are:

1. Analyze Netflix content using Python.
2. Perform data cleaning and preprocessing using Pandas.
3. Create meaningful visualizations using Plotly.
4. Develop an interactive dashboard using Streamlit.
5. Identify trends and patterns in Netflix Movies and TV Shows.
6. Provide an easy-to-use interface for exploring Netflix content.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical operations |
| Plotly | Interactive data visualization |
| Streamlit | Dashboard development |
| Git & GitHub | Version control and project hosting |

---

## 📊 Dashboard Features

### 1. Content Type Analysis

The dashboard compares:

- Movies
- TV Shows

using an interactive chart.

### 2. Release Year Analysis

Shows how Netflix content is distributed across different release years.

### 3. Netflix Content Addition Trends

Analyzes how many titles were added to Netflix each year.

### 4. Rating Analysis

Displays the distribution of Netflix content according to ratings.

### 5. Genre Analysis

Identifies the most common genres available on Netflix.

### 6. Country Analysis

Shows which countries contribute the most Netflix content.

### 7. Global Distribution Map

An interactive world map visualizes Netflix content by country.

### 8. Director Analysis

Displays directors with the highest number of titles.

### 9. Actor Analysis

Identifies actors appearing in the largest number of titles.

### 10. Movie Duration Analysis

Analyzes the duration of Netflix movies.

### 11. TV Show Season Analysis

Shows the distribution of TV shows according to the number of seasons.

### 12. Monthly Content Analysis

Shows the months in which Netflix added the most titles.

### 13. Content Age Analysis

Analyzes the difference between a title's release year and the year it was added to Netflix.

### 14. Search Function

Users can search for specific Netflix titles.

### 15. Data Filtering

Users can filter the dashboard by:

- Content Type
- Country
- Rating
- Release Year

### 16. Data Export

Filtered data can be downloaded as a CSV file.

---

## 📁 Project Structure

```text
Netflix-Content-Visualization/
│
├── app.py
├── netflix_titles.csv
├── requirements.txt
├── README.md
└── .gitignore



📂 Dataset

The project uses the netflix_titles.csv dataset containing information about Netflix Movies and TV Shows.

The dataset includes fields such as:
show_id
type
title
director
cast
country
date_added
release_year
rating
duration
listed_in
description


⚙️ Installation
Step 1: Clone the repository
git clone https://github.com/Talha-ali628/Netflix-Content-Visualization.git


Step 2: Open the project
cd Netflix-Content-Visualization

Step 3: Install the required libraries
pip install -r requirements.txt

Step 4: Run the Streamlit application
streamlit run app.py
The application will open in your browser.

🖥️ Running the Dashboard

After running:
streamlit run app.py
the dashboard will normally be available at:
http://localhost:8501




📈 Key Insights

This project can be used to identify patterns such as:

Whether Netflix has more Movies or TV Shows
Which genres are most common
Which countries produce the most content
How Netflix content has changed over time
Which ratings are most frequently represented
Typical movie durations
The distribution of TV show seasons
The growth of Netflix's content library




🚀 Future Improvements

Future versions of the project could include:

Netflix recommendation system
Machine learning based content recommendations
Sentiment analysis of descriptions
Search by actor or director
Advanced genre filtering
Personalized recommendations
Real-time Netflix data integration



👨‍💻 Author

Talha Ali

GitHub:

https://github.com/Talha-ali628

⭐ Project

If you find this project useful, consider giving the repository a star ⭐


## 🚀 Live Dashboard

🔗 **[Open Netflix Content Analytics Dashboard](https://netflix-content-analytics.streamlit.app/)**