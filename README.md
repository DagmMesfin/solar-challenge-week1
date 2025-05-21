# Solar Data Discovery - Week 0 Challenge

This repository contains my submission for the Week 0 challenge of the **10 Academy Artificial Intelligence Mastery (AIM)** program. The project focuses on exploring and analyzing solar farm data from **Benin**, **Sierra Leone**, and **Togo** to identify high-potential regions for solar energy investment.

## 🚀 Project Objective

Analyze environmental measurements to provide data-driven recommendations for **MoonLight Energy Solutions**. The aim is to identify regions with the most solar potential and propose strategies that align with sustainability goals.

---

## ✅ Tasks Completed

### Task 1: Git & Environment Setup

* Initialized a GitHub repository with the required folder structure.
* Set up a Python virtual environment and requirements.
* Configured GitHub Actions for basic CI.
* Documented the environment setup in this README.

### Task 2: Data Profiling, Cleaning & EDA

* Performed comprehensive EDA for each country:

  * Summary stats, missing value analysis, and outlier detection.
  * Time-series trends, cleaning impact on sensor output.
  * Correlation, scatter, wind rose, and bubble plots.
* Cleaned datasets exported as `data/<country>_clean.csv`.

### Task 3: Cross-Country Comparison

* Compared **GHI**, **DNI**, and **DHI** across all three countries:
* Boxplots, statistical summaries, and ANOVA test results.
* Identified key insights and highlighted solar potential differences.

### Task 4: Interactive Dashboard

* Developed an interactive dashboard using Streamlit to visualize and explore the solar data:
  * Country-specific analysis with detailed metrics and trends
  * Cross-country comparison tools
  * Interactive visualizations for solar irradiance components (GHI, DNI, DHI)
  * Time-series analysis and correlation studies

🔗 **Access the Live Dashboard**: [Solar Challenge Dashboard](https://solar-challenge-week1-demo-dagi.streamlit.app/)

#### Dashboard Screenshots

##### Country Analysis
![Country Analysis Dashboard](dashboard_screenshots/Country_Analysis%20(1).png)
*Detailed view of country-specific solar metrics and trends*

##### Cross-Country Comparison
![Cross Country Analysis](dashboard_screenshots/Cross_Country_Analysis%20(1).png)
*Comparative analysis of solar potential across countries*

##### Interactive Visualizations
![Interactive Analysis](dashboard_screenshots/Country_Analysis%20(3).png)
*Interactive plots and correlation analysis tools*

## 🚀 Getting Started

Follow the steps below to set up and reproduce the development environment.

### 1. Clone the Repository

```bash
git clone https://github.com/DagmMesfin/solar-challenge-week1.git
cd solar-challenge-week1
```

### 2. Create and Activate a Virtual Environment


🔁 For Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```


🔁 For Windows

```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Now you are all set, run the notebooks accordingly!
