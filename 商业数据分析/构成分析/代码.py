import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 构建数据（模拟Excel中的RANDBETWEEN公式结果）
# ============================================================
np.random.seed(42)

# 第一部分：产品销量（单期）
products_1 = ['产品1', '产品2', '产品3', '产品4']
sales_1 = [
    np.random.randint(100, 201),   # 产品1: 100-200
    np.random.randint(100, 501),   # 产品2: 100-500
    np.random.randint(100, 501),   # 产品3: 100-500
    np.random.randint(400, 801),   # 产品4: 400-800
]
df_part1 = pd.DataFrame({'产品类型': products_1, '销售量': sales_1})

# 第二部分：近5年产品销量统计（表1）
years = [2020, 2021, 2022, 2023, 2024]
products_2 = ['产品1', '产品2', '产品3']
data_table1 = {p: [np.random.randint(200, 501) for _ in years] for p in products_2}
df_table1 = pd.DataFrame(data_table1, index=years)

# 第三部分：近5年产品销量统计（表2，不同区间）
data_table2 = {
    '产品1': [np.random.randint(100, 201) for _ in years],
    '产品2': [np.random.randint(200, 301) for _ in years],
    '产品3': [np.random.randint(400, 501) for _ in years],
}
df_table2 = pd.DataFrame(data_table2, index=years)

# ============================================================
# 2. 输出数据结果
# ============================================================
print("=" * 60)
print("【第一部分】产品销量（单期）")
print("=" * 60)
print(df_part1.to_string(index=False))

total_1 = df_part1['销售量'].sum()
df_part1['占比'] = df_part1['销售量'] / total_1
df_part1['累计占比'] = df_part1['占比'].cumsum()
print("\n占比分析：")
for _, row in df_part1.iterrows():
    print(f"  {row['产品类型']}: 销量={row['销售量']:>4d}, 占比={row['占比']:.2%}, 累计占比={row['累计占比']:.2%}")

print("\n" + "=" * 60)
print("【第二部分】近5年产品销量统计（表1：200-500区间）")
print("=" * 60)
print(df_table1.to_string())

print("\n各产品5年合计与占比：")
totals_1 = df_table1.sum()
for p in products_2:
    print(f"  {p}: 合计={totals_1[p]:>4d}, 占比={totals_1[p]/totals_1.sum():.2%}")

print("\n" + "=" * 60)
print("【第三部分】近5年产品销量统计（表2：差异化区间）")
print("=" * 60)
print(df_table2.to_string())

print("\n各产品5年合计与占比：")
totals_2 = df_table2.sum()
for p in products_2:
    print(f"  {p}: 合计={totals_2[p]:>4d}, 占比={totals_2[p]/totals_2.sum():.2%}")

# ============================================================
# 3. 可视化
# ============================================================
fig = plt.figure(figsize=(18, 14))
fig.suptitle('产品销量构成分析', fontsize=18, fontweight='bold', y=0.98)

colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']

# ---------- 图1：产品销量柱状图 + 饼图 ----------
ax1 = fig.add_subplot(2, 3, 1)
bars = ax1.bar(df_part1['产品类型'], df_part1['销售量'], color=colors)
ax1.set_title('产品销量对比（单期）', fontsize=13)
ax1.set_ylabel('销售量')
for bar, val in zip(bars, df_part1['销售量']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(val), ha='center', va='bottom', fontsize=10)

ax2 = fig.add_subplot(2, 3, 2)
ax2.pie(df_part1['销售量'], labels=df_part1['产品类型'], autopct='%1.1f%%',
        colors=colors, startangle=90, explode=[0.02]*4)
ax2.set_title('产品销量占比', fontsize=13)

# ---------- 图2：帕累托图（占比和量） ----------
ax3 = fig.add_subplot(2, 3, 3)
df_sorted = df_part1.sort_values('销售量', ascending=False).reset_index(drop=True)
df_sorted['累计占比'] = df_sorted['销售量'].cumsum() / df_sorted['销售量'].sum()

ax3.bar(df_sorted['产品类型'], df_sorted['销售量'], color=colors, alpha=0.8)
ax3.set_ylabel('销售量', color='#4C72B0')
ax3.tick_params(axis='y', labelcolor='#4C72B0')

ax3_twin = ax3.twinx()
ax3_twin.plot(df_sorted['产品类型'], df_sorted['累计占比'] * 100,
              color='red', marker='o', linewidth=2)
ax3_twin.set_ylabel('累计占比 (%)', color='red')
ax3_twin.tick_params(axis='y', labelcolor='red')
ax3_twin.set_ylim(0, 110)
ax3.set_title('帕累托图（销量+累计占比）', fontsize=13)

# ---------- 图3：近5年产品销量趋势（表1） ----------
ax4 = fig.add_subplot(2, 3, 4)
for i, p in enumerate(products_2):
    ax4.plot(years, df_table1[p], marker='o', label=p, color=colors[i], linewidth=2)
ax4.set_title('近5年产品销量趋势（表1）', fontsize=13)
ax4.set_xlabel('年份')
ax4.set_ylabel('销售量')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xticks(years)

# ---------- 图4：近5年产品销量趋势（表2） ----------
ax5 = fig.add_subplot(2, 3, 5)
for i, p in enumerate(products_2):
    ax5.plot(years, df_table2[p], marker='s', label=p, color=colors[i], linewidth=2, linestyle='--')
ax5.set_title('近5年产品销量趋势（表2）', fontsize=13)
ax5.set_xlabel('年份')
ax5.set_ylabel('销售量')
ax5.legend()
ax5.grid(True, alpha=0.3)
ax5.set_xticks(years)

# ---------- 图5：5年合计占比对比（表1 vs 表2） ----------
ax6 = fig.add_subplot(2, 3, 6)
x = np.arange(len(products_2))
width = 0.35

bars1 = ax6.bar(x - width/2, totals_1.values, width, label='表1（区间200-500）', color='#4C72B0')
bars2 = ax6.bar(x + width/2, totals_2.values, width, label='表2（差异化区间）', color='#DD8452')
ax6.set_xticks(x)
ax6.set_xticklabels(products_2)
ax6.set_ylabel('5年合计销量')
ax6.set_title('5年合计销量对比（表1 vs 表2）', fontsize=13)
ax6.legend()

for bar in bars1:
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('产品销量构成分析.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n图片已保存为：产品销量构成分析.png")
