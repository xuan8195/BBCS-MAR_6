import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
import requests

# Page Configuration
st.set_page_config(page_title="Biodiversity Insights 🌍", page_icon="🌱", layout="wide")

# Function to Load Lottie Animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Load Lottie Animations
lottie_earth = load_lottie_url("https://lottie.host/cb45d1b0-1c7d-4f31-af5a-11bb92094675/sarC5tDuzF.json")
lottie_water = load_lottie_url("https://lottie.host/8e93eb59-78d5-4ed8-836a-83c1cfbc7fdc/Zab7nt3IbR.json")
lottie_air = load_lottie_url("https://lottie.host/a021ac1a-b8b4-4f22-9b7e-52c426f41974/lheP9gNhHg.json")

# Custom CSS for Styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #088F8F;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 34px;
            font-weight: bold;
            color: #088F8F;
            margin-top: 30px;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #C1E1C1;
            border-radius: 10px;
            text-align: center;
        }
        
        .container { 
           font-size:20px; 
        }

        .highlight {
            font-weight: bold;
            color: #2E8B57;
            font-size:20px; 

        }

    </style>
""", unsafe_allow_html=True)

# 🌍 Main Header
st.markdown('<h1 class="main-title">🌍 Welcome to Biodiversity Insights 🌱</h1>', unsafe_allow_html=True)
st_lottie(lottie_earth, speed=1, height=300, key="earth")

# 🌱 Mission Section
st.markdown('<h2 class="section-title">🌿 Our Mission</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="container">
Biodiversity is facing <strong>critical challenges</strong> due to pollution, climate change, and human activities. 
<strong></strong><strong></strong>This project leverages <strong>data science</strong> to analyze global <strong>air and water quality trends</strong>, identifying regions that require urgent action. Our goal is to <strong>provide data-driven insights</strong> to foster a <strong>cleaner, sustainable future</strong>. 🌍💚  
</div>
""", unsafe_allow_html=True)

# 📊 Air & Water Quality Section
st.markdown('<h2 class="section-title">📊 Exploring Air & Water Quality Trends</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h3 style="text-align:center; color:#4682B4;">💧 Water Quality</h3>', unsafe_allow_html=True)
    st_lottie(lottie_water, speed=1, height=200, key="water")
with col2:
    st.markdown('<h3 style="text-align:center; color:#4682B4;">🌬️ Air Quality</h3>', unsafe_allow_html=True)
    st_lottie(lottie_air, speed=1, height=200, key="air")

# 📖 Project Overview
st.markdown('<h2 class="section-title">🔬 Project Overview</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="container">
This project explores <strong>air and water quality</strong> trends worldwide, analyzing key <strong>environmental factors</strong> such as:
</div>
<ul class="content">
    <li><span class="highlight">🌬️ Air Quality:</span> Assessing pollution severity by monitoring PM2.5 and PM10 levels.</li>
    <li><span class="highlight">💧 Water Quality:</span> Examining pH, turbidity, and contamination levels affecting ecosystems.</li>
</ul>
""", unsafe_allow_html=True)

# 📈 Key Insights
st.markdown('<h2 class="section-title">📈 Key Insights from Our Data</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="container">
🚀 Our analysis<strong>eveals <strong>cr</strong>ical insights</strong> into global air and water pollution trends:
</div>
<ul class="content">
    <li><span class="highlight">🔹 Rising Air Pollution:</span> PM2.5 and PM10 levels are increasing in urban regions, posing health risks.</li>
    <li><span class="highlight">🔹 Water Contamination:</span> pH imbalances and pollutants disrupt aquatic life.</li>
    <li><span class="highlight">🔹 Environmental Degradation:</span> Data shows a <strong>gradual decline in environmental quality</strong> over the years.</li>
</ul>
""", unsafe_allow_html=True)

# 🌍 Call to Action
st.markdown('<h2 class="section-title">🌍 Let’s Make a Difference!</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="container">
By harnessing the power of <strong>data science & analytics</strong>, we can drive <strong>positive environmental change</strong>. 
Join us in our mission to <strong>analyze, understand, and protect biodiversity</strong> across the globe! 🌱🌎  
</div>
""", unsafe_allow_html=True)
