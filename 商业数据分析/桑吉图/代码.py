import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# ============ 数据 ============
data = {
    '来源': ['首页','首页','首页','首页','产品页面1','产品页面1','产品页面2','关于我们',
             '关于我们','关于我们','关于我们','联系我们','服务页面1','博客页面','博客页面'],
    '目标': ['产品页面1','产品页面2','关于我们','联系我们','服务页面1','服务页面2',
             '博客页面','常见问题页面','职业机会页面','隐私政策','服务条款',
             '联系表单','服务详情','成功案例','客户反馈'],
    '流量': [800,700,900,300,300,200,250,200,100,80,120,100,150,150,120]
}
df = pd.DataFrame(data)

# ============ 计算节点层级（最长路径） ============
nodes = list(dict.fromkeys(df['来源'].tolist() + df['目标'].tolist()))
out_edges = {n: [] for n in nodes}
for _, r in df.iterrows():
    out_edges[r['来源']].append(r['目标'])

# 用拓扑排序求层级
level = {n: 0 for n in nodes}
changed = True
while changed:
    changed = False
    for s, t in zip(df['来源'], df['目标']):
        if level[t] < level[s] + 1:
            level[t] = level[s] + 1
            changed = True

max_level = max(level.values())
levels = {}
for n in nodes:
    levels.setdefault(level[n], []).append(n)

# ============ 节点流量（取入+出中较大值用于高度） ============
in_flow = {n: 0 for n in nodes}
out_flow = {n: 0 for n in nodes}
for _, r in df.iterrows():
    out_flow[r['来源']] += r['流量']
    in_flow[r['目标']] += r['流量']
node_size = {n: max(in_flow[n], out_flow[n], 1) for n in nodes}

# ============ 布局 ============
fig, ax = plt.subplots(figsize=(14, 9))
gap = 40          # 节点间垂直间隔
x_positions = np.linspace(0.02, 0.98, max_level + 1)

node_y = {}       # 节点中心y
node_h = {}       # 节点高度
node_x = {}       # 节点x

# 每个层级总高度，用于居中
for lv in range(max_level + 1):
    ns = levels[lv]
    total_h = sum(node_size[n] for n in ns) + gap * (len(ns) - 1)
    y = 1.0 - (1.0 - total_h / 2.0 / max(1, sum(node_size.values())))  # 简化居中
    # 改为直接按比例
    pass

# 简单布局：每个层级从上往下排列并居中
scale = 1.0 / (max(sum(node_size[n] for n in levels[lv]) + gap*(len(levels[lv])-1)
                    for lv in range(max_level+1)) + 1)
for lv in range(max_level + 1):
    ns = levels[lv]
    heights = [node_size[n] * scale for n in ns]
    gaps = [gap * scale] * (len(ns) - 1)
    total = sum(heights) + sum(gaps)
    y = 0.5 + total / 2  # 从上往下
    for i, n in enumerate(ns):
        h = heights[i]
        y -= h
        node_y[n] = y + h / 2
        node_h[n] = h
        node_x[n] = x_positions[lv]
        y -= (gaps[i] if i < len(gaps) else 0)

# ============ 节点入/出偏移追踪 ============
in_offset = {n: 0 for n in nodes}
out_offset = {n: 0 for n in nodes}

# 按来源排序保证视觉顺序
df_sorted = df.sort_values(['来源']).reset_index(drop=True)

palette = plt.cm.tab20(np.linspace(0, 1, len(nodes)))
color_map = {n: palette[i] for i, n in enumerate(nodes)}

# ============ 绘制连接带 ============
for _, r in df_sorted.iterrows():
    s, t, v = r['来源'], r['目标'], r['流量']
    vh = v * scale
    x0 = node_x[s] + 0.015
    x1 = node_x[t] - 0.015
    y0_top = node_y[s] + node_h[s]/2 - out_offset[s]
    y0_bot = y0_top - vh
    out_offset[s] += vh
    y1_top = node_y[t] + node_h[t]/2 - in_offset[t]
    y1_bot = y1_top - vh
    in_offset[t] += vh

    # 用贝塞尔曲线构造带状
    xs = np.linspace(x0, x1, 50)
    ctrl = (x0 + x1) / 2
    curve_top = (y0_top * (1 - (xs - x0)/(x1 - x0)) + y1_top * ((xs - x0)/(x1 - x0)))
    curve_bot = (y0_bot * (1 - (xs - x0)/(x1 - x0)) + y1_bot * ((xs - x0)/(x1 - x0)))
    ax.fill_between(xs, curve_bot, curve_top, color=color_map[s], alpha=0.35, linewidth=0)

# ============ 绘制节点矩形 + 标签 ============
for n in nodes:
    x = node_x[n]
    y = node_y[n]
    h = node_h[n]
    rect = patches.Rectangle((x - 0.012, y - h/2), 0.024, h,
                             facecolor=color_map[n], edgecolor='black', lw=0.5)
    ax.add_patch(rect)
    # 标签放在节点外侧
    ha = 'right' if x > 0.5 else 'left'
    dx = -0.025 if x > 0.5 else 0.025
    ax.text(x + dx, y, f"{n}\n({node_size[n]})", va='center', ha=ha, fontsize=9)

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('网站流量桑基图 (Sankey Diagram)', fontsize=16, pad=20)

plt.tight_layout()
plt.savefig('sankey_matplotlib.png', dpi=150, bbox_inches='tight')
plt.show()
print("已生成：sankey_matplotlib.png")
