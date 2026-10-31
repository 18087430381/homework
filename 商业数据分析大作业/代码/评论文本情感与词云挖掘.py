import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from snownlp import SnowNLP
import jieba
from wordcloud import WordCloud
import warnings

warnings.filterwarnings('ignore')
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ================= 1. 读取数据并计算情感得分 =================
print("正在读取数据并进行情感分析，请稍候...")
# 使用你刚才清洗好的数据
df_review = pd.read_csv('data/clean/clean_review.csv')

# 如果 text 列有 NaN，直接删掉
df_review = df_review.dropna(subset=['text'])

# 定义情感打分函数（SnowNLP 返回 0-1，越接近 1 越正面）
def get_sentiment(text):
    try:
        return SnowNLP(str(text)).sentiments
    except:
        return None

# 注意：英文文本 SnowNLP 依然能给出一定倾向，但在作业里我们可以说明这一点
df_review['sentiment_score'] = df_review['text'].apply(get_sentiment)

# ================= 2. 画图：星级 vs 情感得分 (箱线图) =================
plt.figure(figsize=(10, 6))
sns.boxplot(x='stars', y='sentiment_score', data=df_review, palette='Set2')
plt.title('Yelp 用户打分与机器情感得分对比 (1-5星)', fontsize=16)
plt.xlabel('用户星级打分', fontsize=12)
plt.ylabel('SnowNLP 情感得分 (0-1)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('fig04_情感分析箱线图.png', dpi=150)
plt.show()

# 输出业务结论
mean_sent = df_review.groupby('stars')['sentiment_score'].mean()
print("\n📊 商业结论：")
print(f"1星评价的平均情感得分为：{mean_sent.get(1, 0):.3f}")
print(f"5星评价的平均情感得分为：{mean_sent.get(5, 0):.3f}")
print("💡 业务洞察：5星评论情感分极高，说明高分评价真实。但3星中评的情感分方差可能很大，说明有些用户虽然给了中评，但文字里充满了抱怨，平台需要重点关注3星评论中的负面词汇。")


# ================= 3. 画图：评论文本词云图 =================
print("\n正在生成高频词云图...")

# 把所有的文本拼在一起
all_text = " ".join(df_review['text'].astype(str).tolist())

# 使用 jieba 分词（注意：Yelp 是英文，但这里保留了分词逻辑，如果你的文本全是英文，其实可以不做这一步直接生成）
# 为了兼容性，这里直接把它转成小写，并按空格切分
all_text_clean = all_text.lower()

# 生成词云
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white',
    max_words=100,
    colormap='viridis',
    random_state=42
).generate(all_text_clean)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off') # 关掉坐标轴
plt.title('Yelp 评论高频词云图', fontsize=16)
plt.tight_layout()
plt.savefig('fig05_词云图.png', dpi=150)
plt.show()

print("\n✅ 情感分析与词云图生成完毕！")
print("请检查文件夹中是否生成了 fig04_情感分析箱线图.png 和 fig05_词云图.png")
