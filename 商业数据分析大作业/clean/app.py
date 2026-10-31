import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 网页基础设置
st.set_page_config(page_title="Yelp商业数据大屏", layout="wide")
st.title("📊 Yelp 商户运营与用户价值分析大屏")
st.markdown("---")

# 2. 读取数据
@st.cache_data
def load_data():
    # 读取你之前关联好的多表宽表
    df = pd.read_csv('data/clean/clean_merged_data.csv')
    return df

df = load_data()

# 3. 侧边栏筛选器（交互联动）
st.sidebar.header("⚙️ 数据筛选")
# 让用户选择城市
cities = df['city'].dropna().unique().tolist()
selected_city = st.sidebar.multiselect("选择城市 (City)", cities, default=cities[:3])

# 根据用户选择过滤数据
if selected_city:
    filtered_df = df[df['city'].isin(selected_city)]
else:
    filtered_df = df

# 4. 顶部 KPI 指标卡
col1, col2, col3 = st.columns(3)
col1.metric("当前商户总数", f"{len(filtered_df)} 家")
col2.metric("平均星级", f"{filtered_df['stars'].mean():.2f} ⭐")
col3.metric("累计评论数", f"{filtered_df['review_count'].sum():,} 条")

st.markdown("---")

# 5. 图表展示区（左右两列）
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📍 城市商户分布 (Top 10)")
    # 统计筛选后各城市商户数
    city_counts = filtered_df['city'].value_counts().head(10).reset_index()
    city_counts.columns = ['城市', '商户数']
    fig_bar = px.bar(city_counts, x='城市', y='商户数', color='商户数', color_continuous_scale='Blues')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("📈 商户星级与评论数关系")
    # 散点图
    fig_scatter = px.scatter(filtered_df, x='stars', y='review_count', 
                             size='review_count', color='city', 
                             hover_name='name', labels={'stars': '星级', 'review_count': '评论数'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# 6. 数据明细表
st.subheader("📋 商户数据明细表")
st.dataframe(filtered_df[['name', 'city', 'stars', 'review_count', 'categories']].head(50), use_container_width=True)
