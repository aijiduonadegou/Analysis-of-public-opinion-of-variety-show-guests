import pandas as pd
import jieba
import re
from collections import Counter
import json
import pysenti

# 数据清洗函数
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # 去除URL
    text = re.sub(r'[^\w\s]', '', text)  # 去除特殊字符
    text = re.sub(r'\s+', ' ', text).strip()  # 去除多余空格并去除首尾空格
    return text

# 加载停用词
def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
    return stopwords

# 加载情感词典
def load_sentiment_dict(pos_path, neg_path):
    pos_words = set()
    neg_words = set()
    
    with open(pos_path, 'r', encoding='utf-8') as f:
        for line in f:
            pos_words.add(line.strip())
    
    with open(neg_path, 'r', encoding='utf-8') as f:
        for line in f:
            neg_words.add(line.strip())
    
    return pos_words, neg_words

# 分词并统计情感形容词词频和情感得分
def get_sentiment_adjectives(text, stopwords, pos_words, neg_words):
    # 使用 pysenti 进行情感分析
    result = pysenti.classify(text)
    # 提取情感词
    sentiment_words = []
    for key, value in result.items():
        if isinstance(value, dict) and 'sentiment' in value:
            for sentiment in value['sentiment']:
                if sentiment['score'] != 0:
                    word = sentiment['key']
                    if word in pos_words or word in neg_words:
                        if word not in stopwords:
                            sentiment_words.append((word, sentiment['score']))
    return sentiment_words

# 读取CSV文件
df = pd.read_csv('E:/代码作业/love/comments.csv')

# 加载停用词
stopwords_path = 'E:/代码作业/love/hit_stopwords.txt'  # 停用词文件路径
stopwords = load_stopwords(stopwords_path)

# 加载情感词典
pos_path = 'E:/代码作业/love/pos_all_dict.txt'
neg_path = 'E:/代码作业/love/neg_all_dict.txt'
pos_words, neg_words = load_sentiment_dict(pos_path, neg_path)

# 处理数据
guest_sentiment_data = []

for index, row in df.iterrows():
    cleaned_comment = clean_text(row['comment'])
    sentiment_adjectives = get_sentiment_adjectives(cleaned_comment, stopwords, pos_words, neg_words)
    guest = row['guest']
    
    for word, score in sentiment_adjectives:
        guest_sentiment_data.append({
            'guest': guest,
            'word': word,
            'score': score
        })

# 转换为DataFrame
output_df = pd.DataFrame(guest_sentiment_data)

# 保存处理后的数据为CSV文件
output_path = 'E:/代码作业/love/guest_sentiment_adjectives.csv'
output_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("数据处理完成，情感形容词的词频和情感得分已保存为CSV文件。")