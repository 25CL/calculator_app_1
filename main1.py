import streamlit as st
import math

def safe_evaluate(expression, x_value=0.0):
    """
    Safely evaluates a mathematical string expression.
    Blocks built-in Python functions to prevent malicious code execution.
    """
    # 1. Create a dictionary of allowed math functions (sin, cos, log, pi, etc.)
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    
    # 2. Add support for the variable 'x' and absolute values
    allowed_names["x"] = x_value
    allowed_names["abs"] = abs

    try:
        # 3. Evaluate the string. 
        # {"__builtins__": None} is the security lock that blocks system commands.
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result, None
    except ZeroDivisionError:
        return None, "Error: Cannot divide by zero."
    except SyntaxError:
        return None, "Error: Invalid math syntax. Check your operators (e.g., use '*' for multiplication, not just '2x')."
    except NameError as e:
        return None, f"Error: Unsupported function or invalid character used. ({e})"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"


def main():
    st.set_page_config(page_title="Expression Calculator", page_icon="🧮")
    st.title("🧮 Expression Calculator")
    st.write("Type a full mathematical expression to calculate it all at once.")

    # Input section
    expression = st.text_input(
        "Enter your expression:", 
        value="2 * x**2 + 3 * x - 5",
        help="Use Python math syntax: ** for exponents, * for multiplication. Example: math.log(10) or 2**3"
    )

    # Optional variable input for polynomials
    x_val = st.number_input("If using 'x' in your equation, set the value of x here:", value=1.0, format="%.4f")

    # Calculation trigger
    if st.button("Calculate"):
        if expression.strip() == "":
            st.warning("Please enter an expression.")
        else:
            result, error = safe_evaluate(expression, x_value=x_val)
            
            if error:
                st.error(error)
            else:
                st.success(f"**Result:** {result}")

    st.markdown("---")
    st.markdown("""
    ### 💡 Quick Guide to Math Syntax:
    * **Addition / Subtraction:** `+` , `-`
    * **Multiplication / Division:** `*` , `/`
    * **Exponents:** `**` *(e.g., $x^3$ is written as `x**3`)*
    * **Modulo:** `%`
    * **Logarithms:** `log(value, base)` *(e.g., `log(100, 10)`)*
    * **Trigonometry:** `sin(x)`, `cos(x)`, `tan(x)`
    * **Constants:** `pi`, `e`
    """)

if __name__ == "__main__":
    main()
