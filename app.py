import streamlit as st
import pandas as pd
from model import PharmaModel

# Set Page Config for a professional look
st.set_page_config(page_title="Pharma Supply Chain Sim", layout="wide")

st.title("🧪 Pharma Supply Chain: Agent-Based Model")
st.markdown("""
This simulation models the flow of material through various CMOs. 
Each agent processes inventory based on **Capacity** and **Yield Rates**.
""")

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")
sim_days = st.sidebar.slider("Days to Simulate", 5, 120, 60)
init_stock = st.sidebar.number_input("Initial Starting Material (kg)", value=1000)
daily_cap = st.sidebar.slider("CMO Daily Capacity (kg/day)", 10, 200, 40)

# --- Execution ---
if st.button("🚀 Run Simulation"):
    # Initialize the model with UI parameters
    model = PharmaModel(init_stock=init_stock, capacity=daily_cap)
    
    # Data container for plotting
    history = []
    
    for day in range(sim_days):
        model.step()
        # Collect current state of all agents
        for agent in model.agents:
            history.append({
                "Day": day,
                "Stage": agent.agent_type,
                "Inventory": round(agent.inventory, 2)
            })
    
    # --- Visualization ---
    df = pd.DataFrame(history)
    
    # Create a Pivot Table for the Line Chart
    chart_data = df.pivot(index='Day', columns='Stage', values='Inventory')
    
    st.subheader("Inventory Levels Over Time")
    st.line_chart(chart_data)
    
    # Display the final results in a table
    st.subheader("Final State Analysis")
    final_day = df[df['Day'] == sim_days - 1]
    st.table(final_day[['Stage', 'Inventory']])
    
    st.success(f"Simulation of {sim_days} days completed successfully!")
