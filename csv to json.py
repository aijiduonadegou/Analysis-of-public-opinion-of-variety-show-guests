import pandas as pd
import json

# 读取 CSV 文件
csv_file_path = 'E:/代码作业/love/guest_sentiment_adjectives.csv'  # 替换为你的 CSV 文件路径
df = pd.read_csv(csv_file_path)

# 转换为指定的 JSON 格式
json_data = df.apply(lambda row: {"guest": row['guest'], "word": row['word'], "score": row['score']}, axis=1).tolist()

# 打印整理后的 JSON 数据
for item in json_data:
    print(item)

# 保存为 JSON 文件
output_json_path = 'E:/代码作业/love/guest_sentiment_adjectives.json'  # 替换为你的输出 JSON 文件路径
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("数据已成功保存为 JSON 文件。")