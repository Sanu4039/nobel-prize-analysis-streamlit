# Nobel Prize Data Explorer

An interactive Streamlit web app that enables users to explore and analyze historical data related to Nobel Prize winners. Dive deep into gender trends, geographic distribution, institutions, and age analysis of laureates from 1901 to 2020.
**Live Demo**: [nobel.streamlit.app](https://nobel-prize-analysis-app-nyatv48wrszm8yvemonj6s.streamlit.app/)

---

## Features

- **Interactive Filters:** Filter data by year range, gender, and Nobel Prize category.
- **Overview Dashboard:** Visualize the number of prizes awarded per year with a 5-year moving average.
- **Gender Analysis:** Pie and bar charts showing gender distribution and category-wise breakdown.
- **Geographical Insights:** Top countries and animated choropleth map showing prizes over time.
- **Institutional Analysis:** Top organizations and cities based on prize count.
- **Age Analysis:** Analyze the distribution of winning ages and regression trends over time.
- **CSV Export:** Download the filtered dataset directly.

---

## Dataset

The app uses the `nobel_prize_data.csv` dataset which includes:

- Laureate names and genders  
- Birth countries and organizations  
- Categories and years of awards  
- Birth dates and calculated ages  
- Prize share percentages  

Data source: [Kaggle Nobel Prize Dataset](https://www.kaggle.com/datasets/imdevskp/nobel-prize)

---
Install Dependencies
It is recommended to use a virtual environment.
**pip install -r requirements.txt**

---
Run the App
**streamlit run app.py**
The app will open in your default browser at http://localhost:8501.

