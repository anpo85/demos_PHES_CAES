import streamlit as st
import numpy as np
import pandas as pd
import math

# =========================
# CONFIGURATION
# =========================
st.set_page_config(
    page_title="PHES & CAES Simulator",
    layout="wide"
)

st.title("🔋 Mechanical Energy Storage Simulator")
st.markdown("""
This application simulates **PHES** and **CAES** systems. 
Calculations use standard physical units, with pressure inputs in **Atmospheres (atm)**.
""")

# =========================
# CONSTANTS
# =========================
G = 9.81
RHO_WATER = 1000
J_TO_KWH = 1 / 3_600_000
ATM_TO_PA = 101325  # 1 atm = 101,325 Pascals

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Global Settings")
system = st.sidebar.radio("Select System:", ["PHES", "CAES"])

eta = st.sidebar.slider("Global Efficiency (η)", 0.50, 0.95, 0.80, 0.05)
duration_h = st.sidebar.slider("Operation Duration (hours)", 0.5, 24.0, 4.0, 0.5)

st.divider()

# ======================================================
# PHES LOGIC
# ======================================================
if system == "PHES":
    st.header("🌊 Pumped Hydro Energy Storage (PHES)")
    st.latex(r"P = \rho \cdot g \cdot Q \cdot h \cdot \eta")

    col1, col2 = st.columns(2)
    with col1:
        h = st.number_input("Hydraulic Head h (m)", 1.0, 1000.0, 100.0)
        Q = st.number_input("Flow Rate Q (m³/s)", 1.0, 500.0, 20.0)

    with col2:
        mode = st.radio("Operating Mode:", ["Discharge (Turbining)", "Charge (Pumping)"])
        V_max = st.number_input("Reservoir Capacity (m³)", 1.0, 1e8, 5e2)

    # Power Calculation
    if mode == "Discharge (Turbining)":
        p_val = (RHO_WATER * G * Q * h * eta) / 1000  # kW
    else:
        p_val = (RHO_WATER * G * Q * h / eta) / 1000  # kW

    # --- GRAPH: POWER VS WATER VOLUME ---
    # In a simple PHES, power is constant as long as there is volume
    vol_points = np.linspace(0, V_max, 100)
    # Power is 0 if volume is 0 (for discharge) or V_max (for charge),
    # but the curve usually shows the potential power availability.
    power_points = [p_val if v > 0 else 0 for v in vol_points]

    st.metric("Operational Power", f"{p_val:,.1f} kW")

    st.subheader("📈 Power in function of Water Volume")
    phes_chart_data = pd.DataFrame({
        "Water Volume (m³)": vol_points,
        "Power (kW)": power_points
    }).set_index("Water Volume (m³)")

    st.line_chart(phes_chart_data)

# ======================================================
# CAES LOGIC
# ======================================================
else:
    st.header("💨 Compressed Air Energy Storage (CAES)")
    st.latex(r"E = P_f \cdot V \cdot \ln\left(\frac{P_f}{P_i}\right) \cdot \eta")

    st.info("Input constraints: Pi ≥ 1 atm | Pf =< 100 atm")

    col1, col2 = st.columns(2)
    with col1:
        V = st.number_input("Cavern Volume V (m³)", 1.0, 1e6, 50000.0)
        p_low_atm = st.number_input("Initial Pressure Pi (atm)", min_value=1.0, value=10.0, step=1.0)
    with col2:
        p_high_atm = st.number_input("Final Pressure Pf (atm)", min_value=100.0, value=150.0, step=5.0)
        mode_caes = st.radio("Operating Mode:", ["Discharge (Expansion)", "Charge (Compression)"])

    # Conversion to Pascals
    p_low_pa = p_low_atm * ATM_TO_PA
    p_high_pa = p_high_atm * ATM_TO_PA

    # Total theoretical energy at Pf
    E_total_kwh = (p_high_pa * V * math.log(p_high_pa / p_low_pa) * eta) * J_TO_KWH

    # --- GRAPH: ENERGY VS PRESSURE ---
    # Generate pressure range
    p_range_atm = np.linspace(p_low_atm, p_high_atm, 100)
    energy_points = []

    for p_atm in p_range_atm:
        p_pa = p_atm * ATM_TO_PA
        if mode_caes == "Charge (Compression)":
            # Energy spent to reach this pressure from Pi
            e = (p_pa * V * math.log(p_pa / p_low_pa) / eta) * J_TO_KWH
        else:
            # Remaining energy available to expand back to Pi
            e = (p_pa * V * math.log(p_pa / p_low_pa) * eta) * J_TO_KWH
        energy_points.append(e)

    st.metric("Total System Energy", f"{E_total_kwh:,.1f} kWh")

    st.subheader(f"📈 Energy Evolution ({mode_caes}) in function of Pressure")
    caes_chart_data = pd.DataFrame({
        "Pressure (atm)": p_range_atm,
        "Energy (kWh)": energy_points
    }).set_index("Pressure (atm)")

    st.line_chart(caes_chart_data)

st.markdown("---")
st.caption("Simulation assumes isothermal expansion/compression for the CAES energy model and constant head for PHES.")