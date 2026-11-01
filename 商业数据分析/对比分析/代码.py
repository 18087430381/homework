import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============ 数据准备 ============

# 第一部分：不同产品订单量对比（随机数据模拟RANDBETWEEN(200,500)）
np.random.seed(42)
products_1 = [f'产品 {i}' for i in range(1, 12)]
orders_1 = np.random.randint(200, 501, size=11)

# 第二部分：排序后的订单量对比
products_2 = [f'我的名字非常长{i}' for i in range(12, 1, -1)]
orders_2 = [205, 214, 258, 291, 295, 323, 375, 383, 400, 483, 494]

# 第三部分：客户画像雷达图数据
dimensions = ['I', 'E', 'S', 'N', 'T', 'P']
scores = [80, 10, 30, 60, 50, 40]

print("=" * 60)
print("【数据概览】")
print("=" * 60)

print("\n1. 不同产品订单量对比（随机生成）:")
df1 = pd.DataFrame({'产品类型': products_1, '订单量': orders_1})
print(df1.to_string(index=False))

print("\n2. 不同产品订单量对比（排序后）:")
df2 = pd.DataFrame({'产品类型': products_2, '订单量': orders_2})
print(df2.to_string(index=False))

print("\n3. 客户画像六维度得分:")
df3 = pd.DataFrame({'维度': dimensions, '得分': scores})
print(df3.to_string(index=False))

# ============ 图表绘制 ============
fig = plt.figure(figsize=(18, 12))
fig.suptitle('2对比分析 - 数据可视化', fontsize=20, fontweight='bold', y=0.98)

# ---- 图1：不同产品订单量对比（柱状图）----
ax1 = fig.add_subplot(2, 2, 1)
colors1 = plt.cm.viridis(np.linspace(0.2, 0.9, len(products_1)))
bars1 = ax1.bar(products_1, orders_1, color=colors1, edgecolor='white', linewidth=1.2)
ax1.set_title('不同产品订单量对比', fontsize=14, fontweight='bold')
ax1.set_xlabel('产品类型', fontsize=11)
ax1.set_ylabel('订单量（单位：个）', fontsize=11)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
for bar, val in zip(bars1, orders_1):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             str(val), ha='center', va='bottom', fontsize=9)

# ---- 图2：排序后的订单量对比（水平条形图）----
ax2 = fig.add_subplot(2, 2, 2)
colors2 = plt.cm.plasma(np.linspace(0.15, 0.85, len(products_2)))
bars2 = ax2.barh(products_2, orders_2, color=colors2, edgecolor='white', linewidth=1.2)
ax2.set_title('不同产品订单量对比（排序）', fontsize=14, fontweight='bold')
ax2.set_xlabel('订单量（单位：个）', fontsize=11)
ax2.set_ylabel('产品类型', fontsize=11)
ax2.grid(axis='x', alpha=0.3, linestyle='--')
for bar, val in zip(bars2, orders_2):
    ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
             str(val), ha='left', va='center', fontsize=9)

# ---- 图3：客户画像雷达图 ----
ax3 = fig.add_subplot(2, 2, 3, projection='polar')

# 闭合雷达图数据
angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
scores_closed = scores + [scores[0]]
angles_closed = angles + [angles[0]]

ax3.plot(angles_closed, scores_closed, 'o-', linewidth=2, color='#e74c3c', markersize=6, label='得分')
ax3.fill(angles_closed, scores_closed, alpha=0.25, color='#e74c3c')
ax3.set_xticks(angles)
ax3.set_xticklabels(dimensions, fontsize=12, fontweight='bold')
ax3.set_ylim(0, 100)
ax3.set_yticks([20, 40, 60, 80, 100])
ax3.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9, color='grey')
ax3.set_title('客户画像雷达图', fontsize=14, fontweight='bold', pad=20)
ax3.grid(True, alpha=0.3)
for angle, score, dim in zip(angles, scores, dimensions):
    ax3.text(angle, score + 8, f'{dim}:{score}', ha='center', va='center',
             fontsize=9, fontweight='bold', color='#c0392b')

# ---- 图4：客户画像得分柱状图（补充展示）----
ax4 = fig.add_subplot(2, 2, 4)
colors4 = ['#e74c3c' if s == max(scores) else '#3498db' if s == min(scores) else '#95a5a6' for s in scores]
bars4 = ax4.bar(dimensions, scores, color=colors4, edgecolor='white', linewidth=1.2)
ax4.set_title('客户画像六维度得分', fontsize=14, fontweight='bold')
ax4.set_xlabel('维度', fontsize=11)
ax4.set_ylabel('因素得分', fontsize=11)
ax4.set_ylim(0, 100)
ax4.grid(axis='y', alpha=0.3, linestyle='--')
for bar, val in zip(bars4, scores):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             str(val), ha='center', va='bottom', fontsize=11, fontweight='bold')
# 添加图例说明
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#e74c3c', label='最高分'),
                   Patch(facecolor='#3498db', label='最低分'),
                   Patch(facecolor='#95a5a6', label='其他')]
ax4.legend(handles=legend_elements, loc='upper right', fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('对比分析结果.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "=" * 60)
print("图表已保存为：对比分析结果.png")
print("=" * 60)
