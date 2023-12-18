import requests
import json
import pprint

# 替换为你的学者ID和API Key
scholar_id = "57209018448"
api_key = "52454aa42e8b5e5c4f5860f62a6d4c5f"

# 构建URL和头部信息
url = f"https://api.elsevier.com/content/search/scopus?query=au-id({scholar_id})"
headers = {
    "X-ELS-APIKey": api_key,
    "Accept": "application/json"
}

# 发送请求
response = requests.get(url, headers=headers)

# 解析响应
data = json.loads(response.text)

# 获取学者名字
author_name = data['search-results']['entry'][0]['dc:creator']

# 获取所有文章名
publications = [entry['dc:title'] for entry in data['search-results']['entry']]

print(f"Author Name: {author_name}")
print("Publications:")
for pub in publications:
    print(pub)


print(1)
