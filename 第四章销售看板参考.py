import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')
FILE = r"C:\Users\x1808\Desktop\第四章 销售看板参考.xlsx"   # ← 改成你的实际路径
df_cost = pd.read_excel(FILE, sheet_name='成本明细')
df_sales = pd.read_excel(FILE, sheet_name='销售明细')
print(f"成本记录数：{len(df_cost)}")
print(f"销售记录数：{len(df_sales)}")
print(df_sales.head())
total_sales = df_sales['订单额'].sum()
total_profit = df_sales['利润额'].sum()
total_orders = len(df_sales)
total_cost = df_cost['成本'].sum()
print("\n" + "="*60)
print(f"【总销售额】{total_sales/10000:.2f} 万元")
print(f"【总利润额】{total_profit/10000:.2f} 万元")
print(f"【总成本】  {total_cost:.2f} 万元")
print(f"【订单总数】{total_orders}")
print(f"【利润率】  {total_profit/total_sales:.2%}")
print("="*60)
month_order = [f"{i}月" for i in range(1, 13)]
monthly = df_sales.groupby('月份_销售').agg(
    销售额=('订单额', 'sum'),
    利润额=('利润额', 'sum'),
    订单数=('订单单号', 'count')
).reindex(month_order)
monthly['成本'] = df_cost.groupby('月份_成本')['成本'].sum().reindex(month_order)
monthly['利润率'] = monthly['利润额'] / monthly['销售额']
monthly['销售额(万)'] = monthly['销售额'] / 10000
monthly['利润额(万)'] = monthly['利润额'] / 10000
monthly['同比'] = monthly['销售额(万)'].pct_change()
print("\n【按月汇总】")
print(monthly[['销售额(万)', '利润额(万)', '利润率', '订单数', '同比']].round(2))
region = df_sales.groupby('区域').agg(
    销售额=('订单额', 'sum'),
    利润额=('利润额', 'sum'),
    订单数=('订单单号', 'count')
).sort_values('销售额', ascending=False)
region['销售额(万)'] = region['销售额'] / 10000
region['利润率'] = region['利润额'] / region['销售额']
print("\n【区域销售排名】")
print(region[['销售额(万)', '利润率', '订单数']].round(2))
category = df_sales.groupby('产品类别').agg(
    销售额=('订单额', 'sum'),
    利润额=('利润额', 'sum'),
    订单数=('订单单号', 'count')
).sort_values('销售额', ascending=False)
category['销售额(万)'] = category['销售额'] / 10000
category['利润率'] = category['利润额'] / category['销售额']
print("\n【产品类别销售】")
print(category[['销售额(万)', '利润率', '订单数']].round(2))
top10 = df_sales.groupby('产品名称').agg(
    销售额=('订单额', 'sum'),
    销量=('订单单号', 'count')
).sort_values('销售额', ascending=False).head(10)
top10['销售额(万)'] = top10['销售额'] / 10000
print("\n【Top10 产品】")
print(top10.round(2))
express = df_sales.groupby('快递公司').agg(
    订单数=('订单单号', 'count'),
    销售额=('订单额', 'sum'),
    利润额=('利润额', 'sum')
).sort_values('订单数', ascending=False)
express['销售额(万)'] = express['销售额'] / 10000
print("\n【快递公司订单分布】")
print(express[['订单数', '销售额(万)']].round(2))
cost_cat = df_cost.groupby('类别')['成本'].sum().sort_values(ascending=False)
cost_ratio = cost_cat / cost_cat.sum()          # 单独存占比，不动 cost_cat
print("\n【成本结构】")
print(pd.DataFrame({'成本': cost_cat.round(2), '占比': cost_ratio.round(4)}))
fig = plt.figure(figsize=(18, 12))
fig.suptitle(f'销售数据看板  |  总销售额：{total_sales/10000:.1f}万  总利润：{total_profit/10000:.1f}万',
             fontsize=18, fontweight='bold', y=0.98)
ax1 = fig.add_subplot(3, 3, 1)
bars = ax1.bar(monthly.index, monthly['销售额(万)'], color='#4472C4', alpha=0.8)
ax1.set_title('月度销售额与利润率', fontweight='bold')
ax1.set_ylabel('销售额(万)', color='#4472C4')
ax1.tick_params(axis='y', labelcolor='#4472C4')
ax2 = ax1.twinx()
ax2.plot(monthly.index, monthly['利润率'], 'o-', color='#C00000', linewidth=2)
ax2.set_ylabel('利润率', color='#C00000')
ax2.tick_params(axis='y', labelcolor='#C00000')
for bar, v in zip(bars, monthly['销售额(万)']):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height(),
             f'{v:.0f}', ha='center', va='bottom', fontsize=7)
ax3 = fig.add_subplot(3, 3, 2)
ax3.pie(region['销售额'], labels=region.index, autopct='%1.1f%%',
        colors=plt.cm.Set3.colors, startangle=90)
ax3.set_title('区域销售占比', fontweight='bold')
ax4 = fig.add_subplot(3, 3, 3)
bars = ax4.barh(category.index, category['销售额(万)'], color='#70AD47')
ax4.set_title('产品类别销售额', fontweight='bold')
ax4.set_xlabel('销售额(万)')
for bar, v in zip(bars, category['销售额(万)']):
    ax4.text(v+1, bar.get_y()+bar.get_height()/2, f'{v:.0f}', va='center', fontsize=9)
ax5 = fig.add_subplot(3, 3, 4)
top10_sorted = top10.sort_values('销售额(万)')
bars = ax5.barh(range(len(top10_sorted)), top10_sorted['销售额(万)'], color='#ED7D31')
ax5.set_yticks(range(len(top10_sorted)))
ax5.set_yticklabels(top10_sorted.index, fontsize=8)
ax5.set_title('Top10 产品销售额', fontweight='bold')
ax5.set_xlabel('销售额(万)')
ax6 = fig.add_subplot(3, 3, 5)
ax6.pie(express['订单数'], labels=express.index, autopct='%1.1f%%',
        colors=plt.cm.Set2.colors, startangle=90)
ax6.set_title('快递公司订单分布', fontweight='bold')
ax7 = fig.add_subplot(3, 3, 6)
ax7.pie(cost_cat, labels=cost_cat.index, autopct='%1.1f%%',
        colors=['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000'])
ax7.set_title('成本结构占比', fontweight='bold')
ax8 = fig.add_subplot(3, 3, 7)
colors = ['#70AD47' if x > 0 else '#C00000' for x in region['利润率']]
bars = ax8.bar(region.index, region['利润率'], color=colors)
ax8.set_title('各区域利润率', fontweight='bold')
ax8.set_ylabel('利润率')
ax8.axhline(y=0, color='black', linewidth=0.8)
for bar, v in zip(bars, region['利润率']):
    ax8.text(bar.get_x()+bar.get_width()/2, v, f'{v:.1%}',
             ha='center', va='bottom' if v>0 else 'top', fontsize=8)
ax9 = fig.add_subplot(3, 3, 8)
bars = ax9.bar(monthly.index, monthly['订单数'], color='#5B9BD5')
ax9.set_title('月度订单数量', fontweight='bold')
ax9.set_ylabel('订单数')
for bar, v in zip(bars, monthly['订单数']):
    ax9.text(bar.get_x()+bar.get_width()/2, bar.get_height(),
             f'{v:.0f}', ha='center', va='bottom', fontsize=8)
ax10 = fig.add_subplot(3, 3, 9)
cost_month = df_cost.pivot_table(index='月份_成本', columns='类别',
                                  values='成本', aggfunc='sum').reindex(month_order)
cost_month.plot(kind='bar', stacked=True, ax=ax10, colormap='Set2', width=0.7)
ax10.set_title('月度成本结构', fontweight='bold')
ax10.set_ylabel('成本')
ax10.tick_params(axis='x', rotation=45)
ax10.legend(fontsize=7, loc='upper right')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('销售看板.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "="*60)
print("【关键结论】")
print("="*60)
print(f"1. 全年总销售额 {total_sales/10000:.1f} 万，总利润 {total_profit/10000:.1f} 万")
print(f"2. 整体利润率 {total_profit/total_sales:.2%}")
print(f"3. 销售额最高月份：{monthly['销售额(万)'].idxmax()}（{monthly['销售额(万)'].max():.1f}万）")
print(f"4. 销售额最低月份：{monthly['销售额(万)'].idxmin()}（{monthly['销售额(万)'].min():.1f}万）")
print(f"5. 最大销售区域：{region.index[0]}（{region['销售额(万)'].iloc[0]:.1f}万）")
print(f"6. 最畅销产品类别：{category.index[0]}（{category['销售额(万)'].iloc[0]:.1f}万）")
print(f"7. 最畅销单品：{top10.index[0]}（{top10['销售额(万)'].iloc[0]:.1f}万）")
print(f"8. 主要成本类别：{cost_cat.index[0]}（占比 {cost_ratio.iloc[0]:.1%}）")
print(f"9. 使用最多的快递：{express.index[0]}（{express['订单数'].iloc[0]}单）")
