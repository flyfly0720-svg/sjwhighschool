import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------------
# 페이지 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(page_title="📚 교육과정 박람회 발표", page_icon="📚", layout="wide")

# 과목별 이모지 매핑 (필요하면 자유롭게 수정하세요)
EMOJI = {
    "언어와 매체": "📖",
    "확률과 통계": "🎲",
    "기하": "📐",
    "고급수학": "➗",
    "미적분": "📈",
    "물리학1": "⚛️",
    "화학1": "🧪",
    "생명과학1": "🧬",
    "화학2": "🧫",
    "생명과학2": "🔬",
}

DEFAULT_SUBJECTS = list(EMOJI.keys())

# ----------------------------------------------------------------------------
# 사이드바 내비게이션
# ----------------------------------------------------------------------------
st.sidebar.title("📚 목차")
page = st.sidebar.radio(
    "슬라이드 선택",
    ["🏠 표지", "📊 내신 선택과목", "🈶 국어 - 언어와 매체", "🔢 수학"],
)

st.sidebar.markdown("---")
st.sidebar.caption("👈 왼쪽에서 슬라이드를 선택하세요")

# ============================================================================
# 슬라이드 1. 표지
# ============================================================================
if page == "🏠 표지":
    st.markdown(
        """
        <div style="text-align:center; padding: 80px 0;">
            <h1 style="font-size:56px;">📚 교육과정 박람회</h1>
            <h3 style="color:gray;">30719 서재원</h3>
            <p style="font-size:24px;">✨ 나의 내신 선택과목과 학습 전략 소개 ✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("🈶 국어", "언어와 매체")
    col2.metric("🔢 수학", "확통·기하·고급수학·미적분")
    col3.metric("🧪 과학", "물리1·화학1·생1·화학2·생2")

# ============================================================================
# 슬라이드 2. 내신 선택과목 - 그래프 (내림차순)
# ============================================================================
elif page == "📊 내신 선택과목":
    st.header("📊 내신 선택과목")
    st.write(
        "아래 표의 **등급(또는 점수)** 값을 직접 입력/수정하면 그래프가 실시간으로 "
        "**내림차순**으로 자동 정렬돼요. 숫자가 클수록 막대가 위쪽(왼쪽)에 오도록 정렬합니다."
    )

    # 기본 데이터 (실제 등급/점수로 바꿔서 사용하세요)
    default_df = pd.DataFrame(
        {
            "과목": DEFAULT_SUBJECTS,
            "등급_또는_점수": [5, 4, 4, 3, 4, 3, 4, 3, 3, 3],
        }
    )

    edited_df = st.data_editor(
        default_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "등급_또는_점수": st.column_config.NumberColumn(
                "등급 / 점수", min_value=0, max_value=9, step=1
            )
        },
        key="grade_editor",
    )

    if edited_df.empty:
        st.warning("표에 최소 1개 이상의 과목 데이터를 입력해주세요.")
    else:
        # 이모지 붙이기
        edited_df["표시이름"] = edited_df["과목"].apply(
            lambda s: f"{EMOJI.get(s, '📘')} {s}"
        )

        # 내림차순 정렬 (값이 큰 것이 위로)
        sorted_df = edited_df.sort_values("등급_또는_점수", ascending=False)

        fig = px.bar(
            sorted_df,
            x="등급_또는_점수",
            y="표시이름",
            orientation="h",
            text="등급_또는_점수",
            color="등급_또는_점수",
            color_continuous_scale="Sunset",
        )
        fig.update_layout(
            yaxis=dict(categoryorder="total ascending"),  # 정렬된 순서대로 표시
            xaxis_title="등급 / 점수",
            yaxis_title="",
            height=520,
            coloraxis_showscale=False,
            font=dict(size=16),
            margin=dict(l=10, r=10, t=30, b=10),
        )
        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 🏆 요약")
        top = sorted_df.iloc[0]
        st.success(f"가장 높은 값: {EMOJI.get(top['과목'], '📘')} **{top['과목']}** ({top['등급_또는_점수']})")

# ============================================================================
# 슬라이드 3. 국어 - 언어와 매체
# ============================================================================
elif page == "🈶 국어 - 언어와 매체":
    st.header("🈶 국어 – 언어와 매체")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("📖 사전의 중요성")
        st.write("여남은, 들뜨다 등\n\n단어의 정확한 의미를 사전에서 직접 확인하며 학습")
    with c2:
        st.subheader("🗂️ 문법 파트별 정리")
        st.write("문법 파트별로 사례를 정리하여\n체계적으로 학습")
    with c3:
        st.subheader("✍️ 오답 사고과정 기록")
        st.write("어떤 사고 과정을 거쳐 틀렸는지\n직접 써보며 원인 분석")

# ============================================================================
# 슬라이드 4. 수학
# ============================================================================
elif page == "🔢 수학":
    st.header("🔢 수학 학습 전략")
    st.markdown(
        """
- 🧠 **문제 풀기 전 미리 과정 예상해보기**  
  (풀 수 있어도 더 간결하고 정확한 풀이가 없는지 고민)
- ⚠️ **실수 포인트 파악하기**  
  자주 실수하는 부분을 의식적으로 인지하고 줄이려 노력
- 🔖 **풀이에 인덱스 달기**  
  풀이 과정에 번호/인덱스를 달아 흐름을 명확히 정리
        """
    )
