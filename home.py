import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie


st.set_page_config(page_title=" Our Biodiversity Project",page_icon="🌍", layout="wide")



# 1. **Main Header**
st.markdown('<h1 style="color: ;">Welcome To Our Biodiversity Data Analysis Project 🌍💧🍃</h1>', unsafe_allow_html=True)

# 2. Mission
st.markdown("<h2 style='color: ;'>Our Project's Mission</h2>", unsafe_allow_html=True)
st.write("Biodiversity is one of the sectors in the world that is very hard to manage throughout the world due to everyday activities and constant changing and adaptation . This has undoubtly lead to the decrease in the quality of the environment around us . Through this project we hope that we can uncover which countries needs help with the most in this world and we strive to raise awarness about the ugrent need for sustainable practices that will be able to create a better world and environment around us . We truly believe that with have thorough research and efficient data-driven insights we can foster a cleaner and healthier planet for everyone to live in🌞.")

st.markdown("<h2 style='color: ;'>Analyzing Air and Water Quality Trends in different countries</h2>", unsafe_allow_html=True)

col1 , col2 =st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center;'>💧 Water</h3>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2927/2927491.png", width=120)

with col2:
    st.markdown("<h3 style='text-align: center;'>🌬️ Air</h3>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/8407/8407664.png", width=120)

# 3. **Introduction**
st.write("""
In this project, we chose to analyze various environmental factors, such as **air quality** and **water quality**, that every country has and we want to uncover the **trends** in different countries and figure out solutions for these countries to better manage their **air and water quality**

**Our analysis covers two main datasets:**
1. **Air Quality Data**: Including PM2.5 and PM10 levels.
2. **Water Quality Data**: Including factors like pH and turbidity.
""")


# 4. **Key Insights Section (Interactive Data)**
st.markdown("### Key Insights from Our Analysis")
st.write("""
- **Air Quality**: A significant statistics for instance is PM2.5 and PM10 which is basically the **measurement of the particle matter** which is one of the things that affects the **Air Quality** in the atmosphere
- **Water Quality**: Variations in water quality parameters like pH impact biodiversity in the region.
- **Trends Over Time**: We will examine the changes in air and water quality over the years and how it affect countries.
""")


