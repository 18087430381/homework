import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')
print("=" * 60)
print("1. 动态柱形图 - 各地区月度销售数据")
print("=" * 60)
df_bar = pd.DataFrame({
    '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
    '华北': [259, 235, 330, 282, 282, 965],
    '华南': [247, 266, 342, 342, 323, 380],
    '东北': [705, 529, 705, 599, 705, 282],
    '西北': [513, 324, 540, 270, 486, 567],
    '西南': [463, 579, 492, 492, 405, 463],
    '华东': [384, 282, 308, 384, 308, 897],
})
print(df_bar.to_string(index=False))
print("\n各地区总和:")
print(df_bar.iloc[:, 1:].sum().sort_values(ascending=False))
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
x = np.arange(len(df_bar['月份']))
width = 0.13
regions = df_bar.columns[1:]
colors = plt.cm.Set2(np.linspace(0, 1, len(regions)))
for i, region in enumerate(regions):
    axes[0].bar(x + i * width, df_bar[region], width, label=region, color=colors[i])
axes[0].set_xlabel('月份')
axes[0].set_ylabel('销售额')
axes[0].set_title('各地区月度销售对比（动态柱形图）')
axes[0].set_xticks(x + width * 2.5)
axes[0].set_xticklabels(df_bar['月份'])
axes[0].legend(ncol=3)
totals = df_bar.iloc[:, 1:].sum().sort_values(ascending=True)
axes[1].barh(totals.index, totals.values, color='steelblue')
axes[1].set_xlabel('总销售额')
axes[1].set_title('各地区总销售额排名')
for i, v in enumerate(totals.values):
    axes[1].text(v + 20, i, str(v), va='center')
plt.tight_layout()
plt.savefig('01_动态柱形图.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("2. 动态跑道图 - 各部门月度人数")
print("=" * 60)
df_runway = pd.DataFrame({
    '部门': ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部'],
    '1月': [130, 226, 238, 293, 326, 451],
    '2月': [138, 206, 228, 305, 349, 456],
    '3月': [130, 217, 255, 314, 316, 406],
    '4月': [129, 226, 226, 264, 359, 433],
})
df_runway['平均'] = df_runway.iloc[:, 1:].mean(axis=1)
print(df_runway.to_string(index=False))
print(f"\n公司总人数(4月): {df_runway['4月'].sum()}")
fig, ax = plt.subplots(figsize=(14, 7))
months = ['1月', '2月', '3月', '4月']
colors = plt.cm.tab10(np.linspace(0, 1, len(df_runway)))
for i, row in df_runway.iterrows():
    values = [row[m] for m in months]
    ax.plot(months, values, marker='o', linewidth=3, markersize=10,
            label=row['部门'], color=colors[i])
    for j, v in enumerate(values):
        ax.annotate(str(v), (j, v), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=9)
ax.set_xlabel('月份')
ax.set_ylabel('人数')
ax.set_title('各部门月度人数变化（动态跑道图）')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('02_动态跑道图.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("3. 动态南丁格尔圆环图 - 流量来源占比")
print("=" * 60)
df_nightingale = pd.DataFrame({
    '来源': ['首页推荐', '关注页面', '搜索', '个人主页', '其他来源'],
    '近7天': [0.44, 0.17, 0.15, 0.08, 0.16],
    '近30天': [0.38, 0.21, 0.15, 0.09, 0.17],
})
print(df_nightingale.to_string(index=False))
fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw=dict(polar=True))
for idx, period in enumerate(['近7天', '近30天']):
    values = df_nightingale[period].values
    labels = df_nightingale['来源'].values
    N = len(values)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N * 0.9
    ax = axes[idx]
    bars = ax.bar(theta, values, width=width, bottom=0.1,
                  color=plt.cm.Spectral(np.linspace(0, 1, N)))
    ax.set_xticks(theta)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_title(f'{period}流量来源（南丁格尔图）', pad=20)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.15,
                f'{v:.0%}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('03_南丁格尔图.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("4. 动态组合图 - 销售额/利润/利润率")
print("=" * 60)
df_combo = pd.DataFrame({
    '类别': ['口红', '面膜', '隔离', '粉底液'],
    '销售额': [2800, 2564, 2282, 2353],
    '利润': [1896, 1563, 986, 1324],
})
df_combo['利润率'] = df_combo['利润'] / df_combo['销售额']
print(df_combo.to_string(index=False))
fig, ax1 = plt.subplots(figsize=(12, 6))
x = np.arange(len(df_combo))
width = 0.35
bars1 = ax1.bar(x - width/2, df_combo['销售额'], width, label='销售额', color='#4472C4')
bars2 = ax1.bar(x + width/2, df_combo['利润'], width, label='利润', color='#ED7D31')
ax1.set_xlabel('产品类别')
ax1.set_ylabel('金额')
ax1.set_xticks(x)
ax1.set_xticklabels(df_combo['类别'])
ax1.legend(loc='upper left')
for bar in bars1:
    ax1.annotate(f'{bar.get_height():.0f}', (bar.get_x()+bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=9)
for bar in bars2:
    ax1.annotate(f'{bar.get_height():.0f}', (bar.get_x()+bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=9)
ax2 = ax1.twinx()
ax2.plot(x, df_combo['利润率'], 'o-', color='#C00000', linewidth=2, markersize=10, label='利润率')
for i, v in enumerate(df_combo['利润率']):
    ax2.annotate(f'{v:.1%}', (i, v), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=10, color='#C00000', fontweight='bold')
ax2.set_ylabel('利润率', color='#C00000')
ax2.tick_params(axis='y', labelcolor='#C00000')
ax2.set_ylim(0, 1)
ax2.legend(loc='upper right')
plt.title('产品销售额、利润与利润率（动态组合图）')
plt.tight_layout()
plt.savefig('04_动态组合图.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("5. 人力资源明细分析")
print("=" * 60)
print("注：完整数据请通过 pd.read_excel 读取第5张工作表")
hr_stats = {
    '部门分布': pd.Series({'市场拓展': 380, '销售': 180, '财务': 60, '行政': 55, '人力资源': 25}),
    '学历分布': pd.Series({'本科': 250, '专科': 200, '硕士': 150, '高中': 80, '博士': 20}),
    '年龄分段': pd.Series({'20-29': 180, '30-39': 320, '40-49': 150, '>=50': 50}),
    '性别分布': pd.Series({'男': 480, '女': 220}),
}
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes[0, 0].pie(hr_stats['部门分布'], labels=hr_stats['部门分布'].index,
               autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
axes[0, 0].set_title('部门人员分布')
axes[0, 1].bar(hr_stats['学历分布'].index, hr_stats['学历分布'].values,
               color=['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5'])
axes[0, 1].set_title('学历分布')
axes[0, 1].set_ylabel('人数')
for i, v in enumerate(hr_stats['学历分布'].values):
    axes[0, 1].text(i, v + 5, str(v), ha='center')
axes[1, 0].bar(hr_stats['年龄分段'].index, hr_stats['年龄分段'].values, color='#70AD47')
axes[1, 0].set_title('年龄分段分布')
axes[1, 0].set_ylabel('人数')
for i, v in enumerate(hr_stats['年龄分段'].values):
    axes[1, 0].text(i, v + 5, str(v), ha='center')
axes[1, 1].pie(hr_stats['性别分布'], labels=hr_stats['性别分布'].index,
               autopct='%1.1f%%', startangle=90, colors=['#5B9BD5', '#ED7D31'])
axes[1, 1].set_title('性别分布')
plt.suptitle('人力资源明细分析', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('05_人力资源分析.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("6. 透视表切片器 - 学历平均月收入")
print("=" * 60)
df_pivot = pd.DataFrame({
    '学历': ['本科', '博士', '高中', '硕士', '专科', '总计'],
    '平均月收入': [6138.32, 7187.00, 5853.63, 6739.01, 6908.04, 6446.50]
})
print(df_pivot.to_string(index=False))
fig, ax = plt.subplots(figsize=(10, 6))
data = df_pivot[df_pivot['学历'] != '总计']
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#70AD47']
bars = ax.bar(data['学历'], data['平均月收入'], color=colors)
ax.axhline(y=6446.50, color='red', linestyle='--', linewidth=2, label='总计平均: 6446.50')
for bar, v in zip(bars, data['平均月收入']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f'{v:,.0f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('平均月收入')
ax.set_title('不同学历的平均月收入（透视表切片器）')
ax.legend()
plt.tight_layout()
plt.savefig('06_透视表分析.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("7. VBA动态玉玦图 - 流量来源占比")
print("=" * 60)
df_yujue = pd.DataFrame({
    '来源': ['个人主页', '搜索', '关注页面', '首页推荐'],
    '近7天': [0.13, 0.19, 0.32, 0.36],
    '近30天': [0.09, 0.24, 0.29, 0.38],
})
print(df_yujue.to_string(index=False))
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(df_yujue))
width = 0.35
bars1 = ax.bar(x - width/2, df_yujue['近7天'], width, label='近7天', color='#4472C4')
bars2 = ax.bar(x + width/2, df_yujue['近30天'], width, label='近30天', color='#ED7D31')
for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{bar.get_height():.0%}', ha='center', fontsize=9)
ax.set_xlabel('流量来源')
ax.set_ylabel('占比')
ax.set_title('流量来源占比对比（动态玉玦图）')
ax.set_xticks(x)
ax.set_xticklabels(df_yujue['来源'])
ax.legend()
plt.tight_layout()
plt.savefig('07_玉玦图.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("8. 动态滑珠图 - 各地区月度完成率")
print("=" * 60)
df_slider = pd.DataFrame({
    '区域': ['华北', '华南', '东北', '西北', '西南', '华东'],
    '1月': [0.32, 0.49, 0.65, 0.73, 0.536, 0.32],
    '2月': [0.45, 0.36, 0.53, 0.63, 0.498, 0.49],
    '3月': [0.66, 0.54, 0.58, 0.61, 0.527, 0.65],
    '4月': [0.52, 0.39, 0.48, 0.53, 0.708, 0.73],
    '5月': [0.69, 0.415, 0.445, 0.47, 0.7035, 0.536],
    '6月': [0.771, 0.403, 0.399, 0.408, 0.758, 0.7468],
})
print(df_slider.to_string(index=False))
print(f"\n各地区平均完成率:")
print(df_slider.iloc[:, 1:].mean(axis=1).sort_values(ascending=False))
fig, ax = plt.subplots(figsize=(14, 7))
months = ['1月', '2月', '3月', '4月', '5月', '6月']
colors = plt.cm.tab10(np.linspace(0, 1, len(df_slider)))
for i, row in df_slider.iterrows():
    values = [row[m] for m in months]
    ax.plot(months, values, marker='o', linewidth=2.5, markersize=12,
            label=row['区域'], color=colors[i], alpha=0.8)
    # 终点标注
    ax.annotate(f"{row['区域']}: {values[-1]:.1%}", (months[-1], values[-1]),
                textcoords="offset points", xytext=(15, 0),
                ha='left', fontsize=9, color=colors[i])
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50%基准线')
ax.set_xlabel('月份')
ax.set_ylabel('完成率')
ax.set_title('各地区月度完成率变化（动态滑珠图）')
ax.set_ylim(0.2, 0.9)
ax.legend(loc='lower right', ncol=2)
plt.tight_layout()
plt.savefig('08_动态滑珠图.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("分析完成！已生成以下图表:")
print("=" * 60)
print("01_动态柱形图.png       - 各地区月度销售对比")
print("02_动态跑道图.png       - 各部门月度人数变化")
print("03_南丁格尔图.png       - 流量来源占比")
print("04_动态组合图.png       - 产品销售额/利润/利润率")
print("05_人力资源分析.png     - 部门/学历/年龄/性别分布")
print("06_透视表分析.png       - 学历平均月收入")
print("07_玉玦图.png           - 流量来源对比")
print("08_动态滑珠图.png       - 各地区完成率")
