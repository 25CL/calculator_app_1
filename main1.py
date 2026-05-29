import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px

# 1. 다국어 텍스트 딕셔너리
TEXT = {
    "English": {
        "menu_title": "Navigation",
        "app_calc": "🧮 Calculator",
        "app_prob": "🎲 Probability Simulator",
        "title": "🧮 Expression Calculator",
        "desc": "Type a full mathematical expression to calculate it all at once.",
        "expr_label": "Enter your expression:",
        "calc_btn": "Calculate",
        "kb_toggle": "⌨️ Show Virtual Keyboard",
        "prob_title": "🎲 Probability Simulator",
        "prob_desc": "Simulate flipping a coin or rolling a die.",
        "sim_type": "Select Item:",
        "sim_coin": "Coin",
        "sim_dice": "Dice",
        "trials": "Number of Trials:",
        "run_sim": "Run Simulation",
        "coin_heads": "Heads",
        "coin_tails": "Tails",
        "xaxis": "Outcome",
        "yaxis": "Frequency"
    },
    "한국어": {
        "menu_title": "메뉴",
        "app_calc": "🧮 계산기",
        "app_prob": "🎲 확률 시뮬레이터",
        "title": "🧮 다항식 계산기",
        "desc": "전체 수학 수식을 입력하여 한 번에 계산하세요.",
        "expr_label": "수식을 입력하세요:",
        "calc_btn": "계산하기",
        "kb_toggle": "⌨️ 가상 키보드 표시",
        "prob_title": "🎲 확률 시뮬레이터",
        "prob_desc": "동전 던지기나 주사위 굴리기를 시뮬레이션 해보세요.",
        "sim_type": "시뮬레이션 선택:",
        "sim_coin": "동전",
        "sim_dice": "주사위",
        "trials": "시행 횟수:",
        "run_sim": "시뮬레이션 실행",
        "coin_heads": "앞면",
        "coin_tails": "뒷면",
        "xaxis": "결과",
        "yaxis": "발생 횟수"
    }
}

# --- 계산기 기능 모듈 ---
def append_to_expr(val):
    st.session_state.expr_input += val

def clear_expr():
    st.session_state.expr_input = ""

def backspace_expr():
    st.session_state.expr_input = st.session_state.expr_input[:-1]

def safe_evaluate(expression, x_value=1.0):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names["x"] = x_value
    allowed_names["abs"] = abs
    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result, None
    except Exception as e:
        return None, str(e)

def calculator_app(t):
    st.title(t["title"])
    st.write(t["desc"])

    if "expr_input" not in st.session_state:
        st.session_state.expr_input = ""

    expression = st.text_input(t["expr_label"], key="expr_input")

    show_keyboard = st.checkbox(t["kb_toggle"], value=False)
    if show_keyboard:
        st.markdown("---")
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
                        st.button(key, on_click=append_to_expr, args=(key,), use_container_width=True)
        st.markdown("---")

    if st.button(t["calc_btn"], type="primary"):
        if expression.strip() != "":
            result, error = safe_evaluate(expression)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success(f"**Result:** {result}")

# --- 확률 시뮬레이터 모듈 ---
def probability_app(t):
    st.title(t["prob_title"])
    st.write(t["prob_desc"])

    col1, col2 = st.columns(2)
    with col1:
        sim_type = st.radio(t["sim_type"], [t["sim_coin"], t["sim_dice"]])
    with col2:
        trials = st.number_input(t["trials"], min_value=1, max_value=100000, value=100, step=10)

    if st.button(t["run_sim"], type="primary"):
        if sim_type == t["sim_coin"]:
            options = [t["coin_heads"], t["coin_tails"]]
        else:
            options = ["1", "2", "3", "4", "5", "6"]

        results = random.choices(options, k=trials)
        
        df = pd.DataFrame(results, columns=[t["xaxis"]])
        counts = df[t["xaxis"]].value_counts().reindex(options, fill_value=0).reset_index()
        counts.columns = [t["xaxis"], t["yaxis"]]

        fig = px.bar(
            counts, 
            x=t["xaxis"], 
            y=t["yaxis"], 
            text=t["yaxis"], 
            title=f"{trials:,} Trials / 시행 결과",
            color=t["xaxis"], 
            template="plotly_white"
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)

# --- 메인 실행 함수 ---
def main():
    st.set_page_config(page_title="Multi-Tool App", page_icon="🛠️")
    
    lang_choice = st.sidebar.radio("Language / 언어", ["한국어", "English"])
    t = TEXT[lang_choice]

    st.sidebar.markdown("---")
    
    st.sidebar.subheader(t["menu_title"])
    app_choice = st.sidebar.selectbox("Go to:", [t["app_calc"], t["app_prob"]])

    if app_choice == t["app_calc"]:
        calculator_app(t)
    elif app_choice == t["app_prob"]:
        probability_app(t)

if __name__ == "__main__":
    main()
