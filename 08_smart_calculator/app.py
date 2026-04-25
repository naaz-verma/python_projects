"""
Smart Calculator - Streamlit Web App
A beginner-friendly calculator with basic math, percentages, averages, and unit conversions.
Teaches: Streamlit basics, importing modules, session state, UI layout.
"""

import streamlit as st
from operations import calculate, power, square_root, percentage, percentage_of, percentage_change, average
from converter import convert_length, convert_weight, convert_temperature
from constants import APP_NAME, VERSION, OPERATORS, LENGTH_UNITS, WEIGHT_UNITS, TEMPERATURE_UNITS


# --- Page Config ---
st.set_page_config(page_title=APP_NAME, page_icon="🧮", layout="centered")

# --- Session State for History ---
# Teaches: Streamlit session state, lists, dictionaries
if "history" not in st.session_state:
    st.session_state.history = []


def add_to_history(expression, result):
    """Save a calculation to history."""
    st.session_state.history.append({
        "expression": expression,
        "result": result,
    })


# --- Header ---
st.title("🧮 Smart Calculator")
st.caption("A Python-powered calculator built with Streamlit")

# --- Sidebar Navigation ---
# Teaches: Streamlit sidebar, radio buttons
mode = st.sidebar.radio(
    "Choose a mode:",
    ["Basic Math", "Power & Root", "Percentage", "Average", "Unit Converter", "History"],
)

# --- Basic Math ---
if mode == "Basic Math":
    st.header("Basic Math")
    st.write("Perform addition, subtraction, multiplication, and division.")

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        num1 = st.number_input("First number", value=0.0, key="basic_num1")
    with col2:
        operator_label = st.selectbox("Operator", list(OPERATORS.keys()))
    with col3:
        num2 = st.number_input("Second number", value=0.0, key="basic_num2")

    if st.button("Calculate", key="basic_calc"):
        operator_symbol = OPERATORS[operator_label]
        result = calculate(num1, num2, operator_symbol)

        if isinstance(result, str):
            st.error(result)
        else:
            expression = f"{num1} {operator_symbol} {num2}"
            st.success(f"{expression} = **{result}**")
            add_to_history(expression, result)

# --- Power & Root ---
elif mode == "Power & Root":
    st.header("Power & Root")

    tab1, tab2 = st.tabs(["Power (x^n)", "Square Root"])

    with tab1:
        st.write("Calculate a number raised to a power.")
        base = st.number_input("Base number", value=2.0, key="power_base")
        exponent = st.number_input("Exponent", value=3.0, key="power_exp")

        if st.button("Calculate Power", key="power_calc"):
            result = power(base, exponent)
            expression = f"{base} ^ {exponent}"
            st.success(f"{expression} = **{result}**")
            add_to_history(expression, result)

    with tab2:
        st.write("Calculate the square root of a number.")
        number = st.number_input("Number", value=16.0, key="sqrt_num")

        if st.button("Calculate Square Root", key="sqrt_calc"):
            result = square_root(number)
            if isinstance(result, str):
                st.error(result)
            else:
                expression = f"√{number}"
                st.success(f"{expression} = **{result}**")
                add_to_history(expression, result)

# --- Percentage ---
elif mode == "Percentage":
    st.header("Percentage Calculator")

    tab1, tab2, tab3 = st.tabs(["What % is X of Y?", "X% of Y", "% Change"])

    with tab1:
        st.write("Find what percentage one number is of another.")
        value = st.number_input("Value", value=25.0, key="pct_value")
        total = st.number_input("Total", value=100.0, key="pct_total")

        if st.button("Calculate", key="pct_calc1"):
            result = percentage(value, total)
            if isinstance(result, str):
                st.error(result)
            else:
                expression = f"{value} is what % of {total}"
                st.success(f"{value} is **{result}%** of {total}")
                add_to_history(expression, f"{result}%")

    with tab2:
        st.write("Find a given percentage of a number.")
        pct = st.number_input("Percentage (%)", value=20.0, key="pctof_pct")
        total2 = st.number_input("Of number", value=500.0, key="pctof_total")

        if st.button("Calculate", key="pct_calc2"):
            result = percentage_of(pct, total2)
            expression = f"{pct}% of {total2}"
            st.success(f"{pct}% of {total2} = **{result}**")
            add_to_history(expression, result)

    with tab3:
        st.write("Calculate the percentage increase or decrease.")
        old_val = st.number_input("Old value", value=100.0, key="pctchg_old")
        new_val = st.number_input("New value", value=120.0, key="pctchg_new")

        if st.button("Calculate", key="pct_calc3"):
            result = percentage_change(old_val, new_val)
            if isinstance(result, str):
                st.error(result)
            else:
                expression = f"% change from {old_val} to {new_val}"
                direction = "increase" if result > 0 else "decrease"
                st.success(f"**{abs(result):.2f}%** {direction}")
                add_to_history(expression, f"{result:.2f}%")

# --- Average ---
elif mode == "Average":
    st.header("Average Calculator")
    st.write("Enter numbers separated by commas to find their average.")

    numbers_input = st.text_input("Enter numbers (e.g. 10, 20, 30, 40)", value="10, 20, 30, 40")

    if st.button("Calculate Average", key="avg_calc"):
        try:
            numbers = [float(n.strip()) for n in numbers_input.split(",")]
            result = average(numbers)

            if isinstance(result, str):
                st.error(result)
            else:
                st.success(f"Average of {numbers} = **{result}**")
                st.info(f"Count: {len(numbers)} | Sum: {sum(numbers)} | Average: {result}")
                add_to_history(f"avg({numbers_input})", result)
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")

# --- Unit Converter ---
elif mode == "Unit Converter":
    st.header("Unit Converter")

    category = st.selectbox("Category", ["Length", "Weight", "Temperature"])

    if category == "Length":
        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.selectbox("From", list(LENGTH_UNITS.keys()), key="len_from")
        with col2:
            to_unit = st.selectbox("To", list(LENGTH_UNITS.keys()), index=3, key="len_to")

        value = st.number_input("Value", value=1.0, key="len_val")

        if st.button("Convert", key="len_conv"):
            result = convert_length(value, from_unit, to_unit)
            st.success(f"{value} {from_unit} = **{result} {to_unit}**")
            add_to_history(f"{value} {from_unit} -> {to_unit}", result)

    elif category == "Weight":
        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.selectbox("From", list(WEIGHT_UNITS.keys()), key="wt_from")
        with col2:
            to_unit = st.selectbox("To", list(WEIGHT_UNITS.keys()), index=2, key="wt_to")

        value = st.number_input("Value", value=1.0, key="wt_val")

        if st.button("Convert", key="wt_conv"):
            result = convert_weight(value, from_unit, to_unit)
            st.success(f"{value} {from_unit} = **{result} {to_unit}**")
            add_to_history(f"{value} {from_unit} -> {to_unit}", result)

    elif category == "Temperature":
        col1, col2 = st.columns(2)
        with col1:
            from_unit = st.selectbox("From", TEMPERATURE_UNITS, key="temp_from")
        with col2:
            to_unit = st.selectbox("To", TEMPERATURE_UNITS, index=1, key="temp_to")

        value = st.number_input("Value", value=100.0, key="temp_val")

        if st.button("Convert", key="temp_conv"):
            result = convert_temperature(value, from_unit, to_unit)
            st.success(f"{value}° {from_unit} = **{result}° {to_unit}**")
            add_to_history(f"{value}° {from_unit} -> {to_unit}", f"{result}°")

# --- History ---
elif mode == "History":
    st.header("Calculation History")

    if len(st.session_state.history) == 0:
        st.info("No calculations yet. Start calculating to build your history!")
    else:
        # Show history in reverse order (newest first)
        for i, entry in enumerate(reversed(st.session_state.history), 1):
            st.write(f"**{i}.** {entry['expression']} = {entry['result']}")

        st.divider()
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# --- Footer ---
st.sidebar.divider()
st.sidebar.caption(f"{APP_NAME} v{VERSION} | Built with Python & Streamlit")
