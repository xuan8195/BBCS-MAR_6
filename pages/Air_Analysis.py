import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA  # ML Forecasting
from sklearn.ensemble import IsolationForest  # Anomaly Detection

st.set_page_config(page_title="Air Quality Analysis", page_icon="💨", layout="wide")

# ---- Load dataset ----
@st.cache_data
def load_air_quality_data():
    df = pd.read_csv(r"C:\Users\Luo Yuxuan\Desktop\tp AAI\BBCS MAR_6 project\data\global_air_quality_data_10000.csv")

    # Ensure 'Date' column is in datetime format
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
    else:
        st.error("The dataset does not contain a 'Date' column. Check your CSV file.")

    return df

df = load_air_quality_data()

# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filter Data")
selected_country = st.sidebar.selectbox("🌍 Select Country", df["Country"].unique())
selected_city = st.sidebar.selectbox("🏙️ Select City", df[df["Country"] == selected_country]["City"].unique())
selected_year = st.sidebar.selectbox("📅 Select Year", df["Year"].unique())
selected_pollutant = st.sidebar.radio("☁️ Select Pollutant", ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])

# Apply Filters
df_filtered = df[(df["Country"] == selected_country) & (df["City"] == selected_city) & (df["Year"] == selected_year)].copy()

# ---- Header with Engaging Description ----
st.markdown("<h1 style='text-align: center;'>🌎 Air Quality Analysis 🌎</h1>", unsafe_allow_html=True)
st.write("""
## **Understanding the Air We Breathe 🌿 (And Why It’s Not Just Oxygen)**
If air had an **ingredients label**, we’d hope to see **78% nitrogen, 21% oxygen, and a sprinkle of noble gases**.  
Unfortunately, modern air is more like a **chemical soup**, featuring **PM2.5, NO2, SO2, CO, and ozone (O3)**, which have significant impacts on human health, **biodiversity, agriculture, and climate change**.

📌 **Did you know?**
- **95% of the world’s population** breathes air that **exceeds WHO pollution limits**.
- **Air pollution reduces global GDP by 2.5% annually** due to increased **healthcare costs and reduced productivity**.
- **PM2.5 exposure** can **increase the risk of lung disease by 36%** and is linked to higher **mortality rates** in urban populations.
- **Biodiversity is under threat!** Pollutants like **NO2 and SO2** contribute to **acid rain**, damaging forests, water bodies, and wildlife.

### 🌍 **So what’s the goal here?**
This project **tracks, predicts, and visualizes** pollution trends so we can understand **how air quality changes over time** and its **real-world effects**.  
Is it improving? Worsening? **Or should we start looking for real estate on Mars?** 🚀
""")

# ---- Fix for ARIMA Forecasting ----
st.write("## 🤖 Predicting Future Pollution Levels")
st.write("""
**Why do we need predictions?**  
Understanding **future pollution trends** helps governments and businesses **plan policies, reduce emissions, and protect public health**.  

### 🔬 **How does this work?**
We use an **ARIMA model (AutoRegressive Integrated Moving Average)** that:
- **Looks at past pollution levels** and detects trends.
- **Predicts the next 3 months** of pollution based on patterns.
- **Identifies whether air quality is getting better or worse** over time.

""")

# Handle duplicate dates & missing values
df_filtered = df_filtered.sort_values("Date").set_index("Date")
df_filtered = df_filtered.select_dtypes(include=[np.number])  # Use only numeric columns
df_filtered = df_filtered.groupby(df_filtered.index).mean()
df_filtered = df_filtered.asfreq("D").interpolate(method="time")

# Train ARIMA Model
try:
    model = ARIMA(df_filtered[selected_pollutant], order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=90)  # Predict next 90 days

    st.write("""
    ### 📈 **What do the results mean?**
    - **If pollution is increasing** → Expect **higher respiratory diseases, crop yield reduction, and more acid rain**.
    - **If pollution is decreasing** → Policies like **low-emission zones, renewable energy investments, and stricter regulations may be working**.
    - **If trends are stable** → Pollution levels are consistent, which can be **good or bad**, depending on whether the levels are high or low.

    """)
    fig = px.line(x=forecast.index, y=forecast, labels={'x': 'Date', 'y': f"Predicted {selected_pollutant}"})
    fig.update_traces(line_color="red", line_width=3)
    fig.update_layout(title=f"Projected {selected_pollutant} Levels for the Next 3 Months")
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"Forecasting failed: {e}")

# ---- Monthly Trend Visualization ----
st.write("## 📈 Monthly Pollution Trend")
st.write("""
### 🌡️ **What causes pollution to change across months?**
- **Winter months:** 🚗 More **vehicle emissions** and **heating pollution**.
- **Summer:** ☀️ Higher **ozone (O3) levels** due to heat-triggered chemical reactions.
- **Monsoon:** 🌧️ Rain **clears pollutants**, but **high humidity traps particles**.

### 🌍 **Why does this matter?**
- **If pollution spikes in winter**, it suggests **vehicle and heating emissions are a key problem**.
- **If pollution is lower in monsoon**, it shows **rain helps improve air quality**.
- **If pollution is high in summer**, ground-level ozone could be increasing, leading to **respiratory issues**.

""")

df_filtered["Month_Year"] = df_filtered.index.to_period("M").astype(str)
monthly_avg = df_filtered.groupby("Month_Year")[selected_pollutant].mean().reset_index()

fig = px.bar(monthly_avg, x="Month_Year", y=selected_pollutant, title=f"Monthly {selected_pollutant} Trends in {selected_city}",
             labels={'Month_Year': 'Month-Year', selected_pollutant: f"{selected_pollutant} (µg/m³)"},
             color=selected_pollutant, color_continuous_scale="reds")
st.plotly_chart(fig)

# ---- Anomaly Detection ----
st.write("## 🚨 Pollution Anomaly Detection")
st.write("""
**Why is anomaly detection important?**  
Extreme pollution spikes are **often linked to major events** like **industrial shutdowns, wildfires, or heavy vehicle congestion**.

### 🔬 **What does this tell us?**
- **Red points** → Days with **extreme pollution levels** (could be from factory emissions, wildfire smoke, or urban traffic jams).
- **Blue points** → Normal pollution days.
- **If anomalies happen frequently**, it could indicate **unregulated industrial activities or environmental disasters**.

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
