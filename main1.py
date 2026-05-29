import streamlit as st
import math

# 1. Dictionary containing all text for both languages
TEXT = {
    "English": {
        "title": "🧮 Expression Calculator",
        "desc": "Type a full mathematical expression to calculate it all at once.",
        "expr_label": "Enter your expression:",
        "expr_help": "Use Python math syntax: ** for exponents, * for multiplication. Example: math.log(10) or 2**3",
        "x_val_label": "If using 'x' in your equation, set the value of x here:",
        "calc_btn": "Calculate",
        "warn_empty": "Please enter an expression.",
        "result_prefix": "**Result:**",
        "err_zero": "Error: Cannot divide by zero.",
        "err_syntax": "Error: Invalid math syntax. Check your operators (e.g., use '*' for multiplication, not just '2x').",
        "err_name": "Error: Unsupported function or invalid character used.",
        "err_unexpected": "An unexpected error occurred:",
        "guide_title": "### 💡 Quick Guide to Math Syntax:",
        "guide_text": """
* **Addition / Subtraction:** `+` , `-`
* **Multiplication / Division:** `*` , `/`
* **Exponents:** `**` *(e.g., $x^3$ is written as `x**3`)*
* **Modulo:** `%`
* **Logarithms:** `log(value, base)` *(e.g., `log(100, 10)`)*
* **Trigonometry:** `sin(x)`, `cos(x)`, `tan(x)`
* **Constants:** `pi`, `e`
        """
    },
    "한국어": {
        "title": "🧮 다항식 계산기",
        "desc": "전체 수학 수식을 입력하여 한 번에 계산하세요.",
        "expr_label": "수식을 입력하세요:",
        "expr_help": "파이썬 수학 문법을 사용하세요: 지수는 **, 곱셈은 * 입니다. 예: math.log(10) 또는 2**3",
        "x_val_label": "수식에 'x'를 사용하는 경우, x의 값을 여기에 설정하세요:",
        "calc_btn": "계산하기",
        "warn_empty": "수식을 입력해주세요.",
        "result_prefix": "**결과:**",
        "err_zero": "오류: 0으로 나눌 수 없습니다.",
        "err_syntax": "오류: 잘못된 수학 문법입니다. 연산자를 확인하세요 (예: '2x' 대신 '2*x' 사용).",
        "err_name": "오류: 지원되지 않는 함수나 잘못된 문자가 사용되었습니다.",
        "err_unexpected": "예기치 않은 오류가 발생했습니다:",
        "guide_title": "### 💡 수학 문법 빠른 안내:",
        "guide_text": """
* **덧셈 / 뺄셈:** `+` , `-`
* **곱셈 / 나눗셈:** `*` , `/`
* **지수:** `**` *(예: $x^3$은 `x**3`으로 입력)*
* **나머지 (모듈로):** `%`
* **로그:** `log(값, 밑)` *(예: `log(100, 10)`)*
* **삼각함수:** `sin(x)`, `cos(x)`, `tan(x)`
* **상수:** `pi`, `e`
        """
    }
}

def safe_evaluate(expression, x_value, lang_dict):
    """
    Safely evaluates a mathematical string expression and returns localized errors.
    """
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names["x"] = x_value
    allowed_names["abs"] = abs

    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result, None
    except ZeroDivisionError:
        return None, lang_dict["err_zero"]
    except SyntaxError:
        return None, lang_dict["err_syntax"]
    except NameError as e:
        return None, f'{lang_dict["err_name"]} ({e})'
    except Exception as e:
        return None, f'{lang_dict["err_unexpected"]} {e}'

def main():
    st.set_page_config(page_title="Expression Calculator", page_icon="🧮")
    
    # 2. Sidebar Language Selector
    lang_choice = st.sidebar.radio("Language / 언어", ["English", "한국어"])
    
    # 3. Load the selected language dictionary
    t = TEXT[lang_choice]

    st.title(t["title"])
    st.write(t["desc"])

    # Input section
    expression = st.text_input(
        t["expr_label"], 
        value="2 * x**2 + 3 * x - 5",
        help=t["expr_help"]
    )

    x_val = st.number_input(t["x_val_label"], value=1.0, format="%.4f")

    # Calculation trigger
    if st.button(t["calc_btn"]):
        if expression.strip() == "":
            st.warning(t["warn_empty"])
        else:
            # Pass the language dictionary to safe_evaluate to get translated errors
            result, error = safe_evaluate(expression, x_value=x_val, lang_dict=t)
            
            if error:
                st.error(error)
            else:
                st.success(f'{t["result_prefix"]} {result}')

    st.markdown("---")
    st.markdown(t["guide_title"])
    st.markdown(t["guide_text"])

if __name__ == "__main__":
    main()
