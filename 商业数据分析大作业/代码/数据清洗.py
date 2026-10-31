import pandas as pd
import os

# 1. 定义文件路径（请确保你把解压后的 json 文件放在了 data/raw/ 目录下）
# 如果你的路径不同，请修改这里
raw_dir = 'data/raw/'
output_dir = 'data/clean/'  # 存到 clean 文件夹里

# 如果输出文件夹不存在，自动创建一个
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. 读取 business.json 的前 500 行
print("正在读取 business.json...")
try:
    df_business = pd.read_json(f'{raw_dir}yelp_academic_dataset_business.json', lines=True, nrows=500)
    # 存为 CSV，注意用 utf-8-sig 防止 Excel 打开中文乱码
    df_business.to_csv(f'{output_dir}sample_business_500.csv', index=False, encoding='utf-8-sig')
    print(f"✅ 成功提取 business 前 500 行，已保存至 {output_dir}sample_business_500.csv")
except FileNotFoundError:
    print("❌ 找不到 business.json，请检查文件路径是否正确！")

# 3. 读取 review.json 的前 500 行
print("正在读取 review.json...")
try:
    df_review = pd.read_json(f'{raw_dir}yelp_academic_dataset_review.json', lines=True, nrows=500)
    df_review.to_csv(f'{output_dir}sample_review_500.csv', index=False, encoding='utf-8-sig')
    print(f"✅ 成功提取 review 前 500 行，已保存至 {output_dir}sample_review_500.csv")
    
    # 简单看一下数据结构
    print("\n--- review 数据预览 ---")
    print(df_review[['review_id', 'stars', 'text', 'date']].head(3))
    
except FileNotFoundError:
    print("❌ 找不到 review.json，请检查文件路径是否正确！")

# 1. 设置路径
raw_dir = 'data/raw/'
output_dir = 'data/clean/'

# 确保输出文件夹存在
os.makedirs(output_dir, exist_ok=True)

# 2. 要处理的文件列表（去掉前缀和后缀，方便命名）
files = ['business', 'checkin', 'review', 'tip', 'user']

print("开始提取数据，请稍候...\n")

for file in files:
    input_path = f"{raw_dir}yelp_academic_dataset_{file}.json"
    output_path = f"{output_dir}sample_{file}_500.csv"
    
    try:
        # 读取前 500 行
        df = pd.read_json(input_path, lines=True, nrows=500)
        
        # 保存为 CSV，用 utf-8-sig 防止 Excel 打开乱码
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"✅ 成功：{file}.json 已提取 500 行 -> {output_path}")
        
    except FileNotFoundError:
        print(f"❌ 失败：找不到文件 {input_path}，请检查路径是否正确。")
    except Exception as e:
        print(f"⚠️ 出错：处理 {file}.json 时发生未知错误：{e}")

print("\n全部处理完成！")
import pandas as pd
import numpy as np
import os

clean_dir = 'data/clean/'

print("========== 开始数据清洗 ==========\n")

# ---------------- 1. 清洗 business ----------------
df_business = pd.read_csv(f'{clean_dir}sample_business_500.csv')
# 检查缺失值
missing_biz = df_business.isnull().sum()
# 填充缺失的 attributes 和 hours（避免后续报错）
df_business['attributes'] = df_business['attributes'].fillna('{}')
df_business['hours'] = df_business['hours'].fillna('{}')
# 删除没有评论数的假数据
df_business = df_business[df_business['review_count'] > 0]
# 保存
df_business.to_csv(f'{clean_dir}clean_business.csv', index=False, encoding='utf-8-sig')
print(f"✅ business 清洗完成，剩余 {len(df_business)} 条记录。缺失值处理完毕。")

# ---------------- 2. 清洗 review ----------------
df_review = pd.read_csv(f'{clean_dir}sample_review_500.csv')
# 剔除没有评论内容的空行
df_review = df_review.dropna(subset=['text'])
# 把 date 转为标准日期格式
df_review['date'] = pd.to_datetime(df_review['date'])
# 新增年份和月份列，方便后续做同期群或时间序列
df_review['year'] = df_review['date'].dt.year
df_review['month'] = df_review['date'].dt.month
# 保存
df_review.to_csv(f'{clean_dir}clean_review.csv', index=False, encoding='utf-8-sig')
print(f"✅ review 清洗完成，剩余 {len(df_review)} 条记录。日期已转换格式。")

# ---------------- 3. 清洗 user ----------------
df_user = pd.read_csv(f'{clean_dir}sample_user_500.csv')
# 转换日期格式
df_user['yelping_since'] = pd.to_datetime(df_user['yelping_since'])
# 计算用户注册年份
df_user['join_year'] = df_user['yelping_since'].dt.year
# 把 fan 和 review_count 等转为数值类型
df_user['review_count'] = pd.to_numeric(df_user['review_count'], errors='coerce').fillna(0)
# 保存
df_user.to_csv(f'{clean_dir}clean_user.csv', index=False, encoding='utf-8-sig')
print(f"✅ user 清洗完成，剩余 {len(df_user)} 条记录。注册时间已拆分。")

# ---------------- 4. 清洗 tip ----------------
df_tip = pd.read_csv(f'{clean_dir}sample_tip_500.csv')
df_tip = df_tip.dropna(subset=['text'])
df_tip['date'] = pd.to_datetime(df_tip['date'])
df_tip.to_csv(f'{clean_dir}clean_tip.csv', index=False, encoding='utf-8-sig')
print(f"✅ tip 清洗完成，剩余 {len(df_tip)} 条记录。")

# ---------------- 5. 清洗 checkin（重头戏） ----------------
df_checkin = pd.read_csv(f'{clean_dir}sample_checkin_500.csv')
# checkin 的 date 列是逗号分隔的字符串，我们需要提取出每一次签到的时间点
# 这一步会把 500 行数据“炸开”成上万行，每一行代表一次具体的签到
checkin_records = []
for index, row in df_checkin.iterrows():
    biz_id = row['business_id']
    if pd.notna(row['date']):
        # 按逗号分割时间戳
        times = row['date'].split(', ')
        for t in times:
            checkin_records.append({'business_id': biz_id, 'checkin_time': t})

df_checkin_clean = pd.DataFrame(checkin_records)
# 转换为日期时间格式
df_checkin_clean['checkin_time'] = pd.to_datetime(df_checkin_clean['checkin_time'])
# 提取出 小时（0-23），供后续画热力图使用
df_checkin_clean['hour'] = df_checkin_clean['checkin_time'].dt.hour
# 保存（注意这里因为炸开了，行数会变多）
df_checkin_clean.to_csv(f'{clean_dir}clean_checkin.csv', index=False, encoding='utf-8-sig')
print(f"✅ checkin 清洗完成，展开后共计 {len(df_checkin_clean)} 条签到记录，已提取出小时数。")

print("\n========== 数据清洗全部结束！==========")
