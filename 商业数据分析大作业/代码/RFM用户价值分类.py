import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 读取用户数据
df_user = pd.read_csv('data/clean/clean_user.csv')

# 2. 构造 R, F, M 指标
# R (Recency): 距离最后一次写评论的时间。因为数据没精确时间，我们用 (2023 - 注册年份) 的倒数代替活跃度
# F (Frequency): 写评论的总数
# M (Monetary): Yelp 没有消费金额，我们用获得的粉丝数 + 有用投票数代替用户影响力
df_user['R'] = 2023 - df_user['join_year']
df_user['F'] = df_user['review_count']
# 这里用粉丝数(fans) + 有用点赞数(useful) 作为 M 的替代指标
df_user['M'] = df_user['fans'] + df_user['useful'] 

# 3. 打分（用中位数切分，大于中位数打 1，小于打 0）
def rfm_score(x, median):
    return 1 if x > median else 0

r_median = df_user['R'].median()
f_median = df_user['F'].median()
m_median = df_user['M'].median()

df_user['R_Score'] = df_user['R'].apply(lambda x: rfm_score(x, r_median))
df_user['F_Score'] = df_user['F'].apply(lambda x: rfm_score(x, f_median))
df_user['M_Score'] = df_user['M'].apply(lambda x: rfm_score(x, m_median))

# 4. 组合出 8 种用户类型
def get_user_type(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r==1 and f==1 and m==1: return '重要价值客户'
    elif r==0 and f==1 and m==1: return '重要保持客户'
    elif r==1 and f==0 and m==1: return '重要发展客户'
    elif r==0 and f==0 and m==1: return '重要挽留客户'
    elif r==1 and f==1 and m==0: return '一般价值客户'
    elif r==0 and f==1 and m==0: return '一般保持客户'
    elif r==1 and f==0 and m==0: return '一般发展客户'
    else: return '一般挽留客户'

df_user['User_Type'] = df_user.apply(get_user_type, axis=1)

# 5. 画图：不同用户类型的人数分布
plt.figure(figsize=(10, 6))
sns.countplot(y='User_Type', data=df_user, order=df_user['User_Type'].value_counts().index, palette='viridis')
plt.title('Yelp 用户 RFM 价值分类', fontsize=16)
plt.xlabel('用户数量', fontsize=12)
plt.ylabel('用户类型', fontsize=12)
plt.tight_layout()

# 保存图片（这就是你的 fig03_RFM分类图.png）
plt.savefig('fig03_RFM分类图.png', dpi=150)
plt.show()

# 输出各类型占比
print(df_user['User_Type'].value_counts(normalize=True) * 100)
