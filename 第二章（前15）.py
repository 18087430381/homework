import matplotlib.pyplot as plt
regions = ["华北", "华南", "东北", "西北", "西南", "华东"]
sales = [2354, 1902, 3524, 2698, 2896, 2563]
fig, ax = plt.subplots(figsize=(10, 7), facecolor="#080820")
ax.set_facecolor("#080820")
bars = ax.bar(regions, sales, color="#00ccff", width=0.55)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 60,
            f"{int(height)}", ha="center", color="white", fontsize=11)
ax.set_title("3月各区域销量分布\n东北销量最多占比总销量的22%，华南销量最低",
             color="white", fontsize=20, pad=25)
ax.tick_params(axis="x", colors="white", labelsize=12)
ax.tick_params(axis="y", colors="white", labelsize=12)
ax.set_ylim(0, 4100)
plt.figtext(0.5, 0.03, "*注：数据来源于公司销售系统，统计日期截至2022.03.31",
            ha="center", color="white", fontsize=10)
plt.savefig("sales_bar.png", facecolor="#080820", dpi=150, bbox_inches="tight")
plt.show()
