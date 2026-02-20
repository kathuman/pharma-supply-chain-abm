import streamlit as st
import pandas as pd
from model import PharmaModel

st.title("Pharma Supply Chain ABM Simulation")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")
sim_days = st.sidebar.slider("Simulation Duration (Days)", 10, 100, 30)
init_stock = st.sidebar.number_input("Initial Starting Material", value=1000)
capacity = st.sidebar.slider("Daily CMO Capacity", 10, 200, 50)

if st.button("Run Simulation"):
    model = PharmaModel(n_agents=6, init_stock=init_stock, capacity=capacity)
    
    data = []
    for i in range(sim_days):
        model.step()
        # Collect daily stats
        for agent in model.schedule.agents:
            data.append({"Day": i, "Agent": agent.agent_type, "Inventory": agent.inventory})
    
    df = pd.DataFrame(data)
    st.line_chart(df.pivot(index='Day', columns='Agent', values='Inventory'))
    st.success("Simulation Complete")
