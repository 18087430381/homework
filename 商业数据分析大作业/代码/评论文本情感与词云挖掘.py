import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import warnings

warnings.filterwarnings('ignore')
# 解决中文显示问题（标题用中文时保留）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ================= 1. 读取数据并计算情感得分 =================
print("正在读取数据并进行情感分析，请稍候...")
df_review = pd.read_csv('data/clean/clean_review.csv')

# 如果 text 列有 NaN，直接删掉
df_review = df_review.dropna(subset=['text'])

# 初始化 VADER
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """返回 VADER compound 分数，范围 [-1, 1]"""
    try:
        return analyzer.polarity_scores(str(text))['compound']
    except Exception:
        return None

# 计算 compound 分数
df_review['sentiment_score'] = df_review['text'].apply(get_sentiment)

# 可选：同时保存 pos / neg / neu 三项，便于后续分析
def get_scores(text):
    try:
        s = analyzer.polarity_scores(str(text))
        return pd.Series([s['pos'], s['neg'], s['neu']])
    except Exception:
        return pd.Series([None, None, None])

df_review[['sentiment_pos', 'sentiment_neg', 'sentiment_neu']] = \
    df_review['text'].apply(get_scores)

# 丢弃情感计算失败的行
df_review = df_review.dropna(subset=['sentiment_score'])

# ================= 2. 画图：星级 vs 情感得分 (箱线图) =================
plt.figure(figsize=(10, 6))
sns.boxplot(x='stars', y='sentiment_score', data=df_review, palette='Set2')
plt.title('Yelp 用户打分与 VADER 情感得分对比 (1-5星)', fontsize=16)
plt.xlabel('用户星级打分', fontsize=12)
plt.ylabel('VADER compound 情感得分 (-1 ~ 1)', fontsize=12)
plt.axhline(0, color='gray', linestyle=':', linewidth=1)  # 0 基准线
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('fig04_情感分析箱线图.png', dpi=150)
plt.show()

# 输出业务结论
mean_sent = df_review.groupby('stars')['sentiment_score'].mean()
print("\n📊 商业结论：")
print(f"1星评价的平均 VADER 情感得分为：{mean_sent.get(1, 0):.3f}")
print(f"3星评价的平均 VADER 情感得分为：{mean_sent.get(3, 0):.3f}")
print(f"5星评价的平均 VADER 情感得分为：{mean_sent.get(5, 0):.3f}")

# 按 VADER 阈值统计情感分布
def vader_label(score):
    if score >= 0.05:
        return '正面'
    elif score <= -0.05:
        return '负面'
    else:
        return '中性'

df_review['sentiment_label'] = df_review['sentiment_score'].apply(vader_label)
print("\nVADER 情感标签分布：")
print(df_review['sentiment_label'].value_counts())

print("\n💡 业务洞察：VADER compound 分数在 [-1,1]，1 星评论应集中在负值区，5 星在正值区。"
      "若 3 星评论的箱体很宽，说明中评用户情绪两极分化，平台应重点拆解 3 星评论中的负面描述。")

# ================= 3. 画图：评论文本词云图 =================
print("\n正在生成高频词云图...")

all_text = " ".join(df_review['text'].astype(str).tolist()).lower()

# 英文文本可用简单停用词过滤（可选）
from wordcloud import STOPWORDS
stopwords = set(STOPWORDS)
# 追加一些 Yelp 常见无意义词
stopwords.update(['place', 'good', 'great', 'food', 'like', 'just', 'really',
                  'get', 'got', 'one', 'also', 'would', 'time', 'go', 'went'])

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    max_words=100,
    colormap='viridis',
    random_state=42,
    stopwords=stopwords
).generate(all_text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Yelp 评论高频词云图', fontsize=16)
plt.tight_layout()
plt.savefig('fig05_词云图.png', dpi=150)
plt.show()

# ================= 4. 保存带情感分数的数据（可选） =================
df_review.to_csv('data/clean/clean_review_with_vader.csv', index=False)

print("\n✅ VADER 情感分析与词云图生成完毕！")
print("请检查：fig4_情感分析箱线图.png、fig5_词云图.png")
print("带情感分数的数据已保存到：data/clean/clean_review_with_vader.csv")
