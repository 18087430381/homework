import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============ 1. 读取数据 ============
# 演示sheet数据
demo_data = pd.DataFrame({
    '阶段': ['潜在', '接触', '意向', '明确', '谈判', '成交'],
    '用户数': [100, 90, 80, 70, 60, 50]
})
demo_data['转化率'] = demo_data['用户数'] / demo_data['用户数'].shift(1)
demo_data.loc[0, '转化率'] = 1.0

print("=" * 50)
print("【演示Sheet】漏斗数据")
print("=" * 50)
print(demo_data.to_string(index=False))
print()

# 练习sheet数据 - 用户行为漏斗
behavior_data = pd.DataFrame({
    '用户行为': ['浏览', '收藏', '加购', '购买'],
    '用户数': [100, 90, 80, 80]
})
behavior_data['转化率'] = behavior_data['用户数'] / behavior_data['用户数'].shift(1)
behavior_data.loc[0, '转化率'] = 1.0

# 练习sheet数据 - 用户运营行为漏斗(AARRR)
aarrr_data = pd.DataFrame({
    '用户运营阶段': ['获取', '激活', '留存', '收益', '推荐'],
    '用户数': [100, 80, 60, 40, 30]
})
aarrr_data['转化率'] = aarrr_data['用户数'] / aarrr_data['用户数'].shift(1)
aarrr_data.loc[0, '转化率'] = 1.0

print("=" * 50)
print("【练习Sheet】用户行为漏斗")
print("=" * 50)
print(behavior_data.to_string(index=False))
print()
print("=" * 50)
print("【练习Sheet】用户运营行为漏斗 (AARRR)")
print("=" * 50)
print(aarrr_data.to_string(index=False))
print()

# ============ 2. 绘制漏斗图 ============
def plot_funnel(ax, stages, values, title, color_start='#4A90D9', color_end='#E74C3C'):
    """绘制漏斗图"""
    n = len(stages)
    max_val = max(values)
    
    # 计算每层的宽度（按比例）
    widths = [v / max_val for v in values]
    
    # 颜色渐变
    colors = plt.cm.RdYlBu_r(np.linspace(0.3, 0.9, n))
    
    y_positions = np.arange(n)[::-1]  # 从上到下
    
    for i, (stage, val, width, y) in enumerate(zip(stages, values, widths, y_positions)):
        # 绘制梯形/矩形
        left = (1 - width) / 2
        rect = patches.FancyBboxPatch(
            (left, y - 0.35), width, 0.7,
            boxstyle="round,pad=0.02",
            facecolor=colors[i], edgecolor='white', linewidth=1.5, alpha=0.85
        )
        ax.add_patch(rect)
        
        # 添加文字标签
        ax.text(0.5, y, f'{stage}\n{val}',
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='white' if i < n//2 else 'white')
        
        # 添加转化率标注（在第一层下方）
        if i > 0:
            conv_rate = values[i] / values[i-1] * 100
            ax.annotate(f'↓ {conv_rate:.1f}%',
                       xy=(1.02, y + 0.35), fontsize=9, color='#2C3E50',
                       ha='left', va='center')
    
    ax.set_xlim(-0.15, 1.35)
    ax.set_ylim(-0.8, n - 0.2)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.axis('off')

# 创建画布
fig, axes = plt.subplots(1, 3, figsize=(18, 7))

# 图1：演示漏斗
plot_funnel(axes[0], demo_data['阶段'].tolist(), demo_data['用户数'].tolist(),
            '演示：销售漏斗')

# 图2：用户行为漏斗
plot_funnel(axes[1], behavior_data['用户行为'].tolist(), behavior_data['用户数'].tolist(),
            '练习：用户行为漏斗')

# 图3：AARRR漏斗
plot_funnel(axes[2], aarrr_data['用户运营阶段'].tolist(), aarrr_data['用户数'].tolist(),
            '练习：用户运营漏斗 (AARRR)')

plt.tight_layout()
plt.savefig('漏斗图.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

# ============ 3. 输出转化率汇总 ============
print("=" * 50)
print("【转化率汇总】")
print("=" * 50)

def calc_conv(df, stage_col, value_col):
    result = []
    vals = df[value_col].values
    stages = df[stage_col].values
    for i in range(len(stages)):
        if i == 0:
            result.append((stages[i], vals[i], '-'))
        else:
            rate = vals[i] / vals[i-1] * 100
            result.append((stages[i], vals[i], f'{rate:.1f}%'))
    return result

print("\n▶ 演示漏斗转化率：")
for stage, val, rate in calc_conv(demo_data, '阶段', '用户数'):
    print(f"  {stage:4s}  用户数={val:3d}  环比转化率={rate}")

print("\n▶ 用户行为漏斗转化率：")
for stage, val, rate in calc_conv(behavior_data, '用户行为', '用户数'):
    print(f"  {stage:4s}  用户数={val:3d}  环比转化率={rate}")

print("\n▶ AARRR漏斗转化率：")
for stage, val, rate in calc_conv(aarrr_data, '用户运营阶段', '用户数'):
    print(f"  {stage:4s}  用户数={val:3d}  环比转化率={rate}")

print("\n▶ 整体转化率（首→尾）：")
print(f"  演示漏斗:  {demo_data['用户数'].iloc[-1]}/{demo_data['用户数'].iloc[0]} = {demo_data['用户数'].iloc[-1]/demo_data['用户数'].iloc[0]*100:.1f}%")
print(f"  用户行为:  {behavior_data['用户数'].iloc[-1]}/{behavior_data['用户数'].iloc[0]} = {behavior_data['用户数'].iloc[-1]/behavior_data['用户数'].iloc[0]*100:.1f}%")
print(f"  AARRR:     {aarrr_data['用户数'].iloc[-1]}/{aarrr_data['用户数'].iloc[0]} = {aarrr_data['用户数'].iloc[-1]/aarrr_data['用户数'].iloc[0]*100:.1f}%")
