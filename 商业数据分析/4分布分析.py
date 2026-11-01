import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
file_path = "4分布分析.xlsx"
xl = pd.ExcelFile(file_path)
print("工作表列表:", xl.sheet_names)

df_raw = pd.read_excel(file_path, sheet_name="分布分析", header=None)
print("原始数据形状:", df_raw.shape)

# ========== 2. 提取客单价数据（U列，索引20；第2行起为数据） ==========
# 表头在行1（0-based），数据从行2开始
price_col = df_raw.iloc[1:, 20]          # U列
price = pd.to_numeric(price_col, errors='coerce').dropna()
print(f"\n客单价有效样本数: {len(price)}")

# ========== 3. 描述性统计与四分位数 ==========
mean_val = price.mean()
q0 = price.min()
q1 = price.quantile(0.25)
q2 = price.median()
q3 = price.quantile(0.75)
q4 = price.max()
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

stats = pd.DataFrame({
    "指标": ["均值", "min", "25%分位数 Q1", "中位数", "75%分位数 Q3", "max", "IQR", "下限(Q1-1.5IQR)", "上限(Q3+1.5IQR)"],
    "数值": [mean_val, q0, q1, q2, q3, q4, iqr, lower_bound, upper_bound]
})
print("\n===== 客单价分布统计 =====")
print(stats.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# ========== 4. 异常值识别 ==========
outliers = price[(price < lower_bound) | (price > upper_bound)]
print(f"\n异常值个数: {len(outliers)}")
if len(outliers) > 0:
    print("异常值:", sorted(outliers.tolist()))

# ========== 5. 客单价分布图 ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 直方图
axes[0].hist(price, bins=25, color='steelblue', edgecolor='black', alpha=0.75)
axes[0].axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'均值={mean_val:.1f}')
axes[0].axvline(q2, color='green', linestyle='-.', linewidth=1.5, label=f'中位数={q2:.1f}')
axes[0].set_title('客单价分布直方图')
axes[0].set_xlabel('客单价')
axes[0].set_ylabel('频数')
axes[0].legend()

# 箱线图
axes[1].boxplot(price, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue'),
                medianprops=dict(color='red', linewidth=2))
axes[1].set_title('客单价箱线图（含异常值）')
axes[1].set_ylabel('客单价')
axes[1].set_xticks([1]); axes[1].set_xticklabels(['客单价'])

plt.tight_layout()
plt.savefig('客单价分布.png', dpi=150)
plt.show()

# ========== 6. 门店客流量时间序列 ==========
time_col = df_raw.iloc[2:, 1]            # B列时点（从第3行开始）
flow_col = pd.to_numeric(df_raw.iloc[2:, 2], errors='coerce')  # C列客流量
flow_df = pd.DataFrame({'时点': pd.to_datetime(time_col, errors='coerce'), '客流量': flow_col}).dropna()

print("\n===== 门店客流量统计 =====")
print(flow_df['客流量'].describe().to_string(float_format=lambda x: f"{x:.2f}"))

plt.figure(figsize=(14, 4))
plt.plot(flow_df['时点'], flow_df['客流量'], color='teal', linewidth=0.8)
plt.title('门店客流量时间序列（2020-01-01 每30分钟）')
plt.xlabel('时点'); plt.ylabel('客流量')
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('客流量时间序列.png', dpi=150)
plt.show()

# ========== 7. 年龄分布 ==========
age = pd.to_numeric(df_raw.iloc[1:, 11], errors='coerce').dropna()  # L列年龄
print("\n===== 年龄统计 =====")
print(age.describe().to_string(float_format=lambda x: f"{x:.2f}"))

plt.figure(figsize=(10, 4))
plt.hist(age, bins=20, color='coral', edgecolor='black', alpha=0.8)
plt.title('用户年龄分布')
plt.xlabel('年龄'); plt.ylabel('人数')
plt.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('年龄分布.png', dpi=150)
plt.show()
