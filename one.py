import matplotlib.pyplot as plt
labels = ["[20,30)", "[30,40)", "[40,50)", "≥50"]
percents = [37.5, 29.2, 20.8, 12.5]
colors = ['#4040ff', '#2080ff', '#20cccc', '#ffcc22'] 
fig, ax = plt.subplots(figsize=(8, 8), facecolor='#000000') 
wedges, texts, autotexts = ax.pie(
    percents,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%',
    pctdistance=1.2,   
    labeldistance=1.4,
    startangle=30,
    wedgeprops={"width":0.35}, 
)
for t in texts:
    t.set_color("white")
for a in autotexts:
    a.set_color("white")
ax.axis("equal")   
ax.set_title("2022年上半年各年龄段人数分布\n公司平均年龄32.5，20‑30员工比例最高占比37.5%",
             color="white", fontsize=13)
plt.figtext(0.5, 0.08, "注：数据来源于公司人力资源系统，统计日期截至2022‑06‑30",
            ha="center", color="white", fontsize=9)
plt.show()
