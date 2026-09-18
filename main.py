import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 페이지 설정
# ==================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    "KOBIS 영화 데이터를 이용해 영화의 **장르, 관객 수, 스크린 수, "
    "제작 국가 등의 분포와 관계**를 다양한 그래프로 살펴봅니다."
)


# ==================================================
# 데이터 불러오기
# ==================================================
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/"
    "modudata/main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)

    # 장르: 여러 장르가 있으면 첫 번째 장르만 사용
    data["genre"] = (
        data["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        ).fillna(0)

    return data


try:
    df = load_data()

    st.success(
        f"총 {len(df):,}편의 영화 데이터를 불러왔습니다."
    )

except Exception as e:
    st.error("영화 데이터를 불러오지 못했습니다.")
    st.stop()


# ==================================================
# ① 장르별 영화 편수
# ==================================================
st.header("① 장르별 영화 편수")

st.markdown(
    "전체 영화 데이터를 장르별로 나누어 "
    "각 장르에 영화가 몇 편씩 포함되어 있는지 보여줍니다."
)

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig_genre = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig_genre.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig_genre.update_layout(
    height=600,
    margin=dict(t=70, b=30, l=20, r=20)
)

st.plotly_chart(
    fig_genre,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "전체 영화에서 어떤 장르의 영화가 많이 포함되어 있는지와 "
    "각 장르가 차지하는 비율을 확인할 수 있습니다."
)

with st.expander("📋 장르별 영화 편수 표 보기"):
    st.dataframe(
        genre_count,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# ② 장르 → 영화별 총 관객 트리맵
# ==================================================
st.header("② 장르별 영화의 총 관객 트리맵")

st.markdown(
    "장르 안에서 각각의 영화가 차지하는 **총 관객 수의 규모**를 "
    "영역의 크기로 나타냅니다."
)

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 → 영화별 총 관객 수"
)

fig_treemap.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig_treemap.update_layout(
    height=700,
    margin=dict(t=70, b=20, l=20, r=20)
)

st.plotly_chart(
    fig_treemap,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "장르별로 어떤 영화가 많은 관객을 모았는지와 "
    "영화 사이의 관객 규모 차이를 한눈에 비교할 수 있습니다."
)


# ==================================================
# ③ 총 관객 수의 분포
# ==================================================
st.header("③ 총 관객 수의 분포")

st.markdown(
    "영화들의 총 관객 수가 어느 구간에 많이 모여 있는지 "
    "히스토그램으로 확인합니다."
)

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig_hist.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig_hist.update_layout(
    height=600,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=70, b=50, l=20, r=20)
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# 가장 많이 나타난 구간 계산
hist_values = df["total_audi"]

hist_bins = pd.cut(
    hist_values,
    bins=20,
    include_lowest=True
)

bin_counts = (
    hist_bins
    .value_counts()
    .sort_index()
)

most_common_bin = bin_counts.idxmax()
most_common_count = bin_counts.max()

# 총 관객이 가장 많은 영화
max_audience_index = df["total_audi"].idxmax()
max_audience_movie = df.loc[max_audience_index]

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    f"영화의 총 관객 수는 **{most_common_bin}** 구간에 "
    f"가장 많이 분포했으며({most_common_count}편), "
    f"총 관객이 가장 많은 영화는 "
    f"**{max_audience_movie['movieNm']}**로 "
    f"{max_audience_movie['total_audi']:,.0f}명의 관객을 기록했습니다."
)


# ==================================================
# ④ 개봉일 스크린 수와 총 관객의 관계
# ==================================================
st.header("④ 개봉일 스크린 수와 총 관객의 관계")

st.markdown(
    "개봉일에 확보한 스크린 수와 영화의 총 관객 수 사이에 "
    "어떤 관계가 나타나는지 산점도로 확인합니다."
)

scatter_df = df[
    (df["first_scrn"] > 0) &
    (df["total_audi"] > 0)
].copy()

fig_scatter = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)

fig_scatter.update_traces(
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

fig_scatter.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=70, b=50, l=20, r=20)
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# 상관계수 계산
corr = scatter_df["first_scrn"].corr(
    scatter_df["total_audi"]
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    f"개봉일 스크린 수와 총 관객 수의 피어슨 상관계수는 "
    f"**{corr:.2f}**입니다. "
    "점들이 오른쪽 위 방향으로 모이는 정도를 통해 "
    "두 변수의 관계를 시각적으로 확인할 수 있습니다."
)


# ==================================================
# ⑤ 장르별 총 관객 상자 그림
# ==================================================
st.header("⑤ 장르별 총 관객 분포")

st.markdown(
    "영화가 **10편 이상인 장르**만 골라 장르별 총 관객 수의 "
    "분포를 상자 그림으로 비교합니다."
)

genre_counts = df["genre"].value_counts()

selected_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["genre"].isin(selected_genres)
].copy()

fig_box = px.box(
    box_df,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    }
)

fig_box.update_traces(
    boxpoints="outliers",
    jitter=0,
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명<br>"
        "장르: %{x}"
        "<extra></extra>"
    )
)

fig_box.update_layout(
    height=650,
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    margin=dict(t=70, b=50, l=20, r=20)
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "영화가 10편 이상인 장르를 비교하면 장르마다 총 관객 수의 "
    "중앙값과 분포의 퍼짐 정도를 확인할 수 있으며, "
    "상자 밖의 점을 통해 다른 영화들과 비교해 관객 수가 크게 다른 영화를 찾을 수 있습니다."
)

st.caption(
    "분석 대상 장르: "
    + ", ".join(selected_genres.tolist())
)


# ==================================================
# ⑥ 첫 주 관객을 크기로 나타낸 버블 그래프
# ==================================================
st.header("⑥ 첫 주 관객을 크기로 나타낸 버블 그래프")

st.markdown(
    "④번 산점도와 같은 데이터를 사용하되, "
    "**점의 크기를 첫 주 관객(first_week_audi)**으로 나타냅니다."
)

bubble_df = df[
    (df["first_scrn"] > 0) &
    (df["total_audi"] > 0) &
    (df["first_week_audi"] > 0)
].copy()

fig_bubble = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린 수 · 총 관객 · 첫 주 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    }
)

fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(
        opacity=0.7,
        line=dict(width=1)
    )
)

fig_bubble.update_layout(
    height=700,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title="장르",
    margin=dict(t=70, b=50, l=20, r=20)
)

st.plotly_chart(
    fig_bubble,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "개봉일 스크린 수와 총 관객의 관계뿐 아니라 점의 크기를 통해 "
    "첫 주에 얼마나 많은 관객이 영화를 관람했는지도 함께 비교할 수 있습니다."
)


# ==================================================
# ⑦ 제작 국가 → 장르 선버스트 그래프
# ==================================================
st.header("⑦ 제작 국가와 장르의 영화 구성")

st.markdown(
    "제작 국가에서 장르로 내려가는 구조로 영화 데이터를 표현하고, "
    "**각 칸의 크기는 영화 편수**를 나타냅니다."
)

sunburst_df = df.copy()

# 제작 국가 결측값 처리
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

# 장르 결측값 처리
sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

# 여러 국가가 | 로 구분되어 있다면 첫 번째 국가만 사용
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .str.split("|")
    .str[0]
    .str.strip()
)

fig_sunburst = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    title="제작 국가 → 장르별 영화 편수"
)

fig_sunburst.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig_sunburst.update_layout(
    height=700,
    margin=dict(t=70, b=20, l=20, r=20)
)

st.plotly_chart(
    fig_sunburst,
    use_container_width=True
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "제작 국가별로 어떤 장르의 영화가 많이 포함되어 있는지와 "
    "각 국가와 장르가 전체 영화에서 차지하는 규모를 한눈에 비교할 수 있습니다."
)
# ==================================================
# ⑧ 나만의 질문
# ==================================================
st.header("⑧ 개봉일에 상영 횟수가 많은 영화는 첫 주에도 많은 관객을 모으는가?")

st.markdown(
    "개봉일 상영 횟수와 개봉 첫 주 관객 수 사이의 관계를 "
    "산점도로 확인합니다."
)

# 분석에 필요한 값이 있는 데이터만 사용
my_question_df = df[
    (df["first_show"] > 0) &
    (df["first_week_audi"] > 0)
].copy()

fig_my_question = px.scatter(
    my_question_df,
    x="first_show",
    y="first_week_audi",
    hover_name="movieNm",
    title="개봉일에 상영 횟수가 많은 영화는 첫 주에도 많은 관객을 모으는가?",
    labels={
        "first_show": "개봉일 상영 횟수",
        "first_week_audi": "개봉 첫 주 관객 수"
    }
)

# 마우스를 올렸을 때 영화명과 수치 표시
fig_my_question.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 상영 횟수: %{x:,.0f}회<br>"
        "개봉 첫 주 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_my_question.update_layout(
    height=650,
    xaxis_title="개봉일 상영 횟수",
    yaxis_title="개봉 첫 주 관객 수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig_my_question,
    use_container_width=True
)


# 상관계수 계산
corr_my_question = my_question_df["first_show"].corr(
    my_question_df["first_week_audi"]
)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    f"개봉일 상영 횟수와 개봉 첫 주 관객 수의 "
    f"피어슨 상관계수는 **{corr_my_question:.2f}**입니다. "
    "산점도에서 점들이 어떤 방향으로 분포하는지 살펴보면서 "
    "두 변수 사이의 관계를 확인할 수 있습니다."
)
# ==================================================
# ⑧ 첫 주 관객 중 최종 관객에서 차지하는 비율은 영화마다 얼마나 다른가?
# ==================================================
st.header("⑧ 첫 주 관객 중 최종 관객에서 차지하는 비율은 영화마다 얼마나 다른가?")

st.markdown(
    "개봉 첫 주 관객 수가 최종 관객 수에서 차지하는 비율을 계산하여 "
    "영화별 분포를 히스토그램으로 확인합니다."
)

# 결측값과 0인 값 제외
df_8 = df[
    (df["first_week_audi"] > 0) &
    (df["total_audi"] > 0)
].copy()

# 첫 주 관객이 최종 관객에서 차지하는 비율 계산
df_8["first_week_ratio"] = (
    df_8["first_week_audi"] / df_8["total_audi"] * 100
)

# 100%를 초과하는 이상한 값이 있다면 제외
df_8 = df_8[
    (df_8["first_week_ratio"] >= 0) &
    (df_8["first_week_ratio"] <= 100)
]

# 히스토그램
fig_8 = px.histogram(
    df_8,
    x="first_week_ratio",
    nbins=20,
    title="첫 주 관객 비율의 분포",
    labels={
        "first_week_ratio": "첫 주 관객 비율(%)",
        "count": "영화 편수"
    }
)

fig_8.update_traces(
    hovertemplate=(
        "첫 주 관객 비율: %{x:.1f}%<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig_8.update_layout(
    height=650,
    xaxis_title="첫 주 관객 비율(%)",
    yaxis_title="영화 편수",
    margin=dict(t=80, b=50, l=20, r=20)
)

st.plotly_chart(
    fig_8,
    use_container_width=True
)

# ==================================================
# 그래프 해석
# ==================================================
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")

median_ratio = df_8["first_week_ratio"].median()

st.info(
    f"영화별 첫 주 관객 비율의 중앙값은 **{median_ratio:.1f}%**입니다. "
    "히스토그램을 통해 첫 주 관객이 최종 관객의 어느 정도를 차지하는 영화가 "
    "많은지 확인할 수 있습니다. "
    "첫 주 관객 비율이 높을수록 영화의 흥행이 개봉 초기에 집중되었음을 의미하고, "
    "낮을수록 첫 주 이후에도 관객이 계속 유입되었음을 의미합니다."
)
