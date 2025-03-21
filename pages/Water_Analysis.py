import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Load dataset ----
file_path = r"C:\Users\Luo Yuxuan\Desktop\tp AAI\BBCS MAR_6 project\data\water_quality.csv"
df = pd.read_csv(file_path, encoding="utf-8")

# Remove missing values to ensure cleaner visualizations
df = df.dropna()

# ---- Streamlit App ----
st.title("🌊 Water Pollution Analysis", page_icon="💧", layout="wide")

st.write("""
## 🔬 **Understanding Water Pollution & Its Impact**
Water is **essential for life**, but pollution is threatening this **critical resource**.  
Water pollution can come from **industrial waste, sewage, chemical runoff, and plastic contamination**,  
leading to devastating effects on **human health, aquatic ecosystems, and biodiversity**.

### 🌍 **Why does this matter?**
- **💀 Contaminated water causes 1.2 million deaths annually.**
- **🌾 Agricultural runoff leads to ‘dead zones’ in oceans, reducing fish populations.**
- **🏭 Industrial pollution lowers drinking water quality, affecting millions.**

This dashboard provides **insightful visualizations** to **analyze water pollution levels**  
and understand how different regions are affected.
""")

# ---- Display raw data ----
st.subheader("📊 Dataset Overview")
st.write(df.head())

# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filter Data")

# Country selection
countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("🌍 Select a country", countries)

# ---- Region Filter (Top N Selection) ----
st.sidebar.subheader("🏞️ Filter Data by Region")
region_counts = df[df['Country'] == selected_country]['Region'].value_counts()
top_regions = region_counts.nlargest(10).index.tolist()
selected_regions = st.sidebar.multiselect("Select regions", top_regions, default=top_regions)

# ---- Apply Filters ----
filtered_df = df[(df['Country'] == selected_country) & (df['Region'].isin(selected_regions))]

# ---- Data Display ----
st.subheader(f"💧 Water Pollution Data for {selected_country}")
st.write(filtered_df)

# ---- Visualization: Water Pollution by Region ----
st.subheader("🌍 Water Pollution Levels by Region")
st.write("""
### 🔎 **What can we learn?**
This bar chart shows **which regions have the highest pollution levels**.

#### 📌 **How to interpret this?**
- **Regions with higher pollution** → Could indicate **industrial zones, poor waste management, or agricultural runoff.**
- **Lower pollution regions** → Suggests **clean water sources, better filtration, or strict environmental policies.**
- **Sudden spikes in pollution** → Might be due to **seasonal factors or a recent pollution event.**

Hover over the bars to see **exact pollution levels** for each region.
""")

plt.figure(figsize=(15, 10))
sns.barplot(data=filtered_df, x="Region", y="WaterPollution", ci=None, palette="Blues_r")
plt.xticks(rotation=45)
plt.xlabel("Region")
plt.ylabel("Water Pollution Level")
plt.title(f"Water Pollution Levels by Region in {selected_country}")
st.pyplot(plt)

# ---- Scatter Plot: City vs. Water Pollution ----
st.subheader("🏙️ Water Pollution Levels by City")
st.write("""
### 🌆 **Why is this useful?**
- **Cities with high pollution** may need **urgent cleanup efforts**.
- **Clusters of cities with high pollution** → Likely due to **shared industrial activities** or **rivers carrying pollutants downstream**.
- **If pollution varies widely within a region** → Some cities may have **better water management than others**.

This scatter plot helps identify **which cities suffer the most** from water contamination.
""")

city_counts = filtered_df['City'].value_counts()
top_cities = city_counts.nlargest(15).index.tolist()
filtered_cities_df = filtered_df[filtered_df['City'].isin(top_cities)]

plt.figure(figsize=(12, 6))
sns.scatterplot(data=filtered_cities_df, x="City", y="WaterPollution", hue="Region", palette="coolwarm", alpha=0.7)
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Water Pollution Level")
plt.title(f"Water Pollution Levels by City in {selected_country}")
st.pyplot(plt)

# ---- Convert Water Pollution Column to Numeric ----
filtered_df['WaterPollution'] = pd.to_numeric(filtered_df['WaterPollution'], errors='coerce')

# ---- Aggregation: Regional Trends ----
region_trends = filtered_df.groupby('Region').agg({'WaterPollution': 'mean'}).reset_index()

# ---- Line Plot: Water Pollution Trends by Region ----
st.subheader(f"📈 Water Pollution Trends by Region in {selected_country}")
st.write("""
### 🔥 **What does this trend tell us?**
- **📈 Upward trend** → Pollution **getting worse** in certain regions.
- **📉 Downward trend** → Suggests **environmental policies are working**.
- **⚖️ Flat trend** → Pollution levels are **consistent** but may still be high.

By tracking these trends, governments can **focus on problem areas**  
and allocate resources effectively for **clean water initiatives**.
""")

plt.figure(figsize=(12, 6))
sns.lineplot(data=region_trends, x="Region", y="WaterPollution", marker="o", palette="Blues_r")
plt.xticks(rotation=45)
plt.xlabel("Region")
plt.ylabel("Average Water Pollution Level")
plt.title(f"Water Pollution Trends by Region in {selected_country}")
st.pyplot(plt)
