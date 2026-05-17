
# Sales, Employee & Customer Data Analysis

A professional, single-page analytics dashboard built with Python and Streamlit. Upload any CSV file and the system automatically generates interactive charts, key insights, predictive analysis, and a built-in data assistant.

---

## Features

- **Universal CSV Upload**: Drag and drop any CSV file to get instant analysis.
- **Smart Data Explorer**: Search, filter, and sort through your entire dataset.
- **Key Insights**: Auto-generated KPIs including totals, averages, and category breakdowns.
- **Visual Analytics**: Interactive bar charts and scatter plots powered by Plotly.
- **Predictive Analysis**: Linear Regression predictions based on your dataset patterns.
- **Data Assistant**: Sidebar chatbot to query your data in plain English.
- **Responsive Design**: Works on desktop, tablet, and mobile browsers.

---

## Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```

The browser will open automatically at `http://localhost:8501`.

---

## Project Structure

```
├── app.py                  # Main application (single-page dashboard)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme and server configuration
├── utils/
│   ├── style.css           # Custom dark theme styles
│   ├── data_processor.py   # Data cleaning utilities
│   ├── pdf_generator.py    # PDF report generation
│   └── generate_data.py    # Sample data generator
├── datasets/               # Sample CSV files
├── reports/                # Generated PDF reports
└── README.md
```

---

## Tech Stack

- **Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Machine Learning**: Scikit-Learn (Linear Regression)
- **Styling**: Custom CSS (Dark Theme)

---

## Deployment (Streamlit Cloud)

1. Push the project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub repo and select `app.py` as the main file.
4. Click **Deploy**.

---

## License
This project is developed for educational and internship demonstration purposes.

Made by **Dikshita**
=======
# data-analysis-dashboard

