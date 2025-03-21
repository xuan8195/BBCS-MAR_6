import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA  # ML Forecasting
from sklearn.ensemble import IsolationForest  # Anomaly Detection
import os

st.set_page_config(page_title="Air Quality Analysis", page_icon="💨", layout="wide")

# ---- Auto-Detect File Path ----
@st.cache_data
def find_file():
    """Automatically detects the data file path in the working directory."""
    possible_paths = ["global_air_quality_data_10000.csv", "./data/global_air_quality_data_10000.csv"]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    st.error("Error: Data file not found. Please check the file location.")
    return None

# ---- Load dataset ----
@st.cache_data
def load_air_quality_data():
    file_path = find_file()
    if file_path is None:
        return None
    
    df = pd.read_csv(file_path)

    # Ensure 'Date' column is present and properly formatted
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # Convert Date to datetime
        df.dropna(subset=["Date"], inplace=True)  # Remove invalid dates
        
        # ✅ FIX: Remove duplicate dates before setting index
        df = df.sort_values("Date").drop_duplicates(subset=["Date"], keep="first")
        
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
    else:
        st.error("The dataset does not contain a 'Date' column. Check your CSV file.")
        return None

    return df

df = load_air_quality_data()

if df is not None:
    # ---- Sidebar Filters ----
    st.sidebar.header("🔍 Filter Data")
    selected_country = st.sidebar.selectbox("🌍 Select Country", df["Country"].unique())
    selected_city = st.sidebar.selectbox("🏙️ Select City", df[df["Country"] == selected_country]["City"].unique())
    selected_year = st.sidebar.selectbox("📅 Select Year", df["Year"].unique())
    selected_pollutant = st.sidebar.radio("☁️ Select Pollutant", ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])

    # Apply Filters
    df_filtered = df[(df["Country"] == selected_country) & (df["City"] == selected_city) & (df["Year"] == selected_year)].copy()
    
    # ✅ FIX: Remove duplicate dates before setting index
    df_filtered = df_filtered.sort_values("Date").drop_duplicates(subset=["Date"], keep="first")

    # Ensure sorting and valid numeric data
    df_filtered = df_filtered.set_index("Date")
    df_filtered = df_filtered.select_dtypes(include=[np.number])  # Keep only numeric columns
    df_filtered = df_filtered.asfreq("D").interpolate(method="time")  # Ensure daily frequency and fill gaps

    # ---- Header with Engaging Description ----
    st.markdown("<h1 style='text-align: center;'>🌎 Air Quality Analysis 🌎</h1>", unsafe_allow_html=True)
    st.write("""
    ## **Understanding the Air We Breathe 🌿**
    The air we breathe isn’t just oxygen and nitrogen—it’s a **mix of pollutants** like PM2.5, NO2, and SO2,  
    affecting **human health, biodiversity, and even the economy**.  

    📌 **Did you know?**
    - **95% of people** breathe air that **exceeds WHO pollution limits**.
    - Air pollution **reduces crop yields** by up to **30%**.
    - High PM2.5 exposure can **increase lung disease risk by 36%**.

    ### **🌍 What’s the Goal?**
    We **track, predict, and analyze** air quality to uncover trends and improve policies.
    """)

    # ---- Air Quality Forecasting ----
    st.write("## 🤖 Predicting Future Pollution Levels")
    st.write("""
    Using an **ARIMA model (AutoRegressive Integrated Moving Average)**,  
    we predict the next **3 months** of pollution levels based on past data trends.
    """)

    # Train ARIMA Model
    try:
        model = ARIMA(df_filtered[selected_pollutant], order=(5,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=90)  # Predict next 90 days

        st.write("### **📈 What do the results mean?**")
        st.write("""
        - **If pollution is increasing** → Expect **more respiratory diseases & environmental damage**.
        - **If pollution is decreasing** → Policies **may be working**.
        - **If trends are stable** → Pollution levels are **consistent**, for better or worse.
        """)

        st.markdown('<a href="https://www.kaggle.com/datasets/waqi786/global-air-quality-dataset" target="_blank">📊 DATA FROM Kaggle</a>', unsafe_allow_html=True)

        fig = px.line(x=forecast.index, y=forecast, labels={'x': 'Date', 'y': f"Predicted {selected_pollutant}"},
                      title=f"Projected {selected_pollutant} Levels for the Next 3 Months")
        fig.update_traces(line_color="red", line_width=3)
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Forecasting failed: {e}")

    # ---- Monthly Trend Visualization ----
    st.write("## 📈 Monthly Pollution Trend")
    df_filtered["Month_Year"] = df_filtered.index.to_period("M").astype(str)
    monthly_avg = df_filtered.groupby("Month_Year")[selected_pollutant].mean().reset_index()

    fig = px.line(monthly_avg, x="Month_Year", y=selected_pollutant,
                  title=f"Monthly {selected_pollutant} Trends",
                  labels={'Month_Year': 'Month-Year', selected_pollutant: f"{selected_pollutant} (µg/m³)"},
                  markers=True)
    st.plotly_chart(fig)

    # ---- Anomaly Detection ----
    st.write("## 🚨 Pollution Anomaly Detection")
    st.write("""
    **Why is anomaly detection important?**  
    - Extreme pollution spikes **often signal environmental disasters or policy failures**.
    - Detecting anomalies can **help governments enforce stricter pollution controls**.
    """)

    # Train Isolation Forest
    try:
        iso_forest = IsolationForest(contamination=0.02, random_state=42)
        df_filtered["Anomaly"] = iso_forest.fit_predict(df_filtered[[selected_pollutant]])

        fig = px.scatter(df_filtered, x=df_filtered.index, y=selected_pollutant, color=df_filtered["Anomaly"],
                         title=f"Anomalies in {selected_pollutant} Levels ({selected_city})",
                         labels={'x': 'Date', 'y': f"{selected_pollutant} (µg/m³)"},
                         color_discrete_map={1: "blue", -1: "red"})
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Anomaly detection failed: {e}")

    # ---- Show Filtered Data ----
    st.write("## 🔬 Full Dataset")
    st.dataframe(df_filtered)


