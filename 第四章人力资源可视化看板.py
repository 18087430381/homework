import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re

rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')
df = pd.read_excel(r'C:\Users\x1808\Desktop\第四章 人力资源可视化看板.xlsx', sheet_name='202203人员基础信息')
print(f"总员工数: {len(df)}")
print(f"列名: {list(df.columns)}")
print(df.head())
df = df.dropna(subset=['员工编号'])
df['员工编号'] = df['员工编号'].astype(str)
total = len(df)
print("\n" + "=" * 60)
print(f"【卡片图】总人数：{total}")
print("=" * 60)
age_order = ['18-24', '25-29', '30-34', '35-39', '40=<']
age_counts = df['年龄段'].value_counts().reindex(age_order, fill_value=0)
age_pct = age_counts / total * 100
print("\n【年龄段分布】")
for k, v in age_counts.items():
    print(f"  {k}: {v}人 ({v/total:.1%})")
gender_counts = df['性别'].value_counts()
print("\n【性别分布】")
for k, v in gender_counts.items():
    print(f"  {k}: {v}人 ({v/total:.1%})")
edu_order = ['专科以下', '专科', '本科', '硕士研究生', '博士研究生']
edu_counts = df['学历'].value_counts().reindex(edu_order, fill_value=0)
print("\n【学历分布】")
for k, v in edu_counts.items():
    print(f"  {k}: {v}人 ({v/total:.1%})")
marriage_order = ['单身', '已婚', '离异']
marriage_counts = df['婚姻状况'].value_counts().reindex(marriage_order, fill_value=0)
print("\n【婚姻状况分布】")
for k, v in marriage_counts.items():
    print(f"  {k}: {v}人 ({v/total:.1%})")
dept_counts = df['部门'].value_counts()
print("\n【部门分布】")
for k, v in dept_counts.items():
    print(f"  {k}: {v}人 ({v/total:.1%})")
turnover_order = ['入职', '转入', '转出']
turnover_counts = df['本月入转调'].value_counts().reindex(turnover_order, fill_value=0)
print("\n【本月入转调】")
for k, v in turnover_counts.items():
    print(f"  {k}: {v}人")
print("\n【部门 x 学历 交叉表】")
cross_dept_edu = pd.crosstab(df['部门'], df['学历'])
print(cross_dept_edu)
print("\n【年龄段 x 性别 交叉表】")
cross_age_gender = pd.crosstab(df['年龄段'], df['性别']).reindex(age_order)
print(cross_age_gender)
fig = plt.figure(figsize=(18, 14))
fig.suptitle(f'人力资源可视化看板  |  总人数：{total}人', 
             fontsize=18, fontweight='bold', y=0.98)
ax1 = fig.add_subplot(3, 3, 1)
bars = ax1.bar(age_counts.index, age_counts.values, color='#4472C4')
ax1.set_title('年龄段分布', fontweight='bold')
ax1.set_ylabel('人数')
for bar, v in zip(bars, age_counts.values):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, 
             str(v), ha='center', fontsize=10)
ax2 = fig.add_subplot(3, 3, 2)
ax2.pie(gender_counts.values, labels=gender_counts.index, 
        autopct='%1.1f%%', startangle=90,
        colors=['#5B9BD5', '#ED7D31'])
ax2.set_title('性别分布', fontweight='bold')
ax3 = fig.add_subplot(3, 3, 3)
bars = ax3.barh(edu_counts.index, edu_counts.values, color='#70AD47')
ax3.set_title('学历分布', fontweight='bold')
ax3.set_xlabel('人数')
for bar, v in zip(bars, edu_counts.values):
    ax3.text(bar.get_width()+2, bar.get_y()+bar.get_height()/2,
             str(v), va='center', fontsize=10)
ax4 = fig.add_subplot(3, 3, 4)
ax4.pie(marriage_counts.values, labels=marriage_counts.index,
        autopct='%1.1f%%', startangle=90,
        colors=['#FFC000', '#A5A5A5', '#5B9BD5'])
ax4.set_title('婚姻状况分布', fontweight='bold')
ax5 = fig.add_subplot(3, 3, 5)
bars = ax5.bar(dept_counts.index, dept_counts.values, color='#ED7D31')
ax5.set_title('部门人员分布', fontweight='bold')
ax5.set_ylabel('人数')
ax5.tick_params(axis='x', rotation=15)
for bar, v in zip(bars, dept_counts.values):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2,
             str(v), ha='center', fontsize=10)
ax6 = fig.add_subplot(3, 3, 6)
bars = ax6.bar(turnover_counts.index, turnover_counts.values,
               color=['#70AD47', '#4472C4', '#C00000'])
ax6.set_title('本月入转调', fontweight='bold')
ax6.set_ylabel('人数')
for bar, v in zip(bars, turnover_counts.values):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
             str(v), ha='center', fontsize=11, fontweight='bold')
ax7 = fig.add_subplot(3, 3, 7)
cross_dept_edu.plot(kind='bar', stacked=True, ax=ax7, 
                     colormap='Set2', width=0.7)
ax7.set_title('部门 x 学历 分布', fontweight='bold')
ax7.set_ylabel('人数')
ax7.tick_params(axis='x', rotation=15)
ax7.legend(loc='upper right', fontsize=8)
ax8 = fig.add_subplot(3, 3, 8)
x = np.arange(len(cross_age_gender))
width = 0.35
ax8.bar(x - width/2, cross_age_gender['男'], width, label='男', color='#5B9BD5')
ax8.bar(x + width/2, cross_age_gender['女'], width, label='女', color='#ED7D31')
ax8.set_xticks(x)
ax8.set_xticklabels(cross_age_gender.index)
ax8.set_title('年龄段 x 性别', fontweight='bold')
ax8.set_ylabel('人数')
ax8.legend()
ax9 = fig.add_subplot(3, 3, 9)
wedges, texts, autotexts = ax9.pie(
    age_counts.values, labels=age_counts.index,
    autopct='%1.1f%%', startangle=90,
    colors=plt.cm.Set3.colors, pctdistance=0.75,
    wedgeprops=dict(width=0.4, edgecolor='w'))
ax9.set_title('年龄段占比（环形图）', fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('人力资源看板.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n【各部门平均年龄】")
avg_age = df.groupby('部门')['年龄'].agg(['mean', 'min', 'max', 'count']).round(1)
avg_age.columns = ['平均年龄', '最小年龄', '最大年龄', '人数']
print(avg_age.sort_values('平均年龄', ascending=False))
print("\n【各学历平均年龄】")
edu_age = df.groupby('学历')['年龄'].agg(['mean', 'count']).round(1)
edu_age.columns = ['平均年龄', '人数']
print(edu_age.reindex(edu_order))
fig2, axes = plt.subplots(1, 2, figsize=(15, 6))
avg_age_sorted = avg_age.sort_values('平均年龄')
bars = axes[0].barh(avg_age_sorted.index, avg_age_sorted['平均年龄'], 
                     color='#4472C4')
axes[0].set_title('各部门平均年龄', fontweight='bold')
axes[0].set_xlabel('平均年龄')
for bar, v in zip(bars, avg_age_sorted['平均年龄']):
    axes[0].text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2,
                 f'{v:.1f}', va='center', fontsize=10)
edu_age_sorted = edu_age.reindex(edu_order).dropna()
bars = axes[1].bar(edu_age_sorted.index, edu_age_sorted['平均年龄'],
                    color='#70AD47')
axes[1].set_title('各学历平均年龄', fontweight='bold')
axes[1].set_ylabel('平均年龄')
axes[1].tick_params(axis='x', rotation=15)
for bar, v in zip(bars, edu_age_sorted['平均年龄']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                 f'{v:.1f}', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('人力资源高级分析.png', dpi=120, bbox_inches='tight')
plt.show()
print("\n" + "=" * 60)
print("关键结论")
print("=" * 60)
print(f"1. 总人数: {total}人")
print(f"2. 性别比例: 男 {gender_counts.get('男',0)} : 女 {gender_counts.get('女',0)} "
      f"(约 {gender_counts.get('男',0)/total:.0%} : {gender_counts.get('女',0)/total:.0%})")
print(f"3. 年龄段主力: {age_counts.idxmax()} (共{age_counts.max()}人, 占{age_counts.max()/total:.1%})")
print(f"4. 学历主力: {edu_counts.idxmax()} (共{edu_counts.max()}人, 占{edu_counts.max()/total:.1%})")
print(f"5. 人数最多部门: {dept_counts.idxmax()} (共{dept_counts.max()}人)")
print(f"6. 婚姻状况主力: {marriage_counts.idxmax()} (共{marriage_counts.max()}人)")
print(f"7. 本月入职: {turnover_counts.get('入职',0)}人, "
      f"转入: {turnover_counts.get('转入',0)}人, "
      f"转出: {turnover_counts.get('转出',0)}人")
print(f"8. 全公司平均年龄: {df['年龄'].mean():.1f}岁")
print(f"9. 平均年龄最高部门: {avg_age['平均年龄'].idxmax()} ({avg_age['平均年龄'].max():.1f}岁)")
print(f"10. 平均年龄最低部门: {avg_age['平均年龄'].idxmin()} ({avg_age['平均年龄'].min():.1f}岁)")
