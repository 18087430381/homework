import pandas as pd
import os

clean_dir = 'data/clean/'

print("开始进行多表关联构建宽表...")

# 1. 读取需要关联的两张表
df_business = pd.read_csv(f'{clean_dir}clean_business.csv')
df_review = pd.read_csv(f'{clean_dir}clean_review.csv')

# 2. 先对评论表进行聚合（防止一个商户有多条评论导致合并后行数爆炸）
# 我们计算每个商家的【实际评论数】和【平均星级】
review_agg = df_review.groupby('business_id').agg(
    actual_review_count=('review_id', 'count'),
    avg_review_stars=('stars', 'mean')
).reset_index()

print(f"聚合后的评论表行数：{len(review_agg)} 行（每个商户只有一行）")

# 3. 将聚合后的评论数据与商户表关联 (LEFT JOIN)
# 使用 business_id 作为主外键
df_merged = pd.merge(df_business, review_agg, on='business_id', how='left')

# 4. 处理关联后产生的 NaN 值（有些商户可能在这 500 条评论里没被评论过）
df_merged['actual_review_count'] = df_merged['actual_review_count'].fillna(0)
df_merged['avg_review_stars'] = df_merged['avg_review_stars'].fillna(df_merged['stars']) # 用官方星级填补

# 5. 保存这张“超级宽表”，后面做 Streamlit 大屏就靠它了！
df_merged.to_csv(f'{clean_dir}clean_merged_data.csv', index=False, encoding='utf-8-sig')

print("✅ 多表关联完成！")
print(f"关联后的宽表行数：{len(df_merged)} 行（说明没有发生行数爆炸，完美对齐）")
print("\n预览一下合并后的核心列：")
print(df_merged[['business_id', 'name', 'city', 'stars', 'actual_review_count', 'avg_review_stars']].head())
