import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="GridPulse AI", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'grid_logs' not in st.session_state:
    st.session_state.grid_logs = pd.DataFrame(columns=['Time', 'Sector', 'Load_MW', 'Status'])

st.title("⚡ GridPulse AI | Load Optimization Hub")
st.write("Real-time Predictive Power Distribution Simulation")

st.sidebar.title("⚙️ Grid Parameters")
reserve_capacity = st.sidebar.slider("Reserve Battery Capacity (MWh)", 100, 1000, 500)
auto_rebalance = st.sidebar.toggle("Enable AI Auto-Rebalancing", value=True)

m1, m2, m3, m4 = st.columns(4)
current_demand = np.random.randint(450, 600)
m1.metric("Current Demand", f"{current_demand} MW")
m2.metric("Grid Stability", "98.2%", delta="0.5%")
m3.metric("Renewable Mix", "42%", delta="-2%")
m4.metric("Active Outages", "0")

placeholder = st.empty()

for i in range(100):
    sectors = ["Residential-A", "Industrial-X", "Commercial-C", "Healthcare-Prime"]
    sector = sectors[i % 4]
    load = np.random.randint(80, 200)
    status = "Stable" if load < 170 else "Overloaded"
    
    new_data = {
        'Time': (datetime.now()).strftime("%H:%M:%S"),
        'Sector': sector,
        'Load_MW': load,
        'Status': status
    }
    
    st.session_state.grid_logs = pd.concat([pd.DataFrame([new_data]), st.session_state.grid_logs]).head(20)
    
    with placeholder.container():
        if status == "Overloaded" and auto_rebalance:
            st.warning(f"⚠️ Load Shifting Initialized: Relieving {sector} by {load-170} MW")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.grid_logs['Time'], 
                                 y=st.session_state.grid_logs['Load_MW'], 
                                 mode='lines+markers', line=dict(color='#f1c40f')))
        fig.update_layout(title="Total Grid Load Curve (Simulated)", template="plotly_dark",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Sector Monitoring")
        st.table(st.session_state.grid_logs.head(10))

    time.sleep(1.5)
