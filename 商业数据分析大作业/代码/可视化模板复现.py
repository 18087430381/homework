import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from math import pi
import platform
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 强行加载系统字体
font_path = r'C:\Windows\Fonts\msyh.ttc' 
my_font = FontProperties(fname=font_path, size=14)
plt.rcParams['font.family'] = my_font.get_name() # 让全局使用这个字体
plt.rcParams['axes.unicode_minus'] = False

# 自动创建 figures 文件夹（防止保存报错）
os.makedirs('figures', exist_ok=True)

# 准备数据
df_business = pd.read_csv('data/clean/clean_business.csv')
df_review = pd.read_csv('data/clean/clean_review.csv')
df_merged = pd.merge(df_review, df_business[['business_id', 'city', 'categories']], on='business_id', how='inner')

print("正在生成 11 种可视化模板...")

# -------------------------------------------------------------------
# 模板 1：基础柱状图
plt.figure(figsize=(6, 4))
stars_counts = df_review['stars'].value_counts().sort_index()
bars = plt.bar(stars_counts.index, stars_counts.values, color='#4C72B0')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, int(bar.get_height()), ha='center')
plt.title('模板1: 评论星级分布柱状图', fontsize=14)
plt.xlabel('星级')
plt.ylabel('评论数量')
plt.savefig('figures/tpl01_柱状图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 2：水平条形图
plt.figure(figsize=(6, 4))
top_cities = df_business['city'].value_counts().head(5)
sns.barplot(x=top_cities.values, y=top_cities.index, palette='Blues_r')
plt.title('模板2: Top 5 城市商家数量', fontsize=14)
plt.savefig('figures/tpl02_水平条形图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 3：多折线图
plt.figure(figsize=(8, 4))
pivot_df = df_merged[df_merged['city'].isin(top_cities.index)].pivot_table(index='city', columns='stars', values='review_id', aggfunc='count').fillna(0)
sns.lineplot(data=pivot_df.T, dashes=False, markers=True)
plt.title('模板3: 各城市星级评论趋势', fontsize=14)
plt.legend(title='星级', bbox_to_anchor=(1, 1))
plt.savefig('figures/tpl03_多折线图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 4：饼图
plt.figure(figsize=(6, 6))
top_cats = df_business['categories'].dropna().str.split(',').str[0].value_counts().head(5)
plt.pie(top_cats.values, labels=top_cats.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('模板4: 头部商家类别占比饼图', fontsize=14)
plt.savefig('figures/tpl04_饼图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 5：直方图
plt.figure(figsize=(6, 4))
sns.histplot(df_business['review_count'], bins=20, kde=True, color='#55A868')
plt.xlim(0, 400)
plt.title('模板5: 商家评论数分布直方图', fontsize=14)
plt.xlabel('评论数')
plt.ylabel('商家频数')
plt.savefig('figures/tpl05_直方图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 6：散点图
plt.figure(figsize=(6, 4))
sns.scatterplot(data=df_business, x='stars', y='review_count', color='#C44E52', alpha=0.6)
plt.title('模板6: 星级与评论数散点图', fontsize=14)
plt.xlabel('星级')
plt.ylabel('评论数')
plt.savefig('figures/tpl06_散点图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 7：箱线图
plt.figure(figsize=(8, 4))
sns.boxplot(data=df_business[df_business['city'].isin(top_cities.index)], x='city', y='stars', palette='Set2')
plt.title('模板7: 各城市商家星级箱线图', fontsize=14)
plt.savefig('figures/tpl07_箱线图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 8：热力图
plt.figure(figsize=(6, 5))
corr = df_business[['stars', 'review_count', 'is_open']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('模板8: 商家指标相关性热力图', fontsize=14)
plt.savefig('figures/tpl08_热力图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 9：气泡图
plt.figure(figsize=(6, 4))
sns.scatterplot(data=df_business, x='stars', y='review_count', size='review_count', sizes=(20, 300), alpha=0.5, color='purple')
plt.title('模板9: 气泡图 (大小代表评论数)', fontsize=14)
plt.xlabel('星级')
plt.ylabel('评论数')
plt.savefig('figures/tpl09_气泡图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 10：堆叠柱状图
plt.figure(figsize=(8, 5))
pivot_count = df_merged[df_merged['city'].isin(top_cities.index)].pivot_table(index='city', columns='stars', values='review_id', aggfunc='count').fillna(0)
pivot_count.plot(kind='bar', stacked=True, colormap='viridis', ax=plt.gca())
plt.title('模板10: 城市评论星级堆叠柱状图', fontsize=14)
plt.ylabel('评论数')
plt.savefig('figures/tpl10_堆叠柱状图.png', dpi=200, bbox_inches='tight'); plt.close()

# -------------------------------------------------------------------
# 模板 11：雷达图
plt.figure(figsize=(6, 6))
city_stats = df_business.groupby('city').agg({'stars': 'mean', 'review_count': 'mean', 'business_id': 'count'}).head(3)
city_stats_norm = (city_stats - city_stats.min()) / (city_stats.max() - city_stats.min())
categories = ['平均星级', '平均评论数', '商家规模']
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
ax = plt.subplot(111, polar=True)
for idx, row in city_stats_norm.iterrows():
    values = row.tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, label=idx)
    ax.fill(angles, values, alpha=0.1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
plt.title('模板11: 头部城市多维雷达图', fontsize=14)
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
plt.savefig('figures/tpl11_雷达图.png', dpi=200, bbox_inches='tight'); plt.close()

print("✅ 11 种模板全部生成完毕！请在 figures 文件夹中查看 tpl01 到 tpl11 的图片。")
