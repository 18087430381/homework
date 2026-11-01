import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 读取数据
df = pd.read_excel('3-1相关分析.xlsx', sheet_name='原始数据')

print("=" * 60)
print("数据概览")
print("=" * 60)
print(f"样本量: {len(df)}")
print(f"列名: {df.columns.tolist()}")
print(f"\n前5行数据:")
print(df.head())
print(f"\n描述性统计:")
print(df.describe())

# 检查缺失值
print(f"\n缺失值统计:")
print(df.isnull().sum())

# 计算皮尔逊相关系数
pearson_r, pearson_p = stats.pearsonr(df['x'], df['y'])
print("\n" + "=" * 60)
print("相关性分析结果")
print("=" * 60)
print(f"皮尔逊相关系数 r = {pearson_r:.4f}")
print(f"p值 = {pearson_p:.6e}")
print(f"决定系数 R² = {pearson_r**2:.4f}")

if pearson_p < 0.001:
    sig = "极其显著 (p < 0.001)"
elif pearson_p < 0.01:
    sig = "非常显著 (p < 0.01)"
elif pearson_p < 0.05:
    sig = "显著 (p < 0.05)"
else:
    sig = "不显著 (p >= 0.05)"
print(f"显著性: {sig}")

# 斯皮尔曼相关
spearman_r, spearman_p = stats.spearmanr(df['x'], df['y'])
print(f"\n斯皮尔曼相关系数 ρ = {spearman_r:.4f}, p = {spearman_p:.6e}")

# 肯德尔相关
kendall_r, kendall_p = stats.kendalltau(df['x'], df['y'])
print(f"肯德尔相关系数 τ = {kendall_r:.4f}, p = {kendall_p:.6e}")

# 相关矩阵
corr_matrix = df.corr()
print(f"\n相关矩阵:")
print(corr_matrix)

# 线性回归拟合
slope, intercept, r_value, p_value, std_err = stats.linregress(df['x'], df['y'])
print(f"\n线性回归: y = {slope:.4f} * x + {intercept:.4f}")
print(f"斜率标准误: {std_err:.4f}")

# ============ 绘图（纯 matplotlib） ============
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# 图1: 散点图 + 回归线
ax1 = axes[0]
ax1.scatter(df['x'], df['y'], alpha=0.6, color='steelblue', edgecolors='white', s=50, label='数据点')
x_line = np.linspace(df['x'].min(), df['x'].max(), 100)
y_line = slope * x_line + intercept
ax1.plot(x_line, y_line, color='crimson', linewidth=2, label=f'拟合线 y={slope:.2f}x+{intercept:.1f}')
ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('y', fontsize=12)
ax1.set_title(f'x 与 y 散点图\nr = {pearson_r:.4f}, R² = {pearson_r**2:.4f}, p = {pearson_p:.2e}', fontsize=12)
ax1.legend()
ax1.grid(alpha=0.3)

# 图2: 相关系数热力图（用 imshow 手写）
ax2 = axes[1]
data = corr_matrix.values
im = ax2.imshow(data, cmap='RdBu_r', vmin=-1, vmax=1)
labels = corr_matrix.columns.tolist()
ax2.set_xticks(range(len(labels)))
ax2.set_yticks(range(len(labels)))
ax2.set_xticklabels(labels)
ax2.set_yticklabels(labels)
# 在每格中标注数值
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        color = 'white' if abs(data[i, j]) > 0.6 else 'black'
        ax2.text(j, i, f'{data[i, j]:.4f}', ha='center', va='center', color=color, fontsize=11)
ax2.set_title('相关系数热力图', fontsize=12)
cbar = fig.colorbar(im, ax=ax2)
cbar.set_label('相关系数')

# 图3: 残差图
ax3 = axes[2]
y_pred = slope * df['x'] + intercept
residuals = df['y'] - y_pred
ax3.scatter(y_pred, residuals, alpha=0.6, color='seagreen', edgecolors='white', s=50)
ax3.axhline(y=0, color='crimson', linestyle='--', linewidth=1.5)
ax3.set_xlabel('拟合值', fontsize=12)
ax3.set_ylabel('残差', fontsize=12)
ax3.set_title('残差图', fontsize=12)
ax3.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('correlation_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n图片已保存为 correlation_analysis.png")

# 导出结果
result_df = pd.DataFrame({
    '指标': ['皮尔逊r', '皮尔逊p值', 'R²', '斯皮尔曼ρ', '肯德尔τ', '回归斜率', '回归截距', '样本量'],
    '值': [pearson_r, pearson_p, pearson_r**2, spearman_r, kendall_r, slope, intercept, len(df)]
})
result_df.to_csv('correlation_results.csv', index=False, encoding='utf-8-sig')
print("结果已导出为 correlation_results.csv")
