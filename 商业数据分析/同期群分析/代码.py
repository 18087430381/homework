import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import LinearSegmentedColormap

# 中文字体设置（Windows 用 SimHei；Mac 改 'Arial Unicode MS'）
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

# ============ 1. 读取与清洗 ============
df = pd.read_excel("1-4同期群分析.xlsx", sheet_name="用户登录明细")
df.columns = ["用户编号", "注册日期", "登录时点"]

df["注册日期"] = pd.to_datetime(df["注册日期"]).dt.normalize()
df["登录时点"] = pd.to_datetime(df["登录时点"]).dt.normalize()
df = df.drop_duplicates(subset=["用户编号", "登录时点"])

df["留存天数"] = (df["登录时点"] - df["注册日期"]).dt.days
df = df[df["留存天数"] >= 0]

# ============ 2. 构建同期群留存率 ============
cohort_size = df.groupby("注册日期")["用户编号"].nunique().rename("同期群用户数")

retention = (
    df.groupby(["注册日期", "留存天数"])["用户编号"]
      .nunique().reset_index()
      .merge(cohort_size, on="注册日期")
)
retention["留存率"] = retention["用户编号"] / retention["同期群用户数"]

MAX_DAY = 15
cohort_pivot = retention.pivot_table(
    index="注册日期", columns="留存天数", values="留存率", aggfunc="first"
)
cohort_pivot = cohort_pivot.loc[:, cohort_pivot.columns <= MAX_DAY]
for d in range(MAX_DAY + 1):
    if d not in cohort_pivot.columns:
        cohort_pivot[d] = np.nan
cohort_pivot = cohort_pivot[sorted(cohort_pivot.columns)]
rate_matrix = cohort_pivot.copy()

# ============ 3. 表格输出 ============
cohort_table = rate_matrix.copy()
cohort_table.insert(0, "同期群用户数", cohort_size)
cohort_table = (cohort_table * 100).round(2).astype(str) + "%"
cohort_table["同期群用户数"] = cohort_size.astype(int)
print(cohort_table.to_string())
cohort_table.to_excel("同期群留存率分析结果.xlsx", sheet_name="留存率矩阵")

# ============ 4. 加权平均留存曲线数据 ============
avg_curve = (
    retention[retention["留存天数"] <= MAX_DAY]
    .groupby("留存天数")
    .apply(lambda g: g["用户编号"].sum() / g["同期群用户数"].sum())
    .rename("加权平均留存率")
    .reset_index()
)

# ================= 图1：留存曲线 =================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(avg_curve["留存天数"], avg_curve["加权平均留存率"] * 100,
        marker="o", linewidth=2, color="#2E86C1", label="加权平均留存率")
for x, y in zip(avg_curve["留存天数"], avg_curve["加权平均留存率"] * 100):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=8)
ax.set_title("加权平均留存曲线（注册后第N天）", fontsize=14, fontweight="bold")
ax.set_xlabel("留存天数（注册后第N天）")
ax.set_ylabel("留存率")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_xticks(range(0, MAX_DAY + 1))
ax.legend()
plt.tight_layout()
plt.savefig("图1_留存曲线.png", dpi=150)
plt.show()

# ================= 图2：同期群留存率热力图（纯 matplotlib） =================
# 自定义渐变色：浅黄 -> 深红
cmap = LinearSegmentedColormap.from_list(
    "custom_heat", ["#FFFDE7", "#FFD54F", "#FF8A65", "#C62828"]
)

data = rate_matrix.values * 100          # 百分比数值
rows, cols = data.shape
masked = np.ma.masked_invalid(data)      # 把 NaN 遮掉，显示白色

fig, ax = plt.subplots(figsize=(14, max(4.5, rows * 0.4)))
im = ax.imshow(masked, cmap=cmap, aspect="auto",
               vmin=np.nanmin(data), vmax=np.nanmax(data))

# 颜色条
cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label("留存率 (%)")

# 每个格子写数值
for i in range(rows):
    for j in range(cols):
        v = data[i, j]
        if not np.isnan(v):
            # 深色格子用白字，浅色用黑字
            color = "white" if v > (np.nanmax(data) * 0.6) else "black"
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=7, color=color)

# 坐标轴
ax.set_xticks(range(cols))
ax.set_xticklabels([f"D{c}" for c in rate_matrix.columns], fontsize=8)
ax.set_yticks(range(rows))
ax.set_yticklabels([d.strftime("%m-%d") for d in rate_matrix.index], fontsize=8)
ax.set_xlabel("留存天数")
ax.set_ylabel("注册日期（同期群）")
ax.set_title("同期群留存率热力图（行=注册日期，列=第N天）",
             fontsize=14, fontweight="bold")

# 网格线
ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
ax.grid(which="minor", color="white", linewidth=0.8)
ax.tick_params(which="minor", length=0)

plt.tight_layout()
plt.savefig("图2_留存率热力图.png", dpi=150)
plt.show()

# ================= 图3：同期群规模柱状图 =================
fig, ax = plt.subplots(figsize=(12, 4.5))
bars = ax.bar(
    [d.strftime("%m-%d") for d in cohort_size.index],
    cohort_size.values, color="#48C9B0", edgecolor="white"
)
for b, v in zip(bars, cohort_size.values):
    ax.annotate(str(v), (b.get_x() + b.get_width()/2, v),
                textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
ax.set_title("各同期群用户规模（按注册日期）", fontsize=14, fontweight="bold")
ax.set_xlabel("注册日期")
ax.set_ylabel("新增用户数")
ax.tick_params(axis="x", labelsize=8)
plt.tight_layout()
plt.savefig("图3_同期群规模.png", dpi=150)
plt.show()

# ================= 图4：多同期群留存曲线对比 =================
top_cohorts = cohort_size.sort_values(ascending=False).head(8).index
fig, ax = plt.subplots(figsize=(10, 5.5))
for d in top_cohorts:
    y = rate_matrix.loc[d] * 100
    ax.plot(y.index, y.values, marker="o", markersize=3,
            label=d.strftime("%m-%d"), alpha=0.85)
ax.set_title("前8大同期群留存曲线对比", fontsize=14, fontweight="bold")
ax.set_xlabel("留存天数（注册后第N天）")
ax.set_ylabel("留存率")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_xticks(range(0, MAX_DAY + 1))
ax.legend(title="注册日期", fontsize=8, ncol=2)
plt.tight_layout()
plt.savefig("图4_同期群曲线对比.png", dpi=150)
plt.show()

print("\n已生成：同期群留存率分析结果.xlsx + 4张图表（PNG）")
