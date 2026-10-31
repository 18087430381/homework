import pandas as pd
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np
import os

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ================= 自动创建 figures 文件夹 =================
os.makedirs('figures', exist_ok=True)

# 1. 准备时间序列数据（按季度统计）
df_review = pd.read_csv('data/clean/clean_review.csv')
df_review['date'] = pd.to_datetime(df_review['date'])
quarterly_reviews = df_review.set_index('date').resample('Q').size()
# 过滤掉极其稀疏的异常季度（比如只有1条评论的季度）
quarterly_reviews = quarterly_reviews[quarterly_reviews > 1]

# 2. 划分训练集和测试集（留出最后 4 个季度做回测）
train_data = quarterly_reviews[:-4]
test_data = quarterly_reviews[-4:]

# 3. 建立 SARIMA 模型（季度数据，季节性周期 s=4）
model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
results = model.fit(disp=False)

# 4. 输出预测数据
forecast = results.get_forecast(steps=len(test_data))
forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int(alpha=0.05) 
forecast_mean.index = test_data.index
forecast_ci.index = test_data.index

# 5. 计算回测误差
mask = test_data != 0
mape = mean_absolute_percentage_error(test_data[mask], forecast_mean[mask])
rmse = np.sqrt(mean_squared_error(test_data, forecast_mean))

print(f"✅ 回测结果：MAPE = {mape*100:.2f}%")
print(f"✅ 回测结果：RMSE = {rmse:.2f}")

# 6. 画图
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data, label='历史训练数据', color='blue')
plt.plot(test_data.index, test_data, label='真实测试数据', color='green', marker='o')
plt.plot(forecast_mean.index, forecast_mean, label='预测数据 (点预测)', color='red', linestyle='--')
plt.fill_between(forecast_ci.index,
                 forecast_ci.iloc[:, 0],
                 forecast_ci.iloc[:, 1],
                 color='pink', alpha=0.3, label='95% 置信区间')

plt.title('评论数量未来趋势预测 (SARIMA 模型)', fontsize=16)
plt.xlabel('日期', fontsize=12)
plt.ylabel('评论数量', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# 这次文件夹存在了，绝对不会报错了
plt.savefig('figures/fig03_评论数量SARIMA预测图.png', dpi=150)
plt.show()

print("✅ 图片已成功保存至 figures 文件夹！")
