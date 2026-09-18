import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# 기본 설정
# ==================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2")
st.markdown("### 분포와 관계")
st.markdown(
    "영화 데이터를 여러 가지 그래프로 표현하고, "
    "각 그래프에서 직접 의미를 찾아봅니다."
)

# ==================================================
# 데이터 불러오기
# ==================================================
CSV_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

try:
    df = pd.read_csv(CSV_URL)
except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.stop()

# ==================================================
# 데이터 전처리
# ==================================================

# 숫자형으로 변환
numeric_cols = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    ).fillna(0)

# 장르 정리
df["genre"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 국가 정리
df["nation"] = (
    df["nation"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# ==================================================
# ① 장르별 영화 편수
# ==================================================
st.header("① 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=600,
    margin=dict(t=80, b=30, l=20, r=20)
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 가장 많은 비율을 차지하는 장르는 ○○이고, 가장 적은 장르는 ○○이다.",
    height=120,
    key="answer1"
)


# ==================================================
# ② 장르별 영화의 총 관객 트리맵
# ==================================================
st.header("② 장르별 영화의 총 관객 트리맵")

treemap_df = df[
    df["total_audi"] > 0
].copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 안에서 어떤 영화가 큰 관객을 모았나",
    color="total_audi",
    hover_data={
        "total_audi": ":,"
    }
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=700,
    margin=dict(t=80, b=20, l=20, r=20)
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 같은 장르에 속한 영화라도 총 관객 수에 큰 차이가 나타난다.",
    height=120,
    key="answer2"
)


# ==================================================
# ③ 총 관객 수의 분포
# ==================================================
st.header("③ 총 관객 수의 분포")

hist_df = df[
    df["total_audi"] > 0
].copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화 대부분은 관객이 몇 명쯤인가?",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 수: %{x:,.0f}명<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=650,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 대부분의 영화가 ○○명 이하 구간에 집중되어 있다.",
    height=120,
    key="answer3"
)


# ==================================================
# ④ 개봉일 스크린 수와 총 관객의 관계
# ==================================================
st.header("④ 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    (df["first_scrn"] > 0) &
    (df["total_audi"] > 0)
].copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="스크린을 많이 받은 영화가 관객도 많나?",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수"
    }
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 스크린 수가 증가할수록 총 관객 수도 증가하는 경향이 나타난다.",
    height=120,
    key="answer4"
)


# ==================================================
# ⑤ 장르별 총 관객 분포
# ==================================================
st.header("⑤ 장르별 총 관객 분포")

box_df = df[
    (df["total_audi"] > 0)
].copy()

# 영화 수가 너무 적은 장르는 제외
genre_valid = (
    box_df["genre"]
    .value_counts()
)

valid_genres = genre_valid[
    genre_valid >= 10
].index

box_df = box_df[
    box_df["genre"].isin(valid_genres)
]

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    title="장르별 관객 분포는 어떻게 다른가?",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{x}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    showlegend=False,
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 장르에 따라 총 관객 수의 분포와 범위가 다르게 나타난다.",
    height=120,
    key="answer5"
)


# ==================================================
# ⑥ 첫 주 관객을 크기로 나타낸 버블 그래프
# ==================================================
st.header("⑥ 첫 주 관객까지 넣으면 무엇이 더 보이나?")

bubble_df = df[
    (df["first_scrn"] > 0) &
    (df["total_audi"] > 0) &
    (df["first_week_audi"] > 0)
].copy()

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    title="스크린 수와 총 관객, 첫 주 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "개봉 첫 주 관객 수"
    },
    size_max=45
)

fig6.update_traces(
    marker=dict(
        opacity=0.70
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=700,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 같은 스크린 수를 가진 영화라도 첫 주 관객 수에는 차이가 나타난다.",
    height=120,
    key="answer6"
)


# ==================================================
# ⑦ 제작 국가와 장르의 영화 구성
# ==================================================
st.header("⑦ 국가에서 장르로 내려가면 무엇이 보이나?")

sunburst_df = df.copy()

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    title="제작 국가 → 장르별 영화 구성",
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=700,
    margin=dict(t=80, b=20, l=20, r=20)
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder="예: 국가별 영화 수의 규모와 그 안에서 장르가 차지하는 구성을 비교할 수 있다.",
    height=120,
    key="answer7"
)


# ==================================================
# ⑧ 첫 주 관객 비율
# ==================================================
st.header("⑧ 첫 주 관객 중 최종 관객에서 차지하는 비율은 영화마다 얼마나 다른가?")

st.markdown(
    "개봉 첫 주 관객 수가 최종 관객 수에서 차지하는 비율을 계산하여 "
    "영화별 분포를 확인합니다."
)

ratio_df = df[
    (df["first_week_audi"] > 0) &
    (df["total_audi"] > 0)
].copy()

# 첫 주 관객 비율 계산
ratio_df["first_week_ratio"] = (
    ratio_df["first_week_audi"]
    / ratio_df["total_audi"]
    * 100
)

# 정상 범위만 사용
ratio_df = ratio_df[
    (ratio_df["first_week_ratio"] >= 0) &
    (ratio_df["first_week_ratio"] <= 100)
].copy()

fig8 = px.histogram(
    ratio_df,
    x="first_week_ratio",
    nbins=20,
    title="첫 주 관객 비율의 분포",
    labels={
        "first_week_ratio": "첫 주 관객 비율(%)",
        "count": "영화 편수"
    }
)

fig8.update_traces(
    hovertemplate=(
        "첫 주 관객 비율: %{x:.1f}%<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig8.update_layout(
    height=650,
    xaxis_title="첫 주 관객 비율(%)",
    yaxis_title="영화 편수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 점을 직접 작성해 보세요.",
    placeholder=(
        "예: 대부분의 영화는 첫 주 관객 비율이 ○○~○○% 구간에 "
        "분포한다. 이를 통해 영화의 흥행이 개봉 초기에 얼마나 "
        "집중되는지 확인할 수 있었다."
    ),
    height=130,
    key="answer8"
)

# --------------------------------------------------
# ⑧ 그래프가 잘 나타나지 않은 원인
# --------------------------------------------------
st.subheader("🔎 그래프가 잘 나타나지 않은 원인은 무엇일까?")

st.text_area(
    "그래프의 모양이나 분포에 영향을 준 원인을 직접 작성해 보세요.",
    placeholder=(
        "예: 영화마다 첫 주 관객 수와 총 관객 수의 차이가 크기 때문에 "
        "비율이 특정 구간에 집중되어 나타난 것 같다."
    ),
    height=150,
    key="reason8"
)

# ==================================================
# 계산 방법
# ==================================================
st.markdown("---")
st.subheader("📌 ⑧번 그래프의 계산 방법")

st.latex(
    r"\text{첫 주 관객 비율(\%)}"
    r"="
    r"\frac{\text{개봉 첫 주 관객 수}}{\text{총 관객 수}}"
    r"\times 100"
)

st.caption(
    "첫 주 관객 비율은 전체 관객 중 개봉 첫 주에 관람한 관객이 차지하는 비율입니다."
)

# ==================================================
# 마무리
# ==================================================
st.markdown("---")
st.success(
    "🎬 모든 그래프의 분석 내용을 직접 작성해 보세요. "
    "그래프의 모양과 데이터의 특징을 근거로 자신의 생각을 정리하면 됩니다."
)
