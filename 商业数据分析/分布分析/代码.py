import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 1. 读取数据 ============
file_path = '3分布分析-参考.xlsx'
df = pd.read_excel(file_path, sheet_name='分布分析', header=None)

# 客单价数据在 U 列（第20列，索引20），从第2行（索引1）到第339行
# 但表头 U1 是"客单价"，数据从 U2 开始
order_values = pd.to_numeric(df.iloc[1:339, 20], errors='coerce').dropna()

# 年龄数据在 L 列（索引11），K列为用户id
age_values = pd.to_numeric(df.iloc[1:339, 11], errors='coerce').dropna()

# 门店客流量数据在 C 列（索引2），时点在 B 列（索引1）
traffic_values = pd.to_numeric(df.iloc[1:50, 2], errors='coerce').dropna()

print("=" * 60)
print("数据概况")
print("=" * 60)
print(f"客单价样本数: {len(order_values)}")
print(f"年龄样本数: {len(age_values)}")
print(f"客流量样本数: {len(traffic_values)}")

# ============ 2. 客单价描述性统计（5数概括 + IQR） ============
print("\n" + "=" * 60)
print("客单价描述性统计")
print("=" * 60)

mean_val = order_values.mean()
q0 = order_values.quantile(0)      # min
q1 = order_values.quantile(0.25)   # Q1
q2 = order_values.quantile(0.50)   # 中位数
q3 = order_values.quantile(0.75)   # Q3
q4 = order_values.quantile(1.0)    # max
iqr = q3 - q1
upper_limit = q3 + 1.5 * iqr
lower_limit = q1 - 1.5 * iqr

print(f"均值 (mean)         : {mean_val:.4f}")
print(f"最小值 (min)        : {q0:.4f}")
print(f"25% 分位数 (Q1)     : {q1:.4f}")
print(f"中位数 (median)     : {q2:.4f}")
print(f"75% 分位数 (Q3)     : {q3:.4f}")
print(f"最大值 (max)        : {q4:.4f}")
print(f"IQR (Q3-Q1)         : {iqr:.4f}")
print(f"上限 (Q3+1.5*IQR)   : {upper_limit:.4f}")
print(f"下限 (Q1-1.5*IQR)   : {lower_limit:.4f}")

# 异常值检测
outliers = order_values[(order_values > upper_limit) | (order_values < lower_limit)]
print(f"\n异常值数量: {len(outliers)}")
if len(outliers) > 0:
    print(f"异常值: {outliers.values.tolist()}")

# ============ 3. 年龄分布 ============
print("\n" + "=" * 60)
print("年龄分布统计")
print("=" * 60)
print(age_values.describe())

# 年龄分组
bins = [0, 18, 25, 35, 45, 55, 65, 100]
labels = ['<18', '18-25', '26-35', '36-45', '46-55', '56-65', '>65']
age_groups = pd.cut(age_values, bins=bins, labels=labels)
age_counts = age_groups.value_counts().sort_index()
print("\n年龄分组分布:")
print(age_counts)

# ============ 4. 客流量分布 ============
print("\n" + "=" * 60)
print("门店客流量统计")
print("=" * 60)
print(traffic_values.describe())

# ============ 5. 可视化 ============
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 5.1 客单价箱线图
ax1 = axes[0, 0]
bp = ax1.boxplot(order_values, vert=True, patch_artist=True, widths=0.5)
bp['boxes'][0].set_facecolor('#4C72B0')
bp['boxes'][0].set_alpha(0.7)
ax1.axhline(upper_limit, color='red', linestyle='--', linewidth=1, label=f'上限={upper_limit:.1f}')
ax1.set_title('客单价箱线图', fontsize=12)
ax1.set_ylabel('客单价')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 5.2 客单价直方图
ax2 = axes[0, 1]
ax2.hist(order_values, bins=30, color='#4C72B0', edgecolor='white', alpha=0.8)
ax2.axvline(mean_val, color='red', linestyle='--', label=f'均值={mean_val:.1f}')
ax2.axvline(q2, color='green', linestyle='--', label=f'中位数={q2:.1f}')
ax2.set_title('客单价分布直方图', fontsize=12)
ax2.set_xlabel('客单价')
ax2.set_ylabel('频数')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 5.3 年龄分布
ax3 = axes[1, 0]
age_counts.plot(kind='bar', ax=ax3, color='#DD8452', edgecolor='white', alpha=0.85)
ax3.set_title('用户年龄分组分布', fontsize=12)
ax3.set_xlabel('年龄区间')
ax3.set_ylabel('人数')
ax3.tick_params(axis='x', rotation=45)
for i, v in enumerate(age_counts.values):
    ax3.text(i, v + 0.5, str(v), ha='center', fontsize=9)
ax3.grid(axis='y', alpha=0.3)

# 5.4 门店客流量时序
ax4 = axes[1, 1]
ax4.plot(range(len(traffic_values)), traffic_values.values, color='#55A868', linewidth=1.5)
ax4.axhline(traffic_values.mean(), color='red', linestyle='--', linewidth=1,
            label=f'均值={traffic_values.mean():.1f}')
ax4.set_title('门店客流量时序图（2020-01-01）', fontsize=12)
ax4.set_xlabel('时段序号')
ax4.set_ylabel('客流量')
ax4.legend()
ax4.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('分布分析结果.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n图片已保存为: 分布分析结果.png")

# ============ 6. 输出汇总表 ============
print("\n" + "=" * 60)
print("客单价分布分析汇总表")
print("=" * 60)
summary = pd.DataFrame({
    '指标': ['min', 'Q1(25%)', 'median', 'Q3(75%)', 'max', 'IQR', '上限', '下限', '均值'],
    '值': [q0, q1, q2, q3, q4, iqr, upper_limit, lower_limit, mean_val]
})
print(summary.to_string(index=False))
