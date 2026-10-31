import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取清洗后的商家数据
df_business = pd.read_csv('data/clean/clean_business.csv')

# 2. 按评论数降序排列
df_pareto = df_business.sort_values(by='review_count', ascending=False).reset_index(drop=True)

# 3. 计算累计占比
total_reviews = df_pareto['review_count'].sum()
df_pareto['cum_review'] = df_pareto['review_count'].cumsum()
df_pareto['cum_percent'] = df_pareto['cum_review'] / total_reviews

# 4. 画帕累托图（柱状图 + 折线图双轴）
fig, ax1 = plt.subplots(figsize=(10, 6))

# 柱状图：各个商家的评论数
ax1.bar(range(len(df_pareto)), df_pareto['review_count'], color='skyblue', label='单店评论数')
ax1.set_xlabel('商家排名（按评论数降序）', fontsize=12)
ax1.set_ylabel('评论数', fontsize=12, color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

# 折线图：累计百分比
ax2 = ax1.twinx()
ax2.plot(range(len(df_pareto)), df_pareto['cum_percent'], color='red', marker='o', markersize=2, linestyle='-', label='累计占比')
ax2.set_ylabel('累计百分比', fontsize=12, color='red')
ax2.tick_params(axis='y', labelcolor='red')

# 画 80% 阈值线
ax2.axhline(0.8, color='gray', linestyle='--')
ax2.text(len(df_pareto)*0.5, 0.82, '80% 阈值线', color='gray')

plt.title('Yelp 头部商家帕累托分析（二八定律）', fontsize=16)
plt.tight_layout()

# 保存图片（这就是你的 fig02_帕累托图.png）
plt.savefig('fig02_帕累托图.png', dpi=150)
plt.show()

# 5. 计算前 20% 的商家占据了多少评论
top_20_index = int(len(df_pareto) * 0.2)
top_20_percent = df_pareto.loc[top_20_index, 'cum_percent']
print(f"✅ 商业结论：排名前 20% 的商家，占据了约 {top_20_percent*100:.1f}% 的评论量。")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("正在读取多表关联数据并计算类别帕累托...")

# 1. 读取原始表（体现多表关联过程）
df_business = pd.read_csv('data/clean/clean_business.csv')
df_review = pd.read_csv('data/clean/clean_review.csv')

# 2. 核心：多表关联 (Merge)
# 我们只取商户表的类别字段，关联到评论表上
# 为了防止行数爆炸，评论表先按商户 ID 聚合
review_agg = df_review.groupby('business_id').size().reset_index(name='actual_reviews')
df_merged = pd.merge(review_agg, df_business[['business_id', 'categories']], on='business_id', how='inner')

# 3. 数据清洗：很多商家的类别是 "A, B, C" 的格式，且有缺失值
df_merged = df_merged.dropna(subset=['categories'])
# 取第一个主类别（比如 "Restaurants, Food" 我们只取 "Restaurants"）
df_merged['main_category'] = df_merged['categories'].apply(lambda x: str(x).split(',')[0].strip())

# 4. 按主类别汇总评论数，并按降序排列（准备画帕累托图）
cat_reviews = df_merged.groupby('main_category')['actual_reviews'].sum().sort_values(ascending=False).reset_index()

# 5. 计算累计百分比
total_reviews = cat_reviews['actual_reviews'].sum()
cat_reviews['cum_review'] = cat_reviews['actual_reviews'].cumsum()
cat_reviews['cum_percent'] = cat_reviews['cum_review'] / total_reviews

# 为了图表美观，我们只取前 20 个主类别画图
plot_data = cat_reviews.head(20).copy()

# 6. 绘制帕累托图（柱状 + 折线双轴）
fig, ax1 = plt.subplots(figsize=(12, 6))

# 柱状图
ax1.bar(plot_data['main_category'], plot_data['actual_reviews'], color='#4C72B0', alpha=0.8, label='类目评论总数')
ax1.set_xlabel('商家主类别 (Top 20)', fontsize=12)
ax1.set_ylabel('评论数量', fontsize=12, color='#4C72B0')
ax1.tick_params(axis='x', rotation=45) # 横轴标签旋转
ax1.tick_params(axis='y', labelcolor='#4C72B0')

# 折线图（累计百分比）
ax2 = ax1.twinx()
ax2.plot(plot_data['main_category'], plot_data['cum_percent'], color='#C44E52', marker='o', markersize=5, linewidth=2, label='累计百分比')
ax2.set_ylabel('累计百分比', fontsize=12, color='#C44E52')
ax2.tick_params(axis='y', labelcolor='#C44E52')
ax2.set_ylim(0, 1.1) # 限制Y轴 0-1

# 画 80% 阈值线
ax2.axhline(0.8, color='gray', linestyle='--', linewidth=1.5)
ax2.text(len(plot_data)-1, 0.82, '80% 阈值线', color='gray', ha='right')

plt.title('Yelp 不同商家类别流量贡献帕累托分析 (基于多表关联)', fontsize=16, fontweight='bold')
plt.tight_layout()

# 保存图片
plt.savefig('fig13_类别帕累托图.png', dpi=150, bbox_inches='tight')
plt.show()

# 7. 打印商业结论
top_cat = plot_data.iloc[0]['main_category']
top_cat_reviews = plot_data.iloc[0]['actual_reviews']
print(f"\n✅ 商业结论：在关联后的数据中，流量最大的主类别是【{top_cat}】，共产生 {top_cat_reviews} 条评论。")
