import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取清洗好的签到数据
df_checkin = pd.read_csv('data/clean/clean_checkin.csv')

# 2. 统计每个小时的签到总次数
# 按小时分组，计算频数
hourly_checkins = df_checkin.groupby('hour').size().reset_index(name='checkin_count')

# 3. 画图：折线图 + 渐变面积图
plt.figure(figsize=(12, 6))

# 画折线
sns.lineplot(data=hourly_checkins, x='hour', y='checkin_count', marker='o', color='#d62728', linewidth=2.5)

# 画渐变填充
plt.fill_between(hourly_checkins['hour'], hourly_checkins['checkin_count'], color='#d62728', alpha=0.15)

# 设置 X 轴刻度（0-23小时）
plt.xticks(range(0, 24))

# 添加标题和标签
plt.title('Yelp 商家全天签到热度分布 (24小时)', fontsize=16, fontweight='bold')
plt.xlabel('一天中的时段 (0 - 23 时)', fontsize=12)
plt.ylabel('签到总次数', fontsize=12)

# 找到最高峰的时刻
peak_hour = hourly_checkins.loc[hourly_checkins['checkin_count'].idxmax(), 'hour']
peak_count = hourly_checkins['checkin_count'].max()

# 在图上标出最高峰
plt.annotate(f'客流最高峰: {int(peak_hour)}点\n({peak_count}次)', 
             xy=(peak_hour, peak_count), 
             xytext=(peak_hour+2, peak_count+10),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=12, color='black', weight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# 保存图片
plt.savefig('fig06_签到时段热力图.png', dpi=150)
plt.show()

print(f"✅ 签到时段图已生成！商业结论：Yelp 商家的签到最高峰出现在 {int(peak_hour)} 点。")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 强行加载系统字体
font_path = r'C:\Windows\Fonts\msyh.ttc' 
my_font = FontProperties(fname=font_path, size=14)
plt.rcParams['font.family'] = my_font.get_name() # 让全局使用这个字体
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("正在读取数据并进行多表关联...")

# 1. 读取数据
df_checkin = pd.read_csv('data/clean/clean_checkin.csv')
df_business = pd.read_csv('data/clean/clean_business.csv')

# 2. 多表关联 (Checkin LEFT JOIN Business)
df_checkin_merged = pd.merge(df_checkin, df_business[['business_id', 'categories']], on='business_id', how='left')

# 3. 数据清洗：提取主类别（为了防止类别太多，我们只取最核心的 3 个行业）
df_checkin_merged = df_checkin_merged.dropna(subset=['categories'])
df_checkin_merged['main_category'] = df_checkin_merged['categories'].apply(lambda x: str(x).split(',')[0].strip())

# 挑出平台最常见的 3 个行业进行对比
top_3_cats = df_checkin_merged['main_category'].value_counts().head(3).index.tolist()
df_filtered = df_checkin_merged[df_checkin_merged['main_category'].isin(top_3_cats)]

# 4. 统计不同类别在不同小时的签到量（准备画折线图）
hourly_cat = df_filtered.groupby(['main_category', 'hour']).size().reset_index(name='checkin_count')

# 5. 画图：多折线对比图（这就是教材里经典的“多系列折线图”模板）
plt.figure(figsize=(12, 6))

# 用 Seaborn 画出不同类别的折线
sns.lineplot(data=hourly_cat, x='hour', y='checkin_count', hue='main_category', marker='o', linewidth=2.5, palette='Set1')

plt.title('不同行业商家的 24 小时签到热度对比 (多表关联)', fontsize=16, fontweight='bold')
plt.xlabel('一天中的时段 (0 - 23 时)', fontsize=12)
plt.ylabel('签到次数', fontsize=12)
plt.xticks(range(0, 24))
plt.legend(title='商家主类别', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# 保存图片（这就是你的 fig06_进阶签到热力图.png）
plt.savefig('fig06_进阶签到热力图.png', dpi=150)
plt.show()

print(f"✅ 多表关联折线图已生成！参与的对比类别包括：{top_3_cats}")
