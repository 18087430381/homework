import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Wedge, Rectangle, FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter
import matplotlib.dates as mdates
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
COLORS = ['#5B9BD5', '#ED7D31', '#A5A5A5', '#FFC000', '#4472C4',
          '#70AD47', '#264478', '#9E480E', '#636363', '#997300']
def chart_01():
    regions = ['华北','华南','东北','西北','西南','华东']
    sales = [2354,1902,3524,2698,2896,2563]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(regions))
    bars = ax.bar(x, sales, width=0.6, color='#5B9BD5')
    for b in bars:
        b.set_alpha(0.85)
        b.set_edgecolor('#2E75B6')
    for i,v in enumerate(sales):
        ax.text(i, v+50, str(v), ha='center', fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(regions)
    ax.set_title('1. 渐变柱形图', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_01()
def chart_02():
    regions = ['华北','华南','东北','西北','西南','华东']
    sales = [2354,1902,3524,2698,2896,2563]
    mean_val = np.mean(sales)
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(regions))
    ax.bar(x, sales, color='#4472C4', width=0.6, label='销售量')
    ax.axhline(mean_val, color='red', ls='--', lw=2, label=f'均值 {mean_val:.1f}')
    for i,v in enumerate(sales):
        ax.text(i, v+50, str(v), ha='center', fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(regions)
    ax.set_title('2. 带均值柱形图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_02()
def chart_03():
    products = ['口红','面膜','隔离','防晒','精华','面霜']
    sales = [653,523,648,856,714,785]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(products))
    colors = plt.cm.Blues(np.linspace(0.4,0.9,len(products)))
    bars = ax.bar(x, sales, color=colors, width=0.6)
    for b,v in zip(bars,sales):
        ax.text(b.get_x()+b.get_width()/2, v+10, str(v), ha='center', fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(products)
    ax.set_title('3. 渐变圆角柱形图', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_03()
def chart_04():
    products = ['口红','面膜','隔离','防晒','精华','面霜','眼影','气垫']
    sales = [9221,5102,6571,5760,6321,8612,2645,5321]
    fig, ax = plt.subplots(figsize=(10,5))
    x = np.arange(len(products))
    bars = ax.bar(x, sales, color='#ED7D31', width=0.6)
    for b,v in zip(bars,sales):
        ax.annotate(f'{v}', xy=(b.get_x()+b.get_width()/2, v),
                    xytext=(0,5), textcoords='offset points',
                    ha='center', fontsize=10, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(products)
    ax.set_title('4. 标注柱形图', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_04()
def chart_05():
    quarters = ['2021Q1','Q2','Q3','Q4','2022Q1','Q2']
    sales = [3121,4086,4321,4601,4936,4231]
    profit = [1020,1421,1502,1623,1781,1432]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(quarters))
    ax.bar(x, sales, color='#5B9BD5', width=0.6, label='销售额')
    ax.bar(x, profit, bottom=sales, color='#ED7D31', width=0.6, label='利润额')
    for i,(s,p) in enumerate(zip(sales,profit)):
        ax.text(i, s/2, str(s), ha='center', va='center', fontsize=9)
        ax.text(i, s+p/2, str(p), ha='center', va='center', fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(quarters)
    ax.set_title('5. 层叠柱形图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_05()
def chart_06():
    regions = ['华东','西北','东北','华北','华南']
    s2022 = [1215,1321,1426,1531,2238]
    s2021 = [1003,1265,1531,1436,2066]
    fig, ax = plt.subplots(figsize=(9,5))
    y = np.arange(len(regions))
    ax.barh(y, [-v for v in s2022], color='#4472C4', label='2022年')
    ax.barh(y, s2021, color='#ED7D31', label='2021年')
    for i,(a,b) in enumerate(zip(s2022,s2021)):
        ax.text(-a-50, i, str(a), va='center', ha='right', fontsize=9)
        ax.text(b+50, i, str(b), va='center', ha='left', fontsize=9)
    ax.set_yticks(y); ax.set_yticklabels(regions)
    ax.axvline(0, color='gray', lw=0.8)
    ax.set_title('6. 蝴蝶图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_06()
def chart_07():
    regions = ['华东','西北','东北','华北','华南']
    p22 = [0.36,0.31,0.18,0.13,0.09]
    p21 = [0.42,0.26,0.19,0.12,0.05]
    fig, ax = plt.subplots(figsize=(10,5))
    y = np.arange(len(regions))
    ax.barh(y, [-v for v in p22], color='#5B9BD5', label='2022年', height=0.4)
    ax.barh(y, p21, color='#ED7D31', label='2021年', height=0.4)
    for i,(a,b) in enumerate(zip(p22,p21)):
        ax.text(-a-0.01, i, f'{a:.0%}', va='center', ha='right', fontsize=9)
        ax.text(b+0.01, i, f'{b:.0%}', va='center', ha='left', fontsize=9)
    ax.set_yticks(y); ax.set_yticklabels(regions)
    ax.axvline(0, color='gray', lw=0.8)
    ax.set_title('7. 蝴蝶图（百分比）', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_07()
def chart_08():
    regions = ['华北','华南','东北','西北','西南','华东']
    sales = [4321,1946,1536,1872,1369,2109]
    yoy = [-0.136,-0.208,-0.093,-0.159,-0.179,-0.058]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(regions)); mx = max(sales)
    ax.bar(x, sales, bottom=[mx-v for v in sales], color='#5B9BD5', width=0.6)
    for i,(v,yv) in enumerate(zip(sales,yoy)):
        ax.text(i, mx+50, str(v), ha='center', fontsize=10, fontweight='bold')
        ax.text(i, mx+160, f'{yv:.1%}', ha='center', fontsize=9,
                color='red' if yv<0 else 'green')
    ax.set_xticks(x); ax.set_xticklabels(regions)
    ax.set_title('8. 数值百分比', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_08()
def chart_09():
    products = ['口红','面膜','隔离','防晒','精华']
    s2021 = [3568,4135,4436,4106,4936]
    s2022 = [2569,3241,2965,3209,3541]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(products)); w = 0.35
    ax.bar(x-w/2, s2021, w, color='#4472C4', label='2021销量')
    ax.bar(x+w/2, s2022, w, color='#ED7D31', label='2022销量')
    for i,(a,b) in enumerate(zip(s2021,s2022)):
        ax.text(i-w/2, a+30, str(a), ha='center', fontsize=9)
        ax.text(i+w/2, b+30, str(b), ha='center', fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(products)
    ax.set_title('9. 对比柱形图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_09()
def chart_10():
    tasks = ['制定计划','方案设计','资源调配','第一阶段','第二阶段','第三阶段','项目总结']
    starts = pd.to_datetime(['2022-03-01','2022-03-13','2022-03-22',
                             '2022-04-02','2022-04-16','2022-05-11','2022-05-26'])
    days = [11,8,10,13,24,14,7]
    prog = [0.51,0.32,0.21,0.85,0.36,0.68,0.68]
    fig, ax = plt.subplots(figsize=(10,5))
    y = np.arange(len(tasks))[::-1]
    for i,(s,d,p) in enumerate(zip(starts,days,prog)):
        ax.barh(y[i], d, left=s, color='#D9E2F3', height=0.6, edgecolor='gray')
        ax.barh(y[i], d*p, left=s, color='#4472C4', height=0.6)
    ax.set_yticks(y); ax.set_yticklabels(tasks)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.set_title('10. 甘特图', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_10()
def chart_11():
    months = ['5月','6月','7月','8月','9月','10月','11月','12月','1月','2月','3月']
    sales = [146,198,296,412,506,615,789,1021,3782,3215,2936]
    fig, ax = plt.subplots(figsize=(10,5))
    x = np.arange(len(months))
    ax.plot(x, sales, color='#4472C4', lw=2.5, marker='o',
            markersize=6, markerfacecolor='white', markeredgewidth=2)
    for i,v in enumerate(sales):
        ax.text(i, v+80, str(v), ha='center', fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(months)
    ax.set_title('11. 平滑折线图', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_11()
def chart_12():
    months = ['1月','2月','3月','4月','5月','6月','7月','8月']
    rates = [0.536,0.498,0.527,0.708,0.609,0.496,0.586,0.704]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(months))
    ax.plot(x, rates, color='#ED7D31', lw=2, marker='D', markersize=10,
            markerfacecolor='#ED7D31', markeredgecolor='white', markeredgewidth=1.5)
    for i,v in enumerate(rates):
        ax.text(i, v+0.015, f'{v:.1%}', ha='center', fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(months)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_title('12. 菱形走势图', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_12()
def chart_13():
    months = ['1月','2月','3月','4月','5月','6月']
    y2021 = [1686,1345,1934,1658,1865,1936]
    y2022 = [1385,1846,1654,1936,2564,2236]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(months))
    ax.plot(x, y2021, color='#4472C4', lw=2, marker='o', label='2021年')
    ax.plot(x, y2022, color='#ED7D31', lw=2, marker='s', label='2022年')
    ax.set_xticks(x); ax.set_xticklabels(months)
    ax.set_title('13. 对比折线图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_13()
def chart_14():
    rate = 0.85
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie([rate, 1-rate], colors=['#4472C4','#E7E6E6'], startangle=90,
           wedgeprops=dict(width=0.3, edgecolor='white'))
    ax.text(0,0,f'{rate:.0%}', ha='center', va='center',
            fontsize=28, fontweight='bold', color='#4472C4')
    ax.set_title('14. 单值圆环图', fontsize=14)
    plt.tight_layout(); plt.show()
chart_14()
def chart_15():
    rate = 0.65
    fig, ax = plt.subplots(figsize=(6,6))
    circle = Circle((0.5,0.5), 0.4, fill=False, edgecolor='#2E75B6', lw=3)
    ax.add_patch(circle)
    x = np.linspace(0,1,500)
    level = 0.1 + 0.8*rate
    ax.fill_between(x, 0.1, level, color='#5B9BD5', alpha=0.8)
    for p in ax.patches:
        p.set_clip_path(circle)
    ax.text(0.5,0.5,f'{rate:.0%}', ha='center', va='center',
            fontsize=28, fontweight='bold', color='#2E75B6')
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('15. 水球图', fontsize=14)
    plt.tight_layout(); plt.show()
chart_15()
def chart_16():
    rate = 0.65
    fig, ax = plt.subplots(figsize=(6,6))
    circle = Circle((0.5,0.5), 0.4, fill=False, edgecolor='#2E75B6', lw=3)
    ax.add_patch(circle)
    x = np.linspace(0,1,500)
    level = 0.1 + 0.8*rate
    wave = level + 0.02*np.sin(2*np.pi*x*4)
    ax.fill_between(x, 0.1, wave, color='#5B9BD5', alpha=0.85)
    for p in ax.patches:
        p.set_clip_path(circle)
    ax.text(0.5,0.5,f'{rate:.0%}', ha='center', va='center',
            fontsize=28, fontweight='bold', color='#2E75B6')
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('16. 波浪水球图', fontsize=14)
    plt.tight_layout(); plt.show()
chart_16()
def chart_17():
    ages = ['>=50','[40,50)','[30,40)','[20,30)']
    pcts = [0.125,0.208333,0.291667,0.375]
    fig, ax = plt.subplots(figsize=(7,7))
    colors = ['#4472C4','#ED7D31','#A5A5A5','#FFC000']
    for i,(a,p,c) in enumerate(zip(ages,pcts,colors)):
        r = 0.2 + i*0.12; w = 0.1
        ax.pie([1], radius=r, colors=['#E7E6E6'],
               wedgeprops=dict(width=w, edgecolor='white'))
        ax.pie([p,1-p], radius=r, colors=[c,'none'], startangle=90,
               counterclock=False, wedgeprops=dict(width=w, edgecolor='white'))
    ax.text(0,0,'年龄\n分布', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.set_title('17. 玉玦图', fontsize=14)
    plt.tight_layout(); plt.show()
chart_17()
def chart_18():
    depts = ['人力部','行政部','财务部','工程部','采购部','销售部']
    counts = [130,226,238,293,326,451]
    fig, ax = plt.subplots(figsize=(9,6))
    y = np.arange(len(depts)); half = sum(counts)/2
    for i,(d,c) in enumerate(zip(depts,counts)):
        ax.barh(y[i], half-c, color='none', height=0.6)
        ax.barh(y[i], c, color=COLORS[i%len(COLORS)], height=0.6)
        ax.text(half+10, y[i], f'{d}  {c}', va='center', fontsize=10)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title('18. 跑道图', fontsize=14)
    plt.tight_layout(); plt.show()
chart_18()
def chart_19():
    depts = ['销售部','采购部','工程部','财务部','行政部','人力部']
    pcts = [0.292,0.227,0.175,0.136,0.103,0.067]
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))
    theta = np.linspace(0, 2*np.pi, len(depts), endpoint=False)
    width = 2*np.pi/len(depts)*0.9
    colors = plt.cm.Set3(np.linspace(0,1,len(depts)))
    ax.bar(theta, pcts, width=width, color=colors, edgecolor='white')
    for t,p,d in zip(theta,pcts,depts):
        ax.text(t, p+0.01, f'{d}\n{p:.1%}', ha='center', va='bottom', fontsize=9)
    ax.set_yticklabels([]); ax.set_xticklabels([])
    ax.set_title('19. 南丁格尔圆饼图', fontsize=14, pad=20)
    plt.tight_layout(); plt.show()
chart_19()
def chart_20():
    ages = ['[20,30)','[30,40)','[40,50)','>=50']
    pcts = [0.375,0.291667,0.208333,0.125]
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))
    theta = np.linspace(0, 2*np.pi, len(ages), endpoint=False)
    width = 2*np.pi/len(ages)*0.9
    colors = ['#4472C4','#ED7D31','#A5A5A5','#FFC000']
    ax.bar(theta, pcts, width=width, color=colors, edgecolor='white')
    ax.bar(theta, [0.06]*len(ages), width=width, color='white', edgecolor='white')
    for t,p,a in zip(theta,pcts,ages):
        ax.text(t, p+0.01, f'{a}\n{p:.1%}', ha='center', va='bottom', fontsize=9)
    ax.set_yticklabels([]); ax.set_xticklabels([])
    ax.set_title('20. 南丁格尔圆环图', fontsize=14, pad=20)
    plt.tight_layout(); plt.show()
chart_20()
def chart_21():
    depts = ['销售部','采购部','工程部','财务部','行政部','人力部']
    pcts = [0.292,0.227,0.175,0.136,0.103,0.05]
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))
    theta = np.linspace(0, 2*np.pi, len(depts), endpoint=False)
    width = 2*np.pi/len(depts)*0.9
    colors = plt.cm.Set3(np.linspace(0,1,len(depts)))
    ax.bar(theta, pcts, width=width, color=colors, edgecolor='white')
    for t,p,d in zip(theta,pcts,depts):
        ax.text(t, p+0.01, f'{d}\n{p:.1%}', ha='center', va='bottom', fontsize=9)
    ax.set_yticklabels([]); ax.set_xticklabels([])
    ax.set_title('21. 南丁格尔图（PPT版）', fontsize=14, pad=20)
    plt.tight_layout(); plt.show()
chart_21()
def chart_22():
    value = 76; min_v, max_v = 50, 150
    fig, ax = plt.subplots(figsize=(8,6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi); ax.set_theta_direction(-1)
    for t in range(50,151,10):
        a = (t-min_v)/(max_v-min_v)*np.pi
        ax.plot([a,a],[0.8,1.0], color='gray', lw=1)
        ax.text(a,1.15,str(t), ha='center', va='center', fontsize=8)
    a = (value-min_v)/(max_v-min_v)*np.pi
    ax.annotate('', xy=(a,0.9), xytext=(0,0),
                arrowprops=dict(arrowstyle='-|>', color='red', lw=3))
    ax.plot(0,0,'o', color='red', markersize=15)
    theta = np.linspace(0, np.pi, 100)
    ax.plot(theta, [1]*100, color='#4472C4', lw=5)
    ax.set_ylim(0,1.3); ax.set_yticklabels([]); ax.set_xticklabels([])
    ax.set_title(f'22. 仪表盘图  当前值: {value}', fontsize=14, pad=20)
    plt.tight_layout(); plt.show()
chart_22()
def chart_23():
    years = [2017,2018,2019,2020,2021,2022]
    sales = [1603,2106,2406,3265,3721,3921]
    yoy = [0.27] + [sales[i]/sales[i-1]-1 for i in range(1,len(sales))]
    fig, ax1 = plt.subplots(figsize=(9,5))
    x = np.arange(len(years))
    ax1.bar(x, sales, color='#4472C4', width=0.5, label='销售量')
    ax1.set_ylabel('销售量', color='#4472C4')
    for i,v in enumerate(sales):
        ax1.text(i, v+50, str(v), ha='center', fontsize=9, color='#4472C4')
    ax2 = ax1.twinx()
    ax2.plot(x, yoy, color='#ED7D31', lw=2, marker='o', label='同比')
    ax2.set_ylabel('同比', color='#ED7D31')
    for i,v in enumerate(yoy):
        ax2.text(i, v+0.02, f'{v:.1%}', ha='center', fontsize=9, color='#ED7D31')
    ax1.set_xticks(x); ax1.set_xticklabels(years)
    ax1.set_title('23. 柱形折线图', fontsize=14)
    plt.tight_layout(); plt.show()
chart_23()
def chart_24():
    products = ['口红','面膜','隔离','防晒','精华','面霜']
    actual = [653,523,648,856,714,785]
    target = [700,500,600,900,600,600]
    rate = [a/t for a,t in zip(actual,target)]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(products))
    ax.bar(x, target, color='#D9E2F3', width=0.6, label='目标销量')
    ax.bar(x, actual, color='#4472C4', width=0.6, label='实际销量')
    for i,(a,t,r) in enumerate(zip(actual,target,rate)):
        ax.text(i, max(a,t)+30, f'{r:.1%}', ha='center', fontsize=9,
                color='green' if r>=1 else 'red')
    ax.set_xticks(x); ax.set_xticklabels(products)
    ax.set_title('24. 目标柱形图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_24()
def chart_25():
    products = ['口红','面膜','隔离','防晒','精华','面霜']
    actual = [653,523,648,856,714,785]
    target = [700,500,600,900,600,600]
    fig, ax = plt.subplots(figsize=(9,5))
    y = np.arange(len(products))[::-1]
    for i,(a,t) in enumerate(zip(actual,target)):
        ax.barh(y[i], t, color='#D9E2F3', height=0.5, label='目标' if i==0 else '')
        ax.barh(y[i], a, color='#4472C4', height=0.25,
                label='实际' if i==0 else '')
        ax.plot([t,t], [y[i]-0.25, y[i]+0.25], color='red', lw=2,
                label='目标线' if i==0 else '')
    ax.set_yticks(y); ax.set_yticklabels(products)
    ax.set_title('25. 子弹图', fontsize=14)
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_25()
def chart_26():
    regions = ['华北','华南','东北','西北','西南','华东']
    sales = [2354,1902,3524,2698,2896,2563]
    yoy = [0.12,0.25,0.16,0.21,0.18,0.25]
    fig, ax = plt.subplots(figsize=(10,6))
    x = np.arange(len(regions))
    bars = ax.bar(x, sales, color='#5B9BD5', width=0.6)
    for i,(b,v,yv) in enumerate(zip(bars,sales,yoy)):
        ax.text(b.get_x()+b.get_width()/2, v+50, str(v),
                ha='center', fontsize=10)
        ax.scatter(b.get_x()+b.get_width()/2, v+250, s=400,
                   color='#ED7D31', zorder=5)
        ax.text(b.get_x()+b.get_width()/2, v+250, f'{yv:.0%}',
                ha='center', va='center', fontsize=8, color='white', zorder=6)
    ax.set_xticks(x); ax.set_xticklabels(regions)
    ax.set_title('26. 柱形圆', fontsize=14)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.show()
chart_26()
def chart_27():
    regions = ['华北','华南','东北','西北','西南','华东']
    s2022 = [2354,1902,3524,2698,2896,2563]
    s2021 = [2021,1563,3213,2531,2631,2361]
    yoy = [0.16,0.22,0.10,0.07,0.10,0.09]
    fig, ax1 = plt.subplots(figsize=(10,5))
    x = np.arange(len(regions)); w = 0.35
    ax1.bar(x-w/2, s2022, w, color='#4472C4', label='2022销量')
    ax1.bar(x+w/2, s2021, w, color='#A5A5A5', label='2021销量')
    ax1.set_ylabel('销量')
    ax2 = ax1.twinx()
    ax2.plot(x, yoy, color='#ED7D31', lw=2, marker='o', label='同比去年')
    ax2.set_ylabel('同比', color='#ED7D31')
    for i,v in enumerate(yoy):
        ax2.text(i, v+0.005, f'{v:.0%}', ha='center', fontsize=9, color='#ED7D31')
    ax1.set_xticks(x); ax1.set_xticklabels(regions)
    ax1.set_title('27. 簇状柱形折线图', fontsize=14)
    h1,l1 = ax1.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='upper left')
    plt.tight_layout(); plt.show()
chart_27()
def chart_28():
    months = ['1月','2月','3月','4月','5月','6月',
              '7月','8月','9月','10月','11月','12月']
    monthly = [2354,1902,3524,2698,2896,2563,
               3156,2896,3621,2635,2963,2789]
    quarterly = []
    for i in range(0, 12, 3):
        q = sum(monthly[i:i+3])
        quarterly.extend([q, q, q])   
    fig, ax1 = plt.subplots(figsize=(12, 6))
    x = np.arange(len(months))
    ax1.bar(x, quarterly, color='#D9E2F3', width=0.8,
            label='季度销量', edgecolor='#B4C7E7')
    ax1.bar(x, monthly, color='#4472C4', width=0.4,
            label='月度销量')
    for i, v in enumerate(monthly):
        ax1.text(i, v + 40, str(v), ha='center', fontsize=8, color='#264478')
    for qi, i in enumerate([1, 4, 7, 10]):
        qv = quarterly[i]
        ax1.text(i, qv + 120, f'季度: {qv}', ha='center', fontsize=9,
                 color='#2E75B6', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(months)
    ax1.set_title('28. 复合柱形图（月度 + 季度）', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.spines[['top','right']].set_visible(False)
    plt.tight_layout()
    plt.show()
chart_28()
def chart_29():
    regions = ['华东','西北','东北','华北','华南']
    rates = [0.35, 0.51, 0.62, 0.74, 0.86]
    unfinished = [1 - r for r in rates]
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(regions))
    ax.barh(y, unfinished, left=rates, color='#E7E6E6',
            height=0.5, label='未完成占比')
    ax.scatter(rates, y, s=300, color='#ED7D31', zorder=5,
               edgecolor='white', linewidth=2, label='完成率')
    for i, r in enumerate(rates):
        ax.text(r - 0.03, i, f'{r:.0%}', ha='right', va='center',
                fontsize=10, color='white', fontweight='bold', zorder=6)
    ax.set_yticks(y)
    ax.set_yticklabels(regions)
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_title('29. 滑珠图', fontsize=14)
    ax.legend(loc='lower right')
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout()
    plt.show()
chart_29()
def chart_30():
    regions = ['华东','西北','东北','华北','华南']
    r2022 = [0.35, 0.51, 0.62, 0.74, 0.86]
    r2021 = [0.45, 0.39, 0.53, 0.69, 0.92]
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (a, b) in enumerate(zip(r2021, r2022)):
        ax.plot([a, b], [i, i], color='#BFBFBF', lw=2, zorder=1)
        ax.scatter(a, i, s=280, color='#A5A5A5', zorder=3,
                   edgecolor='white', linewidth=2)
        ax.text(a, i - 0.22, f'{a:.0%}', ha='center', va='top',
                fontsize=9, color='#636363')
        ax.scatter(b, i, s=280, color='#ED7D31', zorder=4,
                   edgecolor='white', linewidth=2)
        ax.text(b, i + 0.22, f'{b:.0%}', ha='center', va='bottom',
                fontsize=9, color='#C55A11', fontweight='bold')
        arrow = '↑' if b > a else '↓'
        color = 'green' if b > a else 'red'
        ax.text(max(a, b) + 0.03, i, arrow, fontsize=14,
                color=color, va='center')
    ax.set_yticks(range(len(regions)))
    ax.set_yticklabels(regions)
    ax.set_xlim(0.2, 1.0)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_title('30. 对比滑珠图（2021 vs 2022 完成率）', fontsize=14)
    ax.scatter([], [], s=200, color='#A5A5A5', label='2021完成率')
    ax.scatter([], [], s=200, color='#ED7D31', label='2022完成率')
    ax.legend(loc='lower right')
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout()
    plt.show()
chart_30()
