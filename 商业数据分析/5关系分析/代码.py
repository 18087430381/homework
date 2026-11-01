import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import stats

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 1. 构造数据 ============

# 1.1 不同营销活动客户下单情况对比
marketing_activities = ['营销活动 1', '营销活动 2', '营销活动 3', '营销活动 4', '营销活动 5']
np.random.seed(42)
ordered_users = np.random.randint(100, 500, size=5)
unordered_users = np.random.randint(100, 500, size=5)

df_marketing = pd.DataFrame({
    '营销活动': marketing_activities,
    '下单用户': ordered_users,
    '未下单用户': unordered_users
})
df_marketing['总人数'] = df_marketing['下单用户'] + df_marketing['未下单用户']
df_marketing['下单率'] = df_marketing['下单用户'] / df_marketing['总人数']

print("=" * 60)
print("1. 不同营销活动客户下单情况对比")
print("=" * 60)
print(df_marketing.to_string(index=False))

# 1.2 不同忠诚度客户对品牌满意度对比
loyalty_levels = ['忠诚度高', '忠诚度中', '忠诚度低']
satisfied = np.random.randint(100, 500, size=3)
unsatisfied = np.random.randint(100, 500, size=3)

df_loyalty = pd.DataFrame({
    '忠诚度': loyalty_levels,
    '满意': satisfied,
    '不满意': unsatisfied
})
df_loyalty['总人数'] = df_loyalty['满意'] + df_loyalty['不满意']
df_loyalty['满意率'] = df_loyalty['满意'] / df_loyalty['总人数']

print("\n" + "=" * 60)
print("2. 不同忠诚度客户对品牌满意度对比")
print("=" * 60)
print(df_loyalty.to_string(index=False))

# 1.3 营销活动销售额数据（分类变量&连续变量）
np.random.seed(123)
n_users = 60
user_ids = [f'id{i}' for i in range(1, n_users + 1)]
sales_act1 = np.random.randint(50, 500, size=n_users)
sales_act2 = np.random.randint(300, 1000, size=n_users)
sales_act3 = np.random.randint(10, 200, size=n_users)

df_sales = pd.DataFrame({
    '用户id': user_ids,
    '营销活动1': sales_act1,
    '营销活动2': sales_act2,
    '营销活动3': sales_act3
})

print("\n" + "=" * 60)
print("3. 各营销活动销售额数据（前10行）")
print("=" * 60)
print(df_sales.head(10).to_string(index=False))
print(f"\n销售额统计描述：")
print(df_sales[['营销活动1', '营销活动2', '营销活动3']].describe().to_string())

# 1.4 投入成本与产出收益数据（两个连续变量间关系）
revenue = np.array([
    438.21, 600.77, 555.95, 560.21, 387.21, 629.77, 791.95, 386.85, 306.21, 466.85,
    302.77, 470.21, 935.21, 482.95, 315.77, 798.77, 97.77, 653.97, 600.95, 864.77,
    803.21, 803.97, 947.77, 532.95, 359.97, 833.21, 401.97, 903.97, 674.21, 315.95,
    730.95, 913.97, 354.21, 330.77, 194.95, 537.21, 531.95, 335.77, 865.21, 429.95,
    740.97, 303.95, 200.97, 771.85, 422.85, 709.77, 783.21, 684.77, 614.21, 674.85,
    877.77, 578.85, 98.95, 50.21, 759.97, 874.95, 106.21, 336.85
])
cost = np.array([
    155, 272, 248, 292, 144, 329, 411, 216, 91, 195,
    135, 176, 415, 257, 153, 357, 48, 286, 292, 431,
    426, 385, 441, 236, 154, 439, 154, 387, 319, 137,
    329, 432, 187, 136, 142, 282, 241, 181, 429, 175,
    376, 165, 95, 342, 166, 341, 378, 311, 326, 299,
    450, 276, 37, 55, 356, 404, 45, 153
])

df_cost_revenue = pd.DataFrame({
    '投入成本': cost,
    '产出收益': revenue
})

# 计算相关系数
corr, p_value = stats.pearsonr(df_cost_revenue['投入成本'], df_cost_revenue['产出收益'])
# 线性回归
slope, intercept, r_value, p_val, std_err = stats.linregress(
    df_cost_revenue['投入成本'], df_cost_revenue['产出收益']
)

print("\n" + "=" * 60)
print("4. 投入成本与产出收益关系分析")
print("=" * 60)
print(df_cost_revenue.describe().to_string())
print(f"\n皮尔逊相关系数: {corr:.4f} (p值: {p_value:.4e})")
print(f"线性回归方程: 产出收益 = {slope:.4f} × 投入成本 + {intercept:.4f}")
print(f"R² = {r_value**2:.4f}")

# ============ 2. 可视化 ============

fig = plt.figure(figsize=(18, 14))

# 图1：不同营销活动客户下单情况对比（分组柱状图）
ax1 = plt.subplot(2, 2, 1)
x = np.arange(len(marketing_activities))
width = 0.35
bars1 = ax1.bar(x - width/2, ordered_users, width, label='下单用户', color='#4C72B0')
bars2 = ax1.bar(x + width/2, unordered_users, width, label='未下单用户', color='#DD8452')

# 在柱子上标注下单率
for i, (o, u) in enumerate(zip(ordered_users, unordered_users)):
    rate = o / (o + u) * 100
    ax1.text(i, max(o, u) + 20, f'{rate:.1f}%', ha='center', fontsize=9, 
             fontweight='bold', color='red')

ax1.set_xlabel('营销活动', fontsize=11)
ax1.set_ylabel('用户人数', fontsize=11)
ax1.set_title('不同营销活动客户下单情况对比\n(红色数字为下单率)', fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(marketing_activities)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 图2：不同忠诚度客户满意度对比（堆叠柱状图）
ax2 = plt.subplot(2, 2, 2)
x2 = np.arange(len(loyalty_levels))
width2 = 0.5
p1 = ax2.bar(x2, satisfied, width2, label='满意', color='#55A868')
p2 = ax2.bar(x2, unsatisfied, width2, bottom=satisfied, label='不满意', color='#C44E52')

# 标注满意率
for i, (s, u) in enumerate(zip(satisfied, unsatisfied)):
    rate = s / (s + u) * 100
    ax2.text(i, s + u + 15, f'满意率: {rate:.1f}%', ha='center', fontsize=10, 
             fontweight='bold', color='darkgreen')

ax2.set_xlabel('忠诚度', fontsize=11)
ax2.set_ylabel('人数', fontsize=11)
ax2.set_title('不同忠诚度客户对品牌满意度对比', fontsize=13, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(loyalty_levels)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 图3：各营销活动销售额对比图（箱线图 + 散点，反映分布情况）
ax3 = plt.subplot(2, 2, 3)
sales_data = [sales_act1, sales_act2, sales_act3]
labels = ['营销活动1', '营销活动2', '营销活动3']
colors = ['#4C72B0', '#DD8452', '#55A868']

bp = ax3.boxplot(sales_data, labels=labels, patch_artist=True, widths=0.5,
                 showmeans=True, meanline=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

# 叠加散点显示分布
for i, data in enumerate(sales_data):
    x_jitter = np.random.normal(i + 1, 0.06, size=len(data))
    ax3.scatter(x_jitter, data, alpha=0.4, s=15, color=colors[i], edgecolors='none')

ax3.set_ylabel('销售额', fontsize=11)
ax3.set_title('各营销活动销售额对比及分布情况\n(箱线图+散点)', fontsize=13, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

# 在箱线图上标注均值
means = [np.mean(d) for d in sales_data]
for i, m in enumerate(means):
    ax3.text(i + 1, m + 15, f'均值:{m:.0f}', ha='center', fontsize=9, 
             color='darkred', fontweight='bold')

# 图4：投入成本与产出收益关系（散点图 + 回归线）
ax4 = plt.subplot(2, 2, 4)
scatter = ax4.scatter(df_cost_revenue['投入成本'], df_cost_revenue['产出收益'],
                      c=df_cost_revenue['产出收益'], cmap='viridis', 
                      s=60, alpha=0.7, edgecolors='white', linewidth=0.5)

# 回归线
x_line = np.linspace(cost.min(), cost.max(), 100)
y_line = slope * x_line + intercept
ax4.plot(x_line, y_line, color='red', linewidth=2, linestyle='--',
         label=f'回归线: y={slope:.2f}x+{intercept:.2f}\nR²={r_value**2:.3f}, r={corr:.3f}')

ax4.set_xlabel('投入成本', fontsize=11)
ax4.set_ylabel('产出收益', fontsize=11)
ax4.set_title('投入成本与产出收益关系\n(散点图+线性回归)', fontsize=13, fontweight='bold')
ax4.legend(loc='upper left', fontsize=9)
ax4.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax4, label='产出收益')

plt.tight_layout(pad=3.0)
plt.savefig('关系分析可视化.png', dpi=150, bbox_inches='tight')
plt.show()

# ============ 3. 输出关键结论 ============

print("\n" + "=" * 60)
print("分析结论汇总")
print("=" * 60)

# 最佳营销活动
best_idx = df_marketing['下单率'].idxmax()
print(f"\n【营销活动效果】")
print(f"  下单率最高的活动: {df_marketing.loc[best_idx, '营销活动']} "
      f"(下单率 {df_marketing.loc[best_idx, '下单率']*100:.1f}%)")
print(f"  各活动下单率范围: {df_marketing['下单率'].min()*100:.1f}% ~ {df_marketing['下单率'].max()*100:.1f}%")

# 忠诚度与满意度
print(f"\n【忠诚度与满意度】")
for _, row in df_loyalty.iterrows():
    print(f"  {row['忠诚度']}: 满意率 {row['满意率']*100:.1f}%")
print(f"  忠诚度越高，满意率{'越高' if df_loyalty['满意率'].is_monotonic_decreasing else '无明显单调关系'}")

# 销售额分布
print(f"\n【各营销活动销售额】")
for col in ['营销活动1', '营销活动2', '营销活动3']:
    print(f"  {col}: 均值={df_sales[col].mean():.1f}, "
          f"标准差={df_sales[col].std():.1f}, "
          f"范围=[{df_sales[col].min()}, {df_sales[col].max()}]")

# 成本收益关系
print(f"\n【投入成本与产出收益】")
print(f"  相关系数 r = {corr:.4f} → {'强' if abs(corr)>0.7 else '中等' if abs(corr)>0.4 else '弱'}正相关")
print(f"  回归方程: 收益 = {slope:.2f} × 成本 + {intercept:.2f}")
print(f"  R² = {r_value**2:.4f}，即投入成本可解释收益变异的 {r_value**2*100:.1f}%")
print(f"  结论: 投入成本与产出收益呈显著正相关，增加投入总体上能带来更高收益")
