import streamlit as st

st.set_page_config(page_title="My Calculator", page_icon="🧮")

st.title("🧮 My Calculator")
st.write("Perform basic mathematical operations!")

num1 = st.number_input("Enter first number:", value=0.0)
num2 = st.number_input("Enter second number:", value=0.0)

choice = st.selectbox(
"Select an operation:",
["Addition", "Subtraction", "Multiplication", "Division", "Modulo"]
)

if st.button("Calculate"):

  if choice == "Addition":
      result = num1 + num2
      st.success(f"{num1} + {num2} = {result}")
  elif choice == "Subtraction":
      result = num1 - num2
      st.success(f"{num1} - {num2} = {result}")
  elif choice == "Multiplication":
      result = num1 * num2
      st.success(f"{num1} × {num2} = {result}")
  elif choice == "Division":
      if num2 == 0:
          st.error("Cannot divide by zero!")
      else:
          result = num1 / num2
          st.success(f"{num1} ÷ {num2} = {result}")
  elif choice == "Modulo":
      if num2 == 0:
          st.error("Cannot calculate modulo with zero!")
      else:
          result = num1 % num2
          st.success(f"{num1} mod {num2} = {result}")
