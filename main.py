import streamlit as st
import pandas as pd
import numpy as np
import time
from core.simulation import MicrogridEnv
from core.coordinator import GlobalCoordinator
from agents.microgrid_agents import StorageAgent

# Page Configuration
st.set_page_config(page_title="AI Microgrid Live Dashboard", layout="wide")

st.title("⚡ Dynamic AI Microgrid Control System")
st.markdown("This dashboard shows the **Global Coordinator** and **Local Agents** making real-time decisions.")

# Initialize System
env = MicrogridEnv()
coord = GlobalCoordinator()
agent = StorageAgent()

# Setup Layout
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Live Status Logs")
    log_container = st.empty() # For the scrolling text
with col2:
    st.subheader("Performance Visualization")
    chart_container = st.line_chart(pd.DataFrame(columns=["SOC", "Solar", "Load"]))

# Persistent Data Storage
if 'history' not in st.session_state:
    st.session_state.history = []

# REAL-TIME LOOP
for hr in range(24):
    # Simulated Inputs
    solar = 80 if 10 <= hr <= 16 else 10
    load = 50 + (25 if 18 <= hr <= 21 else 0)
    price = 0.55 if 17 <= hr <= 22 else 0.15
    
    # AI Decision
    signal = coord.compute_reward(price, solar)
    action = agent.decide_action(signal)
    soc = env.step(solar, load, action)
    
    # Update Data
    new_data = {"Hour": hr, "SOC": soc, "Solar": solar, "Load": load}
    st.session_state.history.append(new_data)
    df = pd.DataFrame(st.session_state.history)
    
    # Update Logs (Scrolling Effect)
    status = "🟢 CHARGING" if action > 0 else "🔴 DISCHARGING" if action < 0 else "⚪ IDLE"
    log_container.write(df.tail(10)[::-1]) # Shows last 10 rows, newest on top
    
    # Update Graphs
    chart_container.line_chart(df.set_index("Hour")[["SOC", "Solar", "Load"]])
    
    # WAIT 10 SECONDS (Change this to 1 for your video if you're in a hurry!)
    time.sleep(10)