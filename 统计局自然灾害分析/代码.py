import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re
import warnings
warnings.filterwarnings('ignore')

# 解决图表中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 第一阶段：数据读取与深度清洗
# ============================================================
folder_path = r'C:\Users\x1808\数据分析'
if os.path.exists(folder_path):
    os.chdir(folder_path)

def clean_nbs_excel(filepath):
    df_raw = pd.read_excel(filepath, header=None)
    header_idx = 0
    for i, row in df_raw.iterrows():
        if str(row[0]).strip() == '指标':
            header_idx = i
            break
            
    df = df_raw.iloc[header_idx:].copy()
    df.columns = [str(c).strip() for c in df.iloc[0]]
    df = df.iloc[1:].reset_index(drop=True)
    df.rename(columns={df.columns[0]: '指标'}, inplace=True)
    
    df = df[~df['指标'].astype(str).str.contains('注：|数据来源', na=False)]
    df['指标'] = df['指标'].astype(str).str.replace('\n', '').str.strip()
    
    year_cols = [c for c in df.columns if re.search(r'\d{4}年', str(c))]
    for col in year_cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = df[col].str.extract(r'([\d\.]+)')[0]
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    new_cols = {c: int(re.search(r'(\d{4})', c).group(1)) for c in year_cols}
    df.rename(columns=new_cols, inplace=True)
    
    return df

excel_files = glob.glob('*.xlsx')
all_clean_data = []

for file in excel_files:
    try:
        df = clean_nbs_excel(file)
        all_clean_data.append(df)
    except Exception as e:
        pass

df_total = pd.concat(all_clean_data, ignore_index=True)
df_total = df_total.drop_duplicates(subset=['指标'], keep='first')
all_years = sorted([c for c in df_total.columns if isinstance(c, int)])
df_total = df_total.set_index('指标')[all_years]

print(f"✅ 数据清洗完成！共提取 {len(df_total)} 项指标。")

# ============================================================
# 第二阶段：逐个独立输出精美的高清图表
# ============================================================

# ---------------- 图 1：地质灾害趋势 ----------------
s_geo = df_total.loc[df_total.index.str.contains('发生地质灾害起数', na=False)].iloc[0].dropna()
# 🔧 修复关键点：强制将 X 轴索引转为整数型
s_geo.index = s_geo.index.astype(int) 

plt.figure(figsize=(10, 5))
plt.plot(s_geo.index, s_geo.values, marker='o', color='#d62728', linewidth=2.5, markersize=8)
plt.fill_between(s_geo.index, s_geo.values, alpha=0.15, color='#d62728')
plt.title('全国地质灾害发生起数趋势', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('年份', fontsize=12); plt.ylabel('起数 (次)', fontsize=12)
plt.xticks(s_geo.index); plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# ---------------- 图 2：森林火灾次数与受害面积 ----------------
s_fire_times = df_total.loc[df_total.index.str.contains('森林火灾次数', na=False)].iloc[0].dropna()
s_fire_area = df_total.loc[df_total.index.str.contains('受害森林面积', na=False)].iloc[0].dropna()
# 🔧 同样强制转为整数
s_fire_times.index = s_fire_times.index.astype(int)
s_fire_area.index = s_fire_area.index.astype(int)

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(s_fire_times.index, s_fire_times.values, color='#ff7f0e', alpha=0.8, width=0.6, label='火灾次数 (次)')
ax1.set_xlabel('年份', fontsize=12)
ax1.set_ylabel('火灾次数 (次)', color='#ff7f0e', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#ff7f0e')
ax1.set_xticks(s_fire_times.index)

ax2 = ax1.twinx()
ax2.plot(s_fire_area.index, s_fire_area.values, marker='s', color='#2ca02c', linewidth=2.5, label='受害面积 (公顷)')
ax2.set_ylabel('受害森林面积 (公顷)', color='#2ca02c', fontsize=12)
ax2.tick_params(axis='y', labelcolor='#2ca02c')

plt.title('森林火灾次数与受害面积对比', fontsize=16, fontweight='bold', pad=15)
ax1.grid(True, linestyle='--', alpha=0.6)
fig.tight_layout()
plt.show()


# ---------------- 图 3：主要污染物排放趋势 ----------------
s_cod = df_total.loc[df_total.index.str.contains('化学需氧量排放量', na=False)].iloc[0].dropna()
s_so2 = df_total.loc[df_total.index.str.contains('二氧化硫排放量', na=False)].iloc[0].dropna()
s_nox = df_total.loc[df_total.index.str.contains('氮氧化物排放量', na=False)].iloc[0].dropna()
# 🔧 强制转换
s_cod.index = s_cod.index.astype(int)
s_so2.index = s_so2.index.astype(int)
s_nox.index = s_nox.index.astype(int)

plt.figure(figsize=(10, 5))
plt.plot(s_cod.index, s_cod.values, marker='o', label='化学需氧量(万吨)', color='#1f77b4', linewidth=2.5)
plt.plot(s_so2.index, s_so2.values, marker='s', label='二氧化硫(万吨)', color='#d62728', linewidth=2.5)
plt.plot(s_nox.index, s_nox.values, marker='^', label='氮氧化物(万吨)', color='#9467bd', linewidth=2.5)

plt.title('主要污染物排放趋势', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('年份', fontsize=12); plt.ylabel('排放量 (万吨)', fontsize=12)
plt.xticks(s_cod.index); plt.legend(fontsize=11); plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# ---------------- 图 4：生活垃圾处理设施与处理率 ----------------
s_rate = df_total.loc[df_total.index.str.contains('生活垃圾无害化处理率', na=False)].iloc[0].dropna()
s_incin = df_total.loc[df_total.index.str.contains('生活垃圾焚烧无害化处理厂数', na=False)].iloc[0].dropna()
# 🔧 强制转换
s_rate.index = s_rate.index.astype(int)
s_incin.index = s_incin.index.astype(int)

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(s_incin.index, s_incin.values, color='#9467bd', alpha=0.6, width=0.6, label='焚烧厂数量 (座)')
ax1.set_xlabel('年份', fontsize=12)
ax1.set_ylabel('焚烧厂数量 (座)', color='#9467bd', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#9467bd')
ax1.set_xticks(s_incin.index)

ax2 = ax1.twinx()
ax2.plot(s_rate.index, s_rate.values, marker='^', color='#2ca02c', linewidth=2.5, label='无害化处理率 (%)')
ax2.set_ylabel('无害化处理率 (%)', color='#2ca02c', fontsize=12)
ax2.tick_params(axis='y', labelcolor='#2ca02c')
ax2.set_ylim(95, 101)

plt.title('生活垃圾处理设施数量与处理率', fontsize=16, fontweight='bold', pad=15)
ax1.grid(True, linestyle='--', alpha=0.6)
fig.tight_layout()
plt.show()
