import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 数据透视表
# ============================================================
print("=" * 60)
print("1. 数据透视表")
print("=" * 60)

data = {
    '销售地区': ['北京']*12 + ['杭州']*12 + ['济南']*12,
    '销售人员': (['白云飞']*4 + ['苏云珊']*4 + ['赵盟盟']*4) * 3,
    '品名': (['显示器','机械键盘','电脑主机','笔记本']) * 9,
    '数量': [52,70,118,144, 10,90,88,16, 3,72,65,64,
             116,58,85,56, 143,72,6,67, 103,147,44,104,
             41,98,109,79, 68,2,88,123, 34,104,97,138],
    '单价': [1000,500,2500,3000] * 9
}
df = pd.DataFrame(data)
df['销售金额'] = df['数量'] * df['单价']

print("\n原始数据前5行：")
print(df.head())

# 按销售地区+销售人员汇总
pivot1 = df.pivot_table(index=['销售地区','销售人员'], values='销售金额',
                        aggfunc='sum', margins=True, margins_name='总计')
print("\n【透视表1】各地区各销售人员销售金额汇总：")
print(pivot1)

# 按品名汇总
pivot2 = df.pivot_table(index='品名', values=['数量','销售金额'],
                        aggfunc='sum', margins=True, margins_name='总计')
print("\n【透视表2】各产品数量与销售金额汇总：")
print(pivot2)

# 交叉透视：地区×品名
pivot3 = df.pivot_table(index='销售地区', columns='品名', values='销售金额',
                        aggfunc='sum', margins=True, margins_name='总计')
print("\n【透视表3】地区×品名 销售金额交叉表：")
print(pivot3)

# ============================================================
# 2. 条件格式
# ============================================================
print("\n" + "=" * 60)
print("2. 条件格式")
print("=" * 60)

cf_data = pd.DataFrame({
    'A': [19, 37, 17, 13, 14],
    'B': [36, 23, 50, 40, 12]
})
print("\n原始数据：")
print(cf_data)

# a. 单元格值介于15和25之间 → 高亮
mask_between = (cf_data >= 15) & (cf_data <= 25)
print("\n【a】单元格值介于15和25之间的位置：")
print(mask_between)

# b. 第二列的值大于第一列 → 高亮
mask_b_gt_a = cf_data['B'] > cf_data['A']
print("\n【b】第二列大于第一列的行：")
print(cf_data[mask_b_gt_a])

# 偶数行加颜色
print("\n【c】偶数行（索引从0开始，行号2,4,...即索引1,3,...）：")
even_rows = cf_data.iloc[1::2]
print(even_rows)

# 可视化条件格式效果
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 图1：介于15-25高亮
ax = axes[0]
colors = ['#FFD700' if v else '#E8E8E8' for v in mask_between.values.flatten()]
ax.bar(range(len(cf_data)*2), cf_data.values.flatten(), color=colors)
ax.set_title('条件格式a: 值介于15-25高亮')
ax.set_xticks(range(len(cf_data)*2))
ax.set_xticklabels([f'A{i+1}' for i in range(len(cf_data))] + [f'B{i+1}' for i in range(len(cf_data))], rotation=45)

# 图2：B>A高亮
ax = axes[1]
x = np.arange(len(cf_data))
w = 0.35
ax.bar(x - w/2, cf_data['A'], w, label='A列', color='#87CEEB')
ax.bar(x + w/2, cf_data['B'], w, label='B列',
       color=['#FF6B6B' if m else '#90EE90' for m in mask_b_gt_a])
ax.set_title('条件格式b: B列>A列高亮红色')
ax.set_xticks(x)
ax.set_xticklabels([f'行{i+1}' for i in range(len(cf_data))])
ax.legend()

# 图3：数据条效果
ax = axes[2]
y_pos = np.arange(len(cf_data))
ax.barh(y_pos, cf_data['A'], color='#4ECDC4', label='A列')
ax.barh(y_pos, cf_data['B'], color='#FF6B6B', alpha=0.6, label='B列')
ax.set_yticks(y_pos)
ax.set_yticklabels([f'行{i+1}' for i in range(len(cf_data))])
ax.set_title('数据条效果对比')
ax.legend()

plt.tight_layout()
plt.savefig('条件格式效果图.png', dpi=100, bbox_inches='tight')
plt.show()
print("\n条件格式效果图已保存：条件格式效果图.png")

# ============================================================
# 3. 单元格引用 - 九九乘法表
# ============================================================
print("\n" + "=" * 60)
print("3. 单元格引用 - 九九乘法表")
print("=" * 60)

# Excel公式: =IF($A2>=B$1, B$1&"×"&$A2&"="&B$1*$A2, "")
# 用Python模拟该公式逻辑，生成9×9乘法表
print("\n用1个公式（IF + 混合引用 + 字符连接）实现九九乘法表：\n")

table = []
for row in range(1, 10):       # 对应 $A2, $A3... 行标
    row_data = []
    for col in range(1, 10):   # 对应 B$1, C$1... 列标
        if row >= col:         # IF($A2>=B$1, ...)
            row_data.append(f"{col}×{row}={col*row}")
        else:
            row_data.append("")
    table.append(row_data)

# 打印
header = "  ".join(f"{c:>7}" for c in range(1,10))
print(f"{'':>6}{header}")
print("-" * 80)
for i, row in enumerate(table, 1):
    cells = "  ".join(f"{v:>7}" for v in row)
    print(f"  {i:>2} |{cells}")

# 可视化九九乘法表
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')
cell_text = []
for i in range(9):
    row_text = []
    for j in range(9):
        if j <= i:
            row_text.append(f"{j+1}×{i+1}={((j+1)*(i+1))}")
        else:
            row_text.append("")
    cell_text.append(row_text)

table_plot = ax.table(cellText=cell_text, loc='center', cellLoc='center')
table_plot.auto_set_font_size(False)
table_plot.set_fontsize(11)
table_plot.scale(1.2, 1.8)

# 给下三角着色
for i in range(9):
    for j in range(9):
        cell = table_plot[(i, j)]
        if j <= i:
            cell.set_facecolor('#E6F3FF')
        else:
            cell.set_facecolor('white')

ax.set_title('九九乘法表（IF + 混合引用 + 字符连接 实现）', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('九九乘法表.png', dpi=100, bbox_inches='tight')
plt.show()
print("\n九九乘法表图片已保存：九九乘法表.png")

# ============================================================
# 4. 查找 - 成绩等级
# ============================================================
print("\n" + "=" * 60)
print("4. 查找 - 成绩等级（VLOOKUP近似匹配）")
print("=" * 60)

names = ['李1','李2','李3','李4','李5','李6','李7','李8',
         '张5','张6','张7','张8','张9','张10','张11','张12',
         '张13','张14','张15','张16','张17','张18','张19','张20',
         '张21','张22','张23','张24','张25','张26','张27','张28',
         '张29','张30','张31','张32','张33','张34','张35','张36']
scores = [0,10,35,50,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,
          81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]

# 查找表（必须按分数升序排列，VLOOKUP近似匹配要求）
lookup_table = pd.DataFrame({
    '分数': [0, 60, 70, 80, 90],
    '等级': ['不及格', '及格', '可以', '良好', '优秀']
})
print("\n查找表（升序）：")
print(lookup_table)

def vlookup_approximate(score, table):
    """模拟Excel VLOOKUP(score, table, 2, TRUE) 近似匹配"""
    result = None
    for _, row in table.iterrows():
        if score >= row['分数']:
            result = row['等级']
        else:
            break
    return result

df_scores = pd.DataFrame({'学生姓名': names, '成绩': scores})
df_scores['成绩等级'] = df_scores['成绩'].apply(lambda x: vlookup_approximate(x, lookup_table))

print("\n【查找结果】前15行：")
print(df_scores.head(15).to_string(index=False))
print("\n...")
print(df_scores.tail(5).to_string(index=False))

# 统计各等级人数
print("\n【各等级人数统计】")
grade_counts = df_scores['成绩等级'].value_counts()
print(grade_counts)

# 可视化
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 图1：成绩分布直方图+等级分界线
ax = axes[0]
ax.hist(df_scores['成绩'], bins=20, color='#4ECDC4', edgecolor='white', alpha=0.8)
for boundary, label in [(60,'及格线'), (70,'可以线'), (80,'良好线'), (90,'优秀线')]:
    ax.axvline(boundary, color='red', linestyle='--', alpha=0.6)
    ax.text(boundary+0.5, ax.get_ylim()[1]*0.9, label, fontsize=9, color='red')
ax.set_title('成绩分布与等级分界线')
ax.set_xlabel('分数')
ax.set_ylabel('人数')

# 图2：等级人数柱状图
ax = axes[1]
order = ['不及格','及格','可以','良好','优秀']
counts = [grade_counts.get(g, 0) for g in order]
colors_bar = ['#FF6B6B','#FFA07A','#FFD700','#90EE90','#4ECDC4']
bars = ax.bar(order, counts, color=colors_bar, edgecolor='white')
for bar, c in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            str(c), ha='center', fontweight='bold')
ax.set_title('各等级人数统计')
ax.set_ylabel('人数')

plt.tight_layout()
plt.savefig('成绩等级查找.png', dpi=100, bbox_inches='tight')
plt.show()
print("\n成绩等级查找图已保存：成绩等级查找.png")

# ============================================================
# 5. 汇总输出
# ============================================================
print("\n" + "=" * 60)
print("全部处理完成！生成图片文件：")
print("  1. 条件格式效果图.png")
print("  2. 九九乘法表.png")
print("  3. 成绩等级查找.png")
print("=" * 60)
