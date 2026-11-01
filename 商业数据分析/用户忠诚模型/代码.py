import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 读取Excel（自动读取"销售流水表"这个sheet）
# ============================================================
FILE = '1-3用户忠诚度模型.xlsx'   # 改成你的实际路径

# sheet_index_num=2 表示第3个sheet（业务背景是第1个，销售流水是第2个有数据的）
xls = pd.ExcelFile(FILE)
print("📑 文件中的Sheet：", xls.sheet_names)

# 自动找到"销售流水表"
sheet = '销售流水表'
df = pd.read_excel(FILE, sheet_name=sheet, parse_dates=['消费日期'])

print(f"✅ 原始数据：{len(df)} 行")
print(f"   字段：{df.columns.tolist()}")
print(f"   日期范围：{df['消费日期'].min().date()} ~ {df['消费日期'].max().date()}")
print(f"   用户数：{df['会员编号'].nunique()}")
print(f"   订单数：{df['订单编号'].nunique()}")
print("=" * 60)

# ============================================================
# 2. 数据预处理
# ============================================================
df = df.copy()
df = df.drop_duplicates(subset=['订单编号', '产品编号'])
df['消费金额'] = pd.to_numeric(df['消费金额'], errors='coerce')
df = df[df['消费金额'] > 0]
df = df.dropna(subset=['会员编号', '消费日期'])
print(f"清洗后数据：{len(df)} 行，用户 {df['会员编号'].nunique()} 个")

# ============================================================
# 3. RFM 模型
# ============================================================
snapshot = df['消费日期'].max() + pd.Timedelta(days=1)

rfm = df.groupby('会员编号').agg(
    R=('消费日期', lambda x: (snapshot - x.max()).days),
    F=('订单编号', 'nunique'),
    M=('消费金额', 'sum')
).reset_index()

# 打分（rank + qcut，防止重复值报错）
rfm['R_score'] = pd.qcut(rfm['R'].rank(method='first'), 5, labels=[5,4,3,2,1]).astype(int)
rfm['F_score'] = pd.qcut(rfm['F'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['M_score'] = pd.qcut(rfm['M'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['RFM_score'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

# ============================================================
# 4. 忠诚度分层
# ============================================================
def seg(s):
    if s >= 13: return '高忠诚用户'
    if s >= 10: return '中忠诚用户'
    if s >= 7:  return '低忠诚用户'
    return '流失风险用户'

rfm['忠诚度分层'] = rfm['RFM_score'].apply(seg)

# ============================================================
# 5. 分层指标
# ============================================================
df_merge = df.merge(rfm[['会员编号','忠诚度分层']], on='会员编号', how='left')

metrics = df_merge.groupby('忠诚度分层').agg(
    用户数=('会员编号','nunique'),
    总消费额=('消费金额','sum'),
    总订单数=('订单编号','nunique'),
    平均客单价=('消费金额','mean')
).reset_index()

metrics['用户占比'] = metrics['用户数'] / metrics['用户数'].sum()
metrics['销售额占比'] = metrics['总消费额'] / metrics['总消费额'].sum()
metrics['人均消费'] = metrics['总消费额'] / metrics['用户数']
metrics = metrics.sort_values('总消费额', ascending=False).reset_index(drop=True)

# ============================================================
# 6. 复购分析
# ============================================================
users = df.groupby('会员编号').agg(
    订单数=('订单编号','nunique'),
    首单=('消费日期','min'),
    末单=('消费日期','max'),
    总金额=('消费金额','sum')
).reset_index()

users['复购次数'] = users['订单数'] - 1
users['是否复购'] = (users['订单数'] > 1).astype(int)
users['生命周期天数'] = (users['末单'] - users['首单']).dt.days

repurchase_rate = users['是否复购'].mean()

# ============================================================
# 7. 打印分析结果
# ============================================================
print("\n" + "=" * 60)
print("【一、整体概况】")
print("=" * 60)
print(f"总用户数        : {rfm.shape[0]}")
print(f"总订单数        : {df['订单编号'].nunique()}")
print(f"总销售额        : {df['消费金额'].sum():.2f}")
print(f"平均客单价      : {df['消费金额'].mean():.2f}")
print(f"人均消费        : {df['消费金额'].sum() / rfm.shape[0]:.2f}")
print(f"整体复购率      : {repurchase_rate:.2%}")
print(f"平均复购次数    : {users['复购次数'].mean():.2f}")
print(f"平均生命周期    : {users['生命周期天数'].mean():.1f} 天")

print("\n" + "=" * 60)
print("【二、忠诚度分层概况】")
print("=" * 60)
cols = ['忠诚度分层','用户数','用户占比','总消费额','销售额占比','人均消费','平均客单价']
print(metrics[cols].round(2).to_string(index=False))

print("\n" + "=" * 60)
print("【三、RFM 分数概况】")
print("=" * 60)
print(rfm[['R','F','M','RFM_score']].describe().round(2).to_string())

print("\n" + "=" * 60)
print("【四、高价值用户 TOP10（按消费金额）】")
print("=" * 60)
top10 = rfm.sort_values('M', ascending=False).head(10)
print(top10[['会员编号','R','F','M','RFM_score','忠诚度分层']].to_string(index=False))

print("\n" + "=" * 60)
print("【五、复购间隔分析（复购用户）】")
print("=" * 60)
repeat_users = users[users['复购次数'] > 0]
if len(repeat_users) > 0:
    print(f"复购用户数：{len(repeat_users)}")
    print(f"平均生命周期：{repeat_users['生命周期天数'].mean():.1f} 天")
    print(f"平均订单数：{repeat_users['订单数'].mean():.2f}")

# ============================================================
# 8. 可视化 - 6张图
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
colors = ['#C44E52','#DD8452','#55A868','#4C72B0']  # 高→流失 用渐变

# 图1：各分层用户数
ax = axes[0,0]
ax.bar(metrics['忠诚度分层'], metrics['用户数'], color=colors[:len(metrics)])
ax.set_title('各忠诚度分层用户数', fontsize=13, fontweight='bold')
ax.set_ylabel('用户数')
for i, v in enumerate(metrics['用户数']):
    ax.text(i, v, f'{v}', ha='center', va='bottom', fontsize=10)

# 图2：销售额占比饼图
ax = axes[0,1]
ax.pie(metrics['销售额占比'], labels=metrics['忠诚度分层'],
       autopct='%1.1f%%', colors=colors[:len(metrics)], startangle=90,
       textprops={'fontsize':10})
ax.set_title('各分层销售额占比', fontsize=13, fontweight='bold')

# 图3：RFM总分分布
ax = axes[0,2]
ax.hist(rfm['RFM_score'], bins=range(3,17), color='steelblue', edgecolor='black')
ax.set_title('RFM总分分布', fontsize=13, fontweight='bold')
ax.set_xlabel('RFM Score')
ax.set_ylabel('用户数')

# 图4：复购次数分布
ax = axes[1,0]
maxrp = min(int(users['复购次数'].max())+2, 30)
ax.hist(users['复购次数'], bins=range(0, max(maxrp,10)), color='coral', edgecolor='black')
ax.set_title('用户复购次数分布', fontsize=13, fontweight='bold')
ax.set_xlabel('复购次数')
ax.set_ylabel('用户数')

# 图5：R/F/M 三维散点（用气泡表示金额）
ax = axes[1,1]
sc = ax.scatter(rfm['R'], rfm['F'], s=rfm['M']/rfm['M'].max()*300+10,
                c=rfm['RFM_score'], cmap='RdYlGn', alpha=0.6, edgecolors='k', linewidths=0.5)
ax.set_xlabel('R（最近消费天数，越小越好）')
ax.set_ylabel('F（消费频次）')
ax.set_title('R-F分布（气泡大小=消费金额）', fontsize=13, fontweight='bold')
ax.invert_xaxis()
plt.colorbar(sc, ax=ax, label='RFM得分')

# 图6：各分层人均消费 vs 平均客单价
ax = axes[1,2]
x = np.arange(len(metrics))
w = 0.35
ax.bar(x - w/2, metrics['人均消费'], w, label='人均消费', color='#4C72B0')
ax.bar(x + w/2, metrics['平均客单价'], w, label='平均客单价', color='#DD8452')
ax.set_xticks(x)
ax.set_xticklabels(metrics['忠诚度分层'])
ax.set_title('各分层人均消费 vs 平均客单价', fontsize=13, fontweight='bold')
ax.legend()

plt.tight_layout()
plt.savefig('忠诚度分析报告.png', dpi=120, bbox_inches='tight')
print("\n📊 图表已保存：忠诚度分析报告.png")
plt.show()
