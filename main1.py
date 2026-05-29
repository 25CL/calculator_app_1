import streamlit as st
import math

# 1. Dictionary containing all text for both languages
TEXT = {
    "English": {
        "title": "🧮 Expression Calculator",
        "desc": "Type a full mathematical expression to calculate it all at once.",
        "expr_label": "Enter your expression:",
        "expr_help": "Use Python math syntax: ** for exponents, * for multiplication.",
        "x_val_label": "If using 'x' in your equation, set the value of x here:",
        "calc_btn": "Calculate",
        "kb_toggle": "⌨️ Show Virtual Keyboard",
        "warn_empty": "Please enter an expression.",
        "result_prefix": "**Result:**",
        "err_zero": "Error: Cannot divide by zero.",
        "err_syntax": "Error: Invalid math syntax.",
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
        "expr_help": "파이썬 수학 문법을 사용하세요: 지수는 **, 곱셈은 * 입니다.",
        "x_val_label": "수식에 'x'를 사용하는 경우, x의 값을 여기에 설정하세요:",
        "calc_btn": "계산하기",
        "kb_toggle": "⌨️ 가상 키보드 표시",
        "warn_empty": "수식을 입력해주세요.",
        "result_prefix": "**결과:**",
        "err_zero": "오류: 0으로 나눌 수 없습니다.",
        "err_syntax": "오류: 잘못된 수학 문법입니다. 연산자를 확인하세요.",
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

# 2. Callback Functions for the Virtual Keyboard
def append_to_expr(val):
    st.session_state.expr_input += val

def clear_expr():
    st.session_state.expr_input = ""

def backspace_expr():
    st.session_state.expr_input = st.session_state.expr_input[:-1]


def safe_evaluate(expression, x_value, lang_dict):
    """Safely evaluates a mathematical string expression."""
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
    
    # Initialize session state for the input box
    if "expr_input" not in st.session_state:
        st.session_state.expr_input = ""

    # Sidebar Language Selector
    lang_choice = st.sidebar.radio("Language / 언어", ["English", "한국어"])
    t = TEXT[lang_choice]

    st.title(t["title"])
    st.write(t["desc"])

    # 3. Text input tied to session state
    expression = st.text_input(
        t["expr_label"], 
        key="expr_input", # Ties this input directly to st.session_state.expr_input
        help=t["expr_help"]
    )

    # 4. Virtual Keyboard UI
    show_keyboard = st.checkbox(t["kb_toggle"], value=False)
    
    if show_keyboard:
        st.markdown("---")
        # Creating a 5-column grid for the keypad
        keys = [
            ["7", "8", "9", "/", "("],
            ["4", "5", "6", "*", ")"],
            ["1", "2", "3", "-", "**"],
            ["0", ".", "%", "+", "x"],
            ["sin(", "cos(", "log(", "Del", "Clear"]
        ]
        
        for row in keys:
            cols = st.columns(5)
            for i, key in enumerate(row):
                with cols[i]:
                    if key == "Clear":
                        st.button(key, on_click=clear_expr, use_container_width=True)
                    elif key == "Del":
                        st.button(key, on_click=backspace_expr, use_container_width=True)
                    else:
                        # Pass the specific key string to the callback function
                        st.button(key, on_click=append_to_expr, args=(key,), use_container_width=True)
        st.markdown("---")

    x_val = st.number_input(t["x_val_label"], value=1.0, format="%.4f")

    # Calculation trigger
    if st.button(t["calc_btn"], type="primary"):
        if expression.strip() == "":
            st.warning(t["warn_empty"])
        else:
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
