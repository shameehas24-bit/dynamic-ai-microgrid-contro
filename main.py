import streamlit as st
import pandas as pd
import time
from core.simulation import MicrogridEnv
from core.coordinator import GlobalCoordinator
from agents.microgrid_agents import StorageAgent

# 1. Page Configuration
st.set_page_config(page_title="AI Microgrid Live Dashboard", layout="wide")

st.title("⚡ Dynamic AI Microgrid Control System")
st.markdown("### Real-Time Distributed Energy Coordination")

# 2. Initialize Architecture
env = MicrogridEnv()
coord = GlobalCoordinator()
agent = StorageAgent()

# 3. Create Dashboard Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("System Status Logs")
    log_placeholder = st.empty()  # This creates the scrolling effect

with col2:
    st.subheader("Live Performance Metrics")
    chart_placeholder = st.empty() # This allows the graph to "grow" live

# 4. Data Storage
if 'history' not in st.session_state:
    st.session_state.history = []

# 5. The Live Loop
if st.button('🚀 Start Real-Time Execution'):
    for hr in range(24):
        # Simulated Environment Inputs
        solar = 75 if 10 <= hr <= 16 else 5
        load = 45 + (30 if 18 <= hr <= 21 else 0)
        price = 0.60 if 17 <= hr <= 22 else 0.12
        
        # AI Logic Layers
        signal = coord.compute_reward(price, solar, load)
        action = agent.decide_action(signal)
        soc, grid_impact = env.step(solar, load, action)
        
        # Record Data
        data = {
            "Hour": hr, 
            "SOC (%)": soc, 
            "Solar (kW)": solar, 
            "Load (kW)": load,
            "Mode": "Charge" if action > 0 else "Discharge" if action < 0 else "Idle"
        }
        st.session_state.history.append(data)
        df = pd.DataFrame(st.session_state.history)
        
        # Update Website Components
        with log_placeholder.container():
            st.dataframe(df.tail(5)[::-1], use_container_width=True) # Shows last 5 events
            
        with chart_placeholder.container():
            st.line_chart(df.set_index("Hour")[["SOC (%)", "Solar (kW)", "Load (kW)"]])
        
        # Real-time Delay (0.5 seconds makes it look active but fast)
        time.sleep(0.5)

    st.success("✅ 24-Hour Simulation Cycle Complete!")