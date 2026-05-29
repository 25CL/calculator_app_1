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
