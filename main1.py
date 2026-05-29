import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import numpy as np

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
        "prob_desc": "Simulate various probability experiments.",
        "sim_type": "Select Simulation:",
        "sim_coin": "Coin Flip",
        "sim_dice": "Dice Roll",
        "sim_cards": "Card Draw",
        "sim_roulette": "Roulette",
        "sim_lotto": "Lottery",
        "sim_birthday": "Birthday Paradox",
        "sim_monte_carlo": "Monte Carlo π",
        "trials": "Number of Trials:",
        "run_sim": "Run Simulation",
        "coin_heads": "Heads",
        "coin_tails": "Tails",
        "xaxis": "Outcome",
        "yaxis": "Frequency",
        # 카드 게임
        "card_suit": "Card Suit:",
        "card_rank": "Card Rank:",
        "hearts": "Hearts",
        "diamonds": "Diamonds",
        "clubs": "Clubs",
        "spades": "Spades",
        "ace": "Ace",
        "king": "King",
        "queen": "Queen",
        "jack": "Jack",
        # 룰렛
        "roulette_type": "Roulette Type:",
        "roulette_red": "Red",
        "roulette_black": "Black",
        "roulette_even": "Even",
        "roulette_odd": "Odd",
        # 로또
        "lotto_info": "Pick 6 numbers (1-45):",
        "lotto_your_numbers": "Your Numbers:",
        "lotto_matches": "Matching Numbers:",
        "lotto_matches_info": "Match {0} of 6 numbers",
        # 생일 문제
        "birthday_people": "Number of People:",
        "birthday_prob": "Probability of Same Birthday:",
        "birthday_info": "Find probability that at least 2 people share a birthday",
        # Monte Carlo
        "monte_carlo_info": "Estimate π using random points in a circle",
        "monte_carlo_pi": "Estimated π:",
        "monte_carlo_actual": "Actual π:",
        "monte_carlo_error": "Error:",
        # 일반
        "stats_mean": "Mean:",
        "stats_std": "Std Dev:",
        "stats_min": "Min:",
        "stats_max": "Max:",
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
        "prob_desc": "다양한 확률 실험을 시뮬레이션 해보세요.",
        "sim_type": "시뮬레이션 선택:",
        "sim_coin": "동전 던지기",
        "sim_dice": "주사위 굴리기",
        "sim_cards": "카드 뽑기",
        "sim_roulette": "룰렛",
        "sim_lotto": "로또",
        "sim_birthday": "생일 문제",
        "sim_monte_carlo": "몬테카를로 π 추정",
        "trials": "시행 횟수:",
        "run_sim": "시뮬레이션 실행",
        "coin_heads": "앞면",
        "coin_tails": "뒷면",
        "xaxis": "결과",
        "yaxis": "발생 횟수",
        # 카드 게임
        "card_suit": "카드 무늬:",
        "card_rank": "카드 숫자:",
        "hearts": "하트",
        "diamonds": "다이아몬드",
        "clubs": "클럽",
        "spades": "스페이드",
        "ace": "에이스",
        "king": "킹",
        "queen": "퀸",
        "jack": "잭",
        # 룰렛
        "roulette_type": "룰렛 종류:",
        "roulette_red": "빨강",
        "roulette_black": "검정",
        "roulette_even": "짝수",
        "roulette_odd": "홀수",
        # 로또
        "lotto_info": "1~45 범위에서 6개 숫자 선택:",
        "lotto_your_numbers": "당신의 숫자:",
        "lotto_matches": "일치한 숫자:",
        "lotto_matches_info": "6개 중 {0}개 일치",
        # 생일 문제
        "birthday_people": "사람 수:",
        "birthday_prob": "같은 생일일 확률:",
        "birthday_info": "최소 2명이 같은 생일일 확률을 구하세요",
        # Monte Carlo
        "monte_carlo_info": "원 안의 무작위 점을 이용하여 π 추정",
        "monte_carlo_pi": "추정된 π:",
        "monte_carlo_actual": "실제 π:",
        "monte_carlo_error": "오차:",
        # 일반
        "stats_mean": "평균:",
        "stats_std": "표준편차:",
        "stats_min": "최솟값:",
        "stats_max": "최댓값:",
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

# 1. 동전 던지기
def simulate_coin_flip(trials, t):
    options = [t["coin_heads"], t["coin_tails"]]
    results = random.choices(options, k=trials)
    
    df = pd.DataFrame(results, columns=[t["xaxis"]])
    counts = df[t["xaxis"]].value_counts().reindex(options, fill_value=0).reset_index()
    counts.columns = [t["xaxis"], t["yaxis"]]
    
    fig = px.bar(counts, x=t["xaxis"], y=t["yaxis"], text=t["yaxis"],
                 title=f"Coin Flip - {trials:,} Trials / {trials:,}회 시행",
                 color=t["xaxis"], template="plotly_white")
    fig.update_traces(textposition='outside')
    return fig, counts

# 2. 주사위 굴리기
def simulate_dice_roll(trials, t):
    options = ["1", "2", "3", "4", "5", "6"]
    results = random.choices(options, k=trials)
    
    df = pd.DataFrame(results, columns=[t["xaxis"]])
    counts = df[t["xaxis"]].value_counts().reindex(options, fill_value=0).reset_index()
    counts.columns = [t["xaxis"], t["yaxis"]]
    
    fig = px.bar(counts, x=t["xaxis"], y=t["yaxis"], text=t["yaxis"],
                 title=f"Dice Roll - {trials:,} Trials / {trials:,}회 시행",
                 color=t["xaxis"], template="plotly_white")
    fig.update_traces(textposition='outside')
    return fig, counts

# 3. 카드 뽑기
def simulate_card_draw(trials, t):
    suits = [t["hearts"], t["diamonds"], t["clubs"], t["spades"]]
    ranks = [t["ace"], "2", "3", "4", "5", "6", "7", "8", "9", "10", t["jack"], t["queen"], t["king"]]
    cards = [f"{rank} of {suit}" for suit in suits for rank in ranks]
    
    results = random.choices(cards, k=trials)
    
    df = pd.DataFrame(results, columns=[t["xaxis"]])
    counts = df[t["xaxis"]].value_counts().reset_index().sort_values(by=t["yaxis"], ascending=False).head(10)
    counts.columns = [t["xaxis"], t["yaxis"]]
    
    fig = px.bar(counts, x=t["yaxis"], y=t["xaxis"], orientation='h',
                 title=f"Card Draw - Top 10 Cards in {trials:,} Trials",
                 template="plotly_white")
    return fig, counts

# 4. 룰렛
def simulate_roulette(trials, roulette_type, t):
    if roulette_type == "Color":
        # 확률: 빨강/검정 = 18/37, 0 = 1/37
        options = [t["roulette_red"], t["roulette_black"], "0"]
        weights = [18, 18, 1]
    elif roulette_type == "Even/Odd":
        options = [t["roulette_even"], t["roulette_odd"], "0"]
        weights = [18, 18, 1]
    
    results = random.choices(options, weights=weights, k=trials)
    
    df = pd.DataFrame(results, columns=[t["xaxis"]])
    counts = df[t["xaxis"]].value_counts().reindex(options, fill_value=0).reset_index()
    counts.columns = [t["xaxis"], t["yaxis"]]
    
    fig = px.pie(counts, values=t["yaxis"], names=t["xaxis"],
                 title=f"Roulette - {roulette_type} ({trials:,} Trials)")
    return fig, counts

# 5. 로또
def simulate_lottery(trials, t):
    match_results = []
    
    for _ in range(trials):
        # 실제 당첨 번호
        winning_numbers = set(random.sample(range(1, 46), 6))
        # 플레이어 번호
        player_numbers = set(random.sample(range(1, 46), 6))
        # 일치 개수
        matches = len(winning_numbers & player_numbers)
        match_results.append(matches)
    
    counter = Counter(match_results)
    df = pd.DataFrame(list(counter.items()), columns=[t["xaxis"], t["yaxis"]])
    df = df.sort_values(by=t["xaxis"])
    
    fig = px.bar(df, x=t["xaxis"], y=t["yaxis"], text=t["yaxis"],
                 title=f"Lottery - Matching Numbers Distribution ({trials:,} Trials)",
                 labels={t["xaxis"]: "Matching Numbers", t["yaxis"]: "Frequency"},
                 template="plotly_white")
    fig.update_traces(textposition='outside')
    return fig, df

# 6. 생일 문제
def simulate_birthday_paradox(num_people, trials, t):
    same_birthday_count = 0
    
    for _ in range(trials):
        # 무작위로 생일 생성 (1-365)
        birthdays = random.choices(range(1, 366), k=num_people)
        # 중복이 있는지 확인
        if len(set(birthdays)) < len(birthdays):
            same_birthday_count += 1
    
    probability = same_birthday_count / trials
    
    # 이론적 확률
    if num_people > 365:
        theoretical_prob = 1.0
    else:
        theoretical_prob = 1.0
        for i in range(num_people):
            theoretical_prob *= (365 - i) / 365
        theoretical_prob = 1 - theoretical_prob
    
    # 막대 그래프로 표시
    data = {
        "Type": ["Simulated", "Theoretical"],
        "Probability": [probability, theoretical_prob]
    }
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x="Type", y="Probability", text="Probability",
                 title=f"Birthday Paradox - {num_people} People ({trials:,} Trials)",
                 template="plotly_white")
    fig.update_traces(textposition='outside')
    fig.update_yaxes(range=[0, 1])
    
    return fig, {"simulated": probability, "theoretical": theoretical_prob}

# 7. 몬테카를로 π 추정
def simulate_monte_carlo_pi(trials, t):
    inside_circle = 0
    
    for _ in range(trials):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
    
    estimated_pi = 4 * inside_circle / trials
    actual_pi = math.pi
    error = abs(estimated_pi - actual_pi)
    
    # 시각화
    sample_size = min(5000, trials)
    x_coords, y_coords, colors = [], [], []
    inside_count = 0
    
    for _ in range(sample_size):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        x_coords.append(x)
        y_coords.append(y)
        if x**2 + y**2 <= 1:
            colors.append("Inside")
            inside_count += 1
        else:
            colors.append("Outside")
    
    fig = go.Figure()
    
    inside_data = [x_coords[i] for i in range(len(x_coords)) if colors[i] == "Inside"]
    inside_y = [y_coords[i] for i in range(len(y_coords)) if colors[i] == "Inside"]
    outside_data = [x_coords[i] for i in range(len(x_coords)) if colors[i] == "Outside"]
    outside_y = [y_coords[i] for i in range(len(y_coords)) if colors[i] == "Outside"]
    
    fig.add_trace(go.Scatter(x=inside_data, y=inside_y, mode='markers', 
                             name='Inside Circle', marker=dict(color='red', size=3)))
    fig.add_trace(go.Scatter(x=outside_data, y=outside_y, mode='markers',
                             name='Outside Circle', marker=dict(color='blue', size=3)))
    
    fig.update_layout(title=f"Monte Carlo π Estimation ({trials:,} Trials)",
                      xaxis_title="X", yaxis_title="Y",
                      template="plotly_white", height=600)
    fig.update_xaxes(scaleanchor="y", scaleratio=1)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    
    return fig, {"estimated": estimated_pi, "actual": actual_pi, "error": error}

def probability_app(t):
    st.title(t["prob_title"])
    st.write(t["prob_desc"])
    
    st.markdown("---")
    
    # 시뮬레이션 선택
    sim_options = [
        t["sim_coin"],
        t["sim_dice"],
        t["sim_cards"],
        t["sim_roulette"],
        t["sim_lotto"],
        t["sim_birthday"],
        t["sim_monte_carlo"]
    ]
    
    sim_type = st.selectbox(t["sim_type"], sim_options)
    
    # 각 시뮬레이션별 입력 폼
    if sim_type == t["sim_coin"]:
        trials = st.slider(t["trials"], min_value=10, max_value=100000, value=1000, step=10)
        if st.button(t["run_sim"], type="primary"):
            fig, counts = simulate_coin_flip(trials, t)
            st.plotly_chart(fig, use_container_width=True)
            st.write(counts)
    
    elif sim_type == t["sim_dice"]:
        trials = st.slider(t["trials"], min_value=10, max_value=100000, value=1000, step=10)
        if st.button(t["run_sim"], type="primary"):
            fig, counts = simulate_dice_roll(trials, t)
            st.plotly_chart(fig, use_container_width=True)
            st.write(counts)
    
    elif sim_type == t["sim_cards"]:
        trials = st.slider(t["trials"], min_value=10, max_value=100000, value=1000, step=10)
        if st.button(t["run_sim"], type="primary"):
            fig, counts = simulate_card_draw(trials, t)
            st.plotly_chart(fig, use_container_width=True)
            st.write(counts)
    
    elif sim_type == t["sim_roulette"]:
        roulette_type = st.radio(t["roulette_type"], ["Color", "Even/Odd"])
        trials = st.slider(t["trials"], min_value=10, max_value=100000, value=1000, step=10)
        if st.button(t["run_sim"], type="primary"):
            fig, counts = simulate_roulette(trials, roulette_type, t)
            st.plotly_chart(fig, use_container_width=True)
            st.write(counts)
    
    elif sim_type == t["sim_lotto"]:
        trials = st.slider(t["trials"], min_value=10, max_value=10000, value=1000, step=10)
        if st.button(t["run_sim"], type="primary"):
            fig, df = simulate_lottery(trials, t)
            st.plotly_chart(fig, use_container_width=True)
            st.write(df)
    
    elif sim_type == t["sim_birthday"]:
        num_people = st.slider(t["birthday_people"], min_value=2, max_value=100, value=23)
        st.info(t["birthday_info"])
        trials = st.slider(t["trials"], min_value=100, max_value=10000, value=1000, step=100)
        if st.button(t["run_sim"], type="primary"):
            fig, results = simulate_birthday_paradox(num_people, trials, t)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(t["birthday_prob"] + " (Simulated)", f"{results['simulated']:.4f}")
            with col2:
                st.metric(t["birthday_prob"] + " (Theoretical)", f"{results['theoretical']:.4f}")
    
    elif sim_type == t["sim_monte_carlo"]:
        st.info(t["monte_carlo_info"])
        trials = st.slider(t["trials"], min_value=100, max_value=1000000, value=10000, step=1000)
        if st.button(t["run_sim"], type="primary"):
            fig, results = simulate_monte_carlo_pi(trials, t)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t["monte_carlo_pi"], f"{results['estimated']:.6f}")
            with col2:
                st.metric(t["monte_carlo_actual"], f"{results['actual']:.6f}")
            with col3:
                st.metric(t["monte_carlo_error"], f"{results['error']:.6f}")

# --- 메인 실행 함수 ---
def main():
    st.set_page_config(page_title="Multi-Tool App", page_icon="🛠️", layout="wide")
    
    # 사이드바 언어 선택
    lang_choice = st.sidebar.radio("Language / 언어", ["한국어", "English"])
    t = TEXT[lang_choice]

    st.sidebar.markdown("---")
    
    # 사이드바 앱 선택 라우팅
    st.sidebar.subheader(t["menu_title"])
    app_choice = st.sidebar.selectbox("Go to:", [t["app_calc"], t["app_prob"]])

    if app_choice == t["app_calc"]:
        calculator_app(t)
    elif app_choice == t["app_prob"]:
        probability_app(t)

if __name__ == "__main__":
    main()
