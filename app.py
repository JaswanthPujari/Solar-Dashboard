import streamlit as st
import numpy_financial as npf
from utils.calculations import *
from utils.visualization import *

st.set_page_config(page_title="Solar  Dashboard", layout="wide")
st.title("Solar Plant Investment Analysis Dashboard")
#Sidebar1
st.sidebar.header("Solar System Details")
investment = st.sidebar.number_input("Total Investment (Rs)", 50000, 10000000, 296000)
panels = st.sidebar.number_input("Number of Panels", 1, 100, 5)
wattage = st.sidebar.number_input("Panel Wattage (W)", 100, 700, 545)
generation = st.sidebar.number_input("Monthly Generation (Units)", 0, 10000, 330)
#Sidebar2
st.sidebar.header("Electricity Details")
rate = st.sidebar.number_input("Electricity Rate (Rs/unit)", 1.0, 20.0, 5.9)
consumption = st.sidebar.number_input("Monthly Consumption (Units)", 0, 10000, 300)
excess_rate = st.sidebar.number_input("Excess Sale Rate (Rs/unit)", 0.0, 20.0, 2.95)
g=st.sidebar.slider("Annual inflation in electricity cost (%)",0.0,10.0,6.0,step=0.5)

#Sidebar3
st.sidebar.header("Financial Parameters")
subsidy = st.sidebar.slider("Subsidy Percentage (%)", 0, 70, 40, step=5)
fd_rate = st.sidebar.slider("FD Interest Rate (%)", 3.0, 10.0, 6.0, step=0.5)
i=st.sidebar.slider("Annual general inflation rate (%)",0.0,10.0,5.0,step=0.5)
years = st.sidebar.slider("Analysis Period (Years)", 10, 30, 25, step=5)


capacity = calculate_system_capacity(panels, wattage)
self_used, excess, deficit, savings, income, cost, net_benefit = calculate_monthly_metrics(
    generation, consumption, rate, excess_rate
)
annual_benefit = calculate_annual_metrics(net_benefit)
subsidy_amt = investment * (subsidy / 100)
net_investment = investment - subsidy_amt
payback = calculate_payback_period(net_investment, annual_benefit)
total_savings, net_profit, roi = calculate_long_term_returns(annual_benefit, years, net_investment)
fd_maturity, fd_interest = calculate_fd_returns(net_investment, fd_rate, years)
solar_advantage = net_profit - fd_interest
E0=rate*consumption
I0=net_investment
N=years
r=fd_rate
#real return
r_real = (1 + r/100) / (1 + i/100) - 1

g=g/100

PV_solar = sum((E0*12*(1+g)**(t-1)) /(1+r_real)**t for t in range(1, N+1))

NPV_solar=PV_solar-I0
#Future value of FD
FV_FD_real = (I0 * (1 + r/100)**N) / (1 + i/100)**N

cashflows = [-I0] + [E0 * 12 * ((1 + g / 100) ** (t - 1)) for t in range(1, years + 1)]
irr=npf.irr(cashflows)


tab1, tab2 = st.tabs(["Overview", "Financial Analysis"])

with tab1:
    st.subheader("Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("System Capacity (kW)", f"{capacity:.2f}")
    c2.metric("Total Investment (Rs)", f"{investment:,.0f}")
    c3.metric("Monthly Generation (Units)", generation)
    c4.metric("Monthly Net Benefit (Rs)", f"{net_benefit:,.2f}")

    st.plotly_chart(create_energy_distribution_pie(self_used, excess, deficit), use_container_width=True)
    st.plotly_chart(create_monthly_financial_bar(savings, income, cost, net_benefit), use_container_width=True)
    
with tab2:
    st.subheader("Financial Analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("Net Investment (Rs)", f"{net_investment:,.2f}")
    c2.metric("Annual Savings",f"{annual_benefit:,.2f}")
    c3.metric("Payback Period (Years)", f"{payback:.2f}")
    
    c1,c2,c3,c4=st.columns(4)
    c1.metric("PV of solar savings",f"{PV_solar:,.2f}")
    c2.metric("NPV of solar",f"{NPV_solar:,.2f}")
    c3.metric("FD real return",f"{r_real*100:,.2f}%")
    c4.metric("Solar real return",f"{irr*100:,.2f}%")
    if(NPV_solar>0):
        st.success("Solar beats FD in real terms")
    st.markdown("**Subsidy Impact Analysis**")
    subsidy_levels = [0, 20, 30, 40, 50]
    rows=[]
    for s in subsidy_levels:
        SA=investment*(s/100)
        NI=investment-SA
        PB=calculate_payback_period(NI,annual_benefit)
        NP=calculate_long_term_returns(annual_benefit,years,NI)
        rows.append({
            "Subsidy %":s,
            "Subsidy Amount":SA,
            "Net Investment":NI,
            "Payback Period":f"{PB:,.2f}",
            "{}-Year Profit".format(years):NP[1]
        })
    st.dataframe(rows)
    roi_list = []
    for s in subsidy_levels:
        amt = investment * (s / 100)
        net_inv = investment - amt
        Roi= calculate_long_term_returns(annual_benefit, years, net_inv)
        roi_list.append(Roi[2])

    st.plotly_chart(create_roi_comparison_bar(subsidy_levels, roi_list), use_container_width=True)

