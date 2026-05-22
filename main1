import streamlit as st
import math

def main():
# Set up the page layout and title
st.set_page_config(page_title="Advanced Calculator", page_icon="🧮")
st.title("🧮 Streamlit Calculator")
st.write("A simple web app supporting basic and advanced arithmetic operations.")

# Create two columns for clean input layout
col1, col2 = st.columns(2)

with col1:
num1 = st.number_input("Enter first number (or 'Value' for Log):", value=0.0, format="%.4f")
with col2:
num2 = st.number_input("Enter second number (or 'Base' for Log):", value=0.0, format="%.4f")

# Dropdown menu to select the operation
operation = st.selectbox(
"Choose an operation:",
[
"Addition (+)",
"Subtraction (-)",
"Multiplication (*)",
"Division (/)",
"Modulo (%)",
"Exponentiation (^)",
"Logarithm (log)"
 ]
)

# Execute calculation when the button is pressed
if st.button("Calculate"):
try:
if operation == "Addition (+)":
result = num1 + num2
st.success(f"Result: {num1} + {num2} = {result}")

elif operation == "Subtraction (-)":
result = num1 - num2
st.success(f"Result: {num1} - {num2} = {result}")

elif operation == "Multiplication (*)":
result = num1 * num2
st.success(f"Result: {num1} * {num2} = {result}")

elif operation == "Division (/)":
if num2 == 0:
st.error("Error: Cannot divide by zero.")
else:
result = num1 / num2
st.success(f"Result: {num1} / {num2} = {result}")

elif operation == "Modulo (%)":
if num2 == 0:
st.error("Error: Modulo by zero is not allowed.")
else:
result = num1 % num2
st.success(f"Result: {num1} % {num2} = {result}")

elif operation == "Exponentiation (^)":
result = num1 ** num2
st.success(f"Result: {num1} ^ {num2} = {result}")

elif operation == "Logarithm (log)":
# Mathematical constraints for logarithms:
# Value must be > 0. Base must be > 0 and != 1.
if num1 <= 0:
st.error("Error: The logarithm value (first number) must be greater than 0.")
elif num2 <= 0 or num2 == 1:
st.error("Error: The logarithm base (second number) must be greater than 0 and not equal to 1.")
else:
result = math.log(num1, num2)
st.success(f"Result: log_{num2}({num1}) = {result}")

except OverflowError:
st.error("Error: The result is too large to calculate.")
except Exception as e:
st.error(f"An unexpected error occurred: {e}")

if name == "main":
main()
