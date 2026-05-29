import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px

# 1. 다국어 텍스트 딕셔너리 (계산기 및 시뮬레이터 통합)
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
    allowed_names = {k:
