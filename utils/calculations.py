import numpy as np

def calculate_system_capacity(num_panels, panel_wattage):
    return (num_panels * panel_wattage) / 1000

def calculate_monthly_metrics(generation, consumption, rate, excess_rate):
    self_used = min(generation, consumption)
    excess = max(0, generation - consumption)
    deficit = max(0, consumption - generation)
    savings = self_used * rate
    income = excess * excess_rate
    cost = deficit * rate
    net_benefit = savings + income - cost
    return self_used, excess, deficit, savings, income, cost, net_benefit

def calculate_annual_metrics(monthly_benefit):
    return monthly_benefit * 12

def calculate_payback_period(net_investment, annual_benefit):
    return net_investment / annual_benefit

def calculate_long_term_returns(annual_benefit, years, net_investment):
    total_savings = annual_benefit * years
    net_profit = total_savings - net_investment
    roi = (net_profit / net_investment) * 100 
    return total_savings, net_profit, roi

def calculate_fd_returns(investment, rate_percent, years):
    rate_percent= rate_percent / 100
    fd_maturity = investment * ((1 + rate_percent) ** years)
    fd_interest = fd_maturity - investment
    return fd_maturity, fd_interest
