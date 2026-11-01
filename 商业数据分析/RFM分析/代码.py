import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


# ============================================================
# 全局设置
# ============================================================
# 中文显示（Windows 用 SimHei；Mac 改成 PingFang SC）
rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
rcParams["axes.unicode_minus"] = False

# 业务类别固定顺序
CATEGORY_ORDER = [
    "重要价值用户", "重要发展用户", "重要保持用户", "重要挽留用户",
    "一般价值用户", "一般发展用户", "一般保持用户", "一般挽留用户",
]


# ============================================================
# 1. 读取数据
# ============================================================
file_path = "1-2RFM模型.xlsx"

df = pd.read_excel(file_path, sheet_name="原始数据")
df.columns = [c.strip() for c in df.columns]

print("原始数据形状:", df.shape)
print(df.head())


# ============================================================
# 2. 数据清洗
# ============================================================
df["用户编号"] = df["用户编号"].astype(str).str.strip()
df["销售日期"] = pd.to_datetime(df["销售日期"], errors="coerce")
df["销售金额"] = pd.to_numeric(df["销售金额"], errors="coerce")

df = df.dropna(subset=["用户编号", "销售日期", "销售金额"])
df = df[df["销售金额"] > 0]

print("\n清洗后数据形状:", df.shape)
print("用户数:", df["用户编号"].nunique())
print("时间范围:", df["销售日期"].min().date(), "~", df["销售日期"].max().date())


# ============================================================
# 3. 计算 R / F / M
# ============================================================
snapshot_date = df["销售日期"].max() + pd.Timedelta(days=1)
print("\n观测截止日期:", snapshot_date.date())

rfm = df.groupby("用户编号").agg(
    R=("销售日期", lambda x: (snapshot_date - x.max()).days),
    F=("销售日期", "nunique"),
    M=("销售金额", "sum")
).reset_index()

print("\nRFM 指标描述：")
print(rfm[["R", "F", "M"]].describe())


# ============================================================
# 4. RFM 打分
#    - R：分位法反向打分（越小越好）
#    - F：业务规则分档（复购率低，分位法区分度不足）
#    - M：分位法正向打分（越大越好）
# ============================================================
def score_by_quantile(x, ascending=True, q=5):
    """稳健分位数打分（绕开 qcut 的 labels 校验）"""
    s = pd.Series(x).reset_index(drop=True)

    if s.nunique() <= 1:
        return pd.Series([3] * len(s), dtype=int)

    quantiles = np.linspace(0, 1, q + 1)
    edges = np.unique(s.quantile(quantiles).values)
    n_bins = len(edges) - 1
    if n_bins < 1:
        return pd.Series([3] * len(s), dtype=int)

    edges = edges.astype(float)
    edges[0] -= 1e-9
    edges[-1] += 1e-9

    idx = np.digitize(s.values, edges, right=False)

    if n_bins >= 5:
        scores = np.clip(idx, 1, 5)
    else:
        scores = np.round(1 + (idx - 1) * 4 / max(n_bins - 1, 1)).astype(int)
        scores = np.clip(scores, 1, 5)

    if not ascending:
        scores = 6 - scores

    return pd.Series(scores, dtype=int)


def score_frequency_by_rule(f):
    """F 业务规则分档：1/2/3/4/≥5 次 → 1~5 分"""
    if f <= 1:   return 1
    elif f == 2: return 2
    elif f == 3: return 3
    elif f == 4: return 4
    else:        return 5


rfm["R_score"] = score_by_quantile(rfm["R"], ascending=False)
rfm["F_score"] = rfm["F"].apply(score_frequency_by_rule)
rfm["M_score"] = score_by_quantile(rfm["M"], ascending=True)

print("\n各维度评分分布：")
for col in ["R_score", "F_score", "M_score"]:
    print(f"\n{col}:")
    print(rfm[col].value_counts().sort_index())


# ============================================================
# 5. 高低划分 + 用户分类
# ============================================================
def high_low(score):
    return "高" if score >= 3 else "低"


rfm["R_程度"] = rfm["R_score"].apply(high_low)
rfm["F_程度"] = rfm["F_score"].apply(high_low)
rfm["M_程度"] = rfm["M_score"].apply(high_low)

category_map = {
    ("高", "高", "高"): "重要价值用户",
    ("高", "低", "高"): "重要发展用户",
    ("低", "高", "高"): "重要保持用户",
    ("低", "低", "高"): "重要挽留用户",
    ("高", "高", "低"): "一般价值用户",
    ("高", "低", "低"): "一般发展用户",
    ("低", "高", "低"): "一般保持用户",
    ("低", "低", "低"): "一般挽留用户",
}

rfm["用户类别"] = rfm.apply(
    lambda row: category_map[(row["R_程度"], row["F_程度"], row["M_程度"])],
    axis=1
)


# ============================================================
# 6. 汇总统计
# ============================================================
# 6.1 用户类别分布
summary = rfm["用户类别"].value_counts().reset_index()
summary.columns = ["用户类别", "用户数"]
summary["占比(%)"] = (summary["用户数"] / len(rfm) * 100).round(2)
summary["排序"] = summary["用户类别"].apply(CATEGORY_ORDER.index)
summary = summary.sort_values("排序").drop(columns="排序").reset_index(drop=True)

print("\n===== 用户类别分布 =====")
print(summary)

# 6.2 各类别 RFM 均值/中位数/人数
profile = (
    rfm.groupby("用户类别")[["R", "F", "M"]]
       .agg(["mean", "median", "count"])
       .round(2)
)
print("\n===== 各类别 RFM 统计 =====")
print(profile)

# 6.3 金额占比
m_share = rfm.groupby("用户类别")["M"].sum().reset_index()
m_share.columns = ["用户类别", "消费总额"]
m_share["金额占比(%)"] = (m_share["消费总额"] / m_share["消费总额"].sum() * 100).round(2)
m_share["排序"] = m_share["用户类别"].apply(CATEGORY_ORDER.index)
m_share = m_share.sort_values("排序").drop(columns="排序").reset_index(drop=True)
print("\n===== 各类别消费金额占比 =====")
print(m_share)


# ============================================================
# 7. 导出 Excel（4 个 Sheet）
# ============================================================
output_path = "RFM分析结果.xlsx"

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    rfm.to_excel(writer, sheet_name="用户RFM明细", index=False)
    summary.to_excel(writer, sheet_name="用户类别分布", index=False)
    profile.to_excel(writer, sheet_name="各类别RFM均值")
    m_share.to_excel(writer, sheet_name="金额占比", index=False)

print(f"\n✅ 表数据已导出: {output_path}")


# ============================================================
# 8. 可视化（4 张 PNG）
# ============================================================
# 图1：用户数量分布
fig, ax = plt.subplots(figsize=(10, 5))
plot_df = summary.set_index("用户类别").reindex(CATEGORY_ORDER).dropna()
bars = ax.barh(plot_df.index[::-1], plot_df["用户数"][::-1], color="#4C72B0")
for b in bars:
    ax.text(b.get_width() + 0.5, b.get_y() + b.get_height() / 2,
            f"{int(b.get_width())}", va="center", fontsize=9)
ax.set_xlabel("用户数")
ax.set_title("各用户类别人数分布")
plt.tight_layout()
plt.savefig("图1_用户数量分布.png", dpi=150)
plt.show()

# 图2：金额贡献饼图
fig, ax = plt.subplots(figsize=(8, 8))
pie_df = m_share.set_index("用户类别").reindex(CATEGORY_ORDER).dropna()
ax.pie(pie_df["消费总额"], labels=pie_df.index, autopct="%1.1f%%",
       startangle=90, counterclock=False,
       colors=plt.cm.Set3.colors[:len(pie_df)])
ax.set_title("各类别消费金额贡献占比")
plt.tight_layout()
plt.savefig("图2_金额占比饼图.png", dpi=150)
plt.show()

# 图3：RFM 归一化均值对比
fig, ax = plt.subplots(figsize=(12, 5))
prof = rfm.groupby("用户类别")[["R", "F", "M"]].mean().reindex(CATEGORY_ORDER).dropna()
prof_norm = prof.copy()
for c in ["R", "F", "M"]:
    v = prof_norm[c]
    prof_norm[c] = (v - v.min()) / (v.max() - v.min() + 1e-9)

x = np.arange(len(prof_norm))
w = 0.25
ax.bar(x - w, prof_norm["R"], w, label="R（越小越好）", color="#DD8452")
ax.bar(x,     prof_norm["F"], w, label="F", color="#55A868")
ax.bar(x + w, prof_norm["M"], w, label="M", color="#4C72B0")
ax.set_xticks(x)
ax.set_xticklabels(prof_norm.index, rotation=30, ha="right")
ax.set_ylabel("归一化均值")
ax.set_title("各类别 RFM 归一化均值对比")
ax.legend()
plt.tight_layout()
plt.savefig("图3_RFM对比.png", dpi=150)
plt.show()

# 图4：人数 vs 金额散点（气泡大小=人均消费）
fig, ax = plt.subplots(figsize=(10, 6))
merge = summary.merge(m_share, on="用户类别").set_index("用户类别").reindex(CATEGORY_ORDER).dropna()
merge["人均消费"] = merge["消费总额"] / merge["用户数"]
ax.scatter(merge["用户数"], merge["消费总额"],
           s=merge["人均消费"] / 5, alpha=0.6, color="#C44E52")
for name, row in merge.iterrows():
    ax.annotate(name, (row["用户数"], row["消费总额"]),
                fontsize=8, xytext=(5, 5), textcoords="offset points")
ax.set_xlabel("用户数")
ax.set_ylabel("消费总额")
ax.set_title("用户类别：人数 vs 消费总额（气泡大小=人均消费）")
plt.tight_layout()
plt.savefig("图4_人数与金额散点.png", dpi=150)
plt.show()

print("\n✅ 4 张图已保存为 PNG")


# ============================================================
# 9. 图表嵌入 Excel
# ============================================================
from openpyxl import load_workbook
from openpyxl.chart import BarChart, PieChart, Reference

wb = load_workbook(output_path)

# 图1：用户数柱状图 → 用户类别分布 Sheet
ws1 = wb["用户类别分布"]
data1 = Reference(ws1, min_col=2, min_row=1, max_row=len(summary) + 1)
cats1 = Reference(ws1, min_col=1, min_row=2, max_row=len(summary) + 1)
chart1 = BarChart()
chart1.title = "各用户类别人数"
chart1.add_data(data1, titles_from_data=True)
chart1.set_categories(cats1)
chart1.y_axis.title = "用户数"
ws1.add_chart(chart1, "F2")

# 图2：金额占比饼图 → 金额占比 Sheet
ws2 = wb["金额占比"]
data2 = Reference(ws2, min_col=2, min_row=1, max_row=len(m_share) + 1)
cats2 = Reference(ws2, min_col=1, min_row=2, max_row=len(m_share) + 1)
chart2 = PieChart()
chart2.title = "各类别消费金额占比"
chart2.add_data(data2, titles_from_data=True)
chart2.set_categories(cats2)
ws2.add_chart(chart2, "F2")

chart_output = "RFM分析结果_含图表.xlsx"
wb.save(chart_output)
print(f"\n✅ 含图表的 Excel 已导出: {chart_output}")

print("\n===== 全流程完成 =====")
