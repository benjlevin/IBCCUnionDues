import streamlit as st

st.title("IBCC Union Dues Calculator")

st.write("""
This tool helps you estimate your union dues based on your earnings.
Dues are **1.5% of earnings** up to a wage cap of **56.15/hour**  
(which results in a maximum dues rate of **0.84 per hour worked**).
""")

# -------------------------
# Inputs
# -------------------------

employment_type = st.radio("Are you salaried or hourly?", ["Salaried", "Hourly"])

if employment_type == "Salaried":
    annual_salary = st.number_input("Annual salary (before taxes)", min_value=0, step=1000, value=116796)
    hours_per_week = st.number_input("Hours worked per week", min_value=1, value=40, step=1)

    if annual_salary > 0 and hours_per_week > 0:
        hourly_rate = annual_salary / 52 / hours_per_week
        st.write(f"**Effective hourly rate:** ${hourly_rate:,.2f}")

else:
    hourly_rate = st.number_input("Hourly wage", min_value=0.0, value=56.15)
    hours_per_week = st.number_input("Hours worked per week", min_value=1, value=40, step=1)
# -------------------------
# Dues Calculation Logic
# -------------------------

WAGE_CAP = 56.15
DUES_CAP_PER_HOUR = 0.84  # 1.5% × 56.15 = 0.84225 → capped at 0.84

hours_worked_year = 52 * hours_per_week 

if hourly_rate > 0:
    if hourly_rate >= WAGE_CAP:
        dues_per_hour = DUES_CAP_PER_HOUR
    else:
        dues_per_hour = 0.015 * hourly_rate

    dues_per_year = dues_per_hour * hours_worked_year
    dues_per_paycheck = dues_per_year / 24
    dues_per_month = dues_per_year / 12

    # For salaried workers, annual salary is known
    if employment_type == "Salaried":
        annual_earnings = annual_salary
    else:
        annual_earnings = hourly_rate * hours_worked_year

    dues_as_pct_salary = (dues_per_year / annual_earnings) * 100 if annual_earnings > 0 else 0

    # -------------------------
    # Outputs
    # -------------------------

    st.subheader("Results")

    st.metric("Dues per paycheck (24 per year)", f"${dues_per_paycheck:,.2f}")
    st.metric("Dues per month", f"${dues_per_month:,.2f}")
    st.metric("Dues per year", f"${dues_per_year:,.2f}")
    st.metric("Dues as % of annual salary", f"{dues_as_pct_salary:.2f}%")
