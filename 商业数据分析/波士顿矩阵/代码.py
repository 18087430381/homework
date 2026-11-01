import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# ============ 1. 中文字体设置 ============
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 2. 读取数据 ============
# 假设 Excel 文件名为 1-1波士顿矩阵.xlsx，销售表是第二个 sheet
file_path = '1-1波士顿矩阵.xlsx'
df = pd.read_excel(file_path, sheet_name='销售表')

# 数据清洗
df['销售日期'] = pd.to_datetime(df['销售日期'])
df['销售额'] = df['单价'] * df['销量']

# ============ 3. 按品牌聚合（品牌作为业务单元） ============
# 按品牌汇总销售额、销量
brand_total = df.groupby('品牌').agg(
    总销售额=('销售额', 'sum'),
    总销量=('销量', 'sum'),
    订单数=('订单ID', 'count')
).reset_index()

# 计算各品牌销售额占比（相对市场份额的近似）
brand_total['销售额占比'] = brand_total['总销售额'] / brand_total['总销售额'].sum()

# ============ 4. 计算销售增长率（7月 vs 8月） ============
df['月份'] = df['销售日期'].dt.month
month_sales = df.pivot_table(
    index='品牌', columns='月份', values='销售额', aggfunc='sum'
).fillna(0)

# 7月、8月销售额
month_sales.columns = [f'{int(c)}月销售额' for c in month_sales.columns]
month_sales = month_sales.reset_index()

# 增长率 = (8月 - 7月) / 7月，若7月为0则用替代值
def calc_growth(row):
    july = row.get('7月销售额', 0)
    aug = row.get('8月销售额', 0)
    if july == 0:
        return aug * 100 if aug > 0 else 0
    return (aug - july) / july

month_sales['销售增长率'] = month_sales.apply(calc_growth, axis=1)

# 合并
bcg = brand_total.merge(month_sales[['品牌', '销售增长率']], on='品牌', how='left')

# ============ 5. 确定分界线（均值作为阈值） ============
growth_threshold = bcg['销售增长率'].mean()      # 纵轴分界
share_threshold = bcg['销售额占比'].mean()       # 横轴分界

print("增长率阈值：", round(growth_threshold, 4))
print("份额阈值：", round(share_threshold, 4))

# ============ 6. 波士顿矩阵分类 ============
def classify(row):
    high_growth = row['销售增长率'] >= growth_threshold
    high_share = row['销售额占比'] >= share_threshold
    if high_growth and high_share:
        return '明星业务'
    elif high_growth and not high_share:
        return '问题业务'
    elif not high_growth and high_share:
        return '金牛业务'
    else:
        return '瘦狗业务'

bcg['业务类型'] = bcg.apply(classify, axis=1)

# 打印分类结果
print("\n===== 波士顿矩阵分类结果 =====")
print(bcg[['品牌', '总销售额', '销售额占比', '销售增长率', '业务类型']]
      .sort_values('总销售额', ascending=False).to_string(index=False))

# ============ 7. 绘制波士顿矩阵气泡图 ============
colors = {
    '明星业务': '#e74c3c',
    '问题业务': '#f39c12',
    '金牛业务': '#27ae60',
    '瘦狗业务': '#7f8c8d'
}

fig, ax = plt.subplots(figsize=(11, 8))

for biz_type, group in bcg.groupby('业务类型'):
    ax.scatter(
        group['销售额占比'],
        group['销售增长率'],
        s=group['总销售额'] / 8,          # 气泡大小反映总销售额
        c=colors[biz_type],
        alpha=0.75,
        edgecolors='black',
        linewidths=0.8,
        label=biz_type
    )
    for _, row in group.iterrows():
        ax.annotate(
            row['品牌'],
            (row['销售额占比'], row['销售增长率']),
            fontsize=10, ha='center', va='center', fontweight='bold'
        )

# 分界线
ax.axvline(share_threshold, color='gray', linestyle='--', linewidth=1.2)
ax.axhline(growth_threshold, color='gray', linestyle='--', linewidth=1.2)

# 四象限文字标注
x_max = bcg['销售额占比'].max() * 1.15
y_max = bcg['销售增长率'].max() * 1.15
y_min = bcg['销售增长率'].min() * 1.15

ax.text(share_threshold * 1.02, y_max * 0.95, '明星业务\n（高增长/高份额）',
        fontsize=11, color=colors['明星业务'], fontweight='bold', va='top')
ax.text(share_threshold * 1.02, y_min * 0.95, '金牛业务\n（低增长/高份额）',
        fontsize=11, color=colors['金牛业务'], fontweight='bold', va='bottom')
ax.text(share_threshold * 0.6, y_max * 0.95, '问题业务\n（高增长/低份额）',
        fontsize=11, color=colors['问题业务'], fontweight='bold', va='top')
ax.text(share_threshold * 0.6, y_min * 0.95, '瘦狗业务\n（低增长/低份额）',
        fontsize=11, color=colors['瘦狗业务'], fontweight='bold', va='bottom')

ax.set_xlabel('相对市场份额（销售额占比）', fontsize=12)
ax.set_ylabel('销售增长率（7月→8月）', fontsize=12)
ax.set_title('波士顿矩阵（BCG Matrix）—— 品牌业务分析', fontsize=15, fontweight='bold')
ax.legend(loc='upper right', fontsize=10, title='业务类型')
ax.grid(alpha=0.25)

plt.tight_layout()
plt.savefig('波士顿矩阵.png', dpi=150, bbox_inches='tight')
plt.show()

# ============ 8. 导出结果 ============
bcg.sort_values('总销售额', ascending=False).to_excel(
    '波士顿矩阵结果.xlsx', index=False
)
print("\n结果已导出为：波士顿矩阵结果.xlsx / 波士顿矩阵.png")
