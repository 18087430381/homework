import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体，避免中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)

# ============================================================
# 1. 近10年订单量波动趋势图
# ============================================================
years = list(range(2014, 2025))  # 2014-2024 共11年（原表实际为11行）
orders_year = np.random.randint(200, 501, size=len(years))

df_year = pd.DataFrame({
    'year': years,
    '订单量（单位：个）': orders_year
})

print("=" * 60)
print("1. 近10年订单量波动趋势")
print("=" * 60)
print(df_year.to_string(index=False))

# ============================================================
# 2. 第1-11周平均处理时长波动趋势
# ============================================================
weeks = [f"week{i}" for i in range(1, 12)]
# week1-week10: 1-40; week11: 32-40
durations = list(np.random.randint(1, 41, size=10)) + [np.random.randint(32, 41)]
durations = np.array(durations, dtype=float)

avg_duration = durations.mean()
warning_value = 35

df_week = pd.DataFrame({
    '周': weeks,
    '平均处理时长（单位：小时）': durations,
    '平均时长（单位：小时）': round(avg_duration, 2),
    '预警值': warning_value
})

max_duration = durations.max()
max_week = weeks[int(np.argmax(durations))]
diff_from_avg = max_duration - avg_duration

print("\n" + "=" * 60)
print("2. 第1-11周平均处理时长波动趋势")
print("=" * 60)
print(df_week.to_string(index=False))
print(f"\n最长时间：{max_duration:.2f} 小时（{max_week}）")
print(f"平均时长：{avg_duration:.2f} 小时")
print(f"最长时间比均值多了：{diff_from_avg:.2f} 小时")

# ============================================================
# 3. 各月订单量及环比增幅
# ============================================================
months = list(range(1, 13))
orders_month = np.random.randint(200, 501, size=12).astype(float)

mom_growth = [np.nan]  # 1月无环比
for i in range(1, 12):
    mom_growth.append((orders_month[i] - orders_month[i-1]) / orders_month[i-1])

df_month = pd.DataFrame({
    '月': months,
    '订单量（单位：个）': orders_month.astype(int),
    '环比增幅': [f"{x:.2%}" if not np.isnan(x) else "" for x in mom_growth]
})

print("\n" + "=" * 60)
print("3. 各月订单量及环比增幅")
print("=" * 60)
print(df_month.to_string(index=False))

# ============================================================
# 4. 绘图
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(10, 14))

# 图1：近10年订单量
axes[0].plot(df_year['year'], df_year['订单量（单位：个）'], marker='o', color='#1f77b4', linewidth=2)
axes[0].set_title('近10年订单量波动趋势图', fontsize=14, fontweight='bold')
axes[0].set_xlabel('年份')
axes[0].set_ylabel('订单量（个）')
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks(df_year['year'])
for x, y in zip(df_year['year'], df_year['订单量（单位：个）']):
    axes[0].annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8)

# 图2：第1-11周平均处理时长
axes[1].plot(weeks, durations, marker='s', color='#ff7f0e', linewidth=2, label='平均处理时长')
axes[1].axhline(y=avg_duration, color='green', linestyle='--', linewidth=1.5, label=f'平均时长 ({avg_duration:.2f}h)')
axes[1].axhline(y=warning_value, color='red', linestyle=':', linewidth=1.5, label=f'预警值 ({warning_value}h)')
axes[1].scatter([max_week], [max_duration], color='red', s=100, zorder=5, label=f'最长时间 ({max_duration:.2f}h)')
axes[1].set_title('第1-11周平均处理时长波动趋势图', fontsize=14, fontweight='bold')
axes[1].set_xlabel('周')
axes[1].set_ylabel('平均处理时长（小时）')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# 图3：各月订单量 + 环比增幅（双轴）
ax3 = axes[2]
ax3.bar(df_month['月'], df_month['订单量（单位：个）'], color='#2ca02c', alpha=0.7, label='订单量')
ax3.set_xlabel('月份')
ax3.set_ylabel('订单量（个）', color='#2ca02c')
ax3.set_xticks(df_month['月'])
ax3.grid(True, alpha=0.3)

ax3_twin = ax3.twinx()
mom_plot = [x * 100 if not np.isnan(x) else 0 for x in mom_growth]
ax3_twin.plot(df_month['月'], mom_plot, marker='^', color='#d62728', linewidth=2, label='环比增幅(%)')
ax3_twin.set_ylabel('环比增幅（%）', color='#d62728')
ax3_twin.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)

# 合并图例
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax3.set_title('各月订单量及环比增幅趋势图', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('趋势分析结果.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n图片已保存为：趋势分析结果.png")
