import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://dblp.uni-trier.de/db/journals/trob/trob39.html'
html_file = 'html/tro2023.html'


# 下载或读取缓存页面
if not os.path.exists(html_file):
    print("Downloading webpage...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
else:
    print("Using cached HTML file.")

# 用 lxml 加速解析
with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

# 查找所有论文块
entries = soup.find_all('cite', class_='data')

results = []
for entry in entries:
    title_tag = entry.find('span', class_='title')
    author_tags = entry.find_all('span', itemprop='author')
    pages_tag = entry.find('span', itemprop='pagination')

    if title_tag and author_tags:
        title = title_tag.get_text(strip=True)
        if 'grasp' in title.lower():
            # 标题末尾如果已有句号就不再加
            title = title.strip()
            if title.endswith('.'):
                title_text = title
            else:
                title_text = title + '.'
            
            authors = [a.get_text(strip=True) for a in author_tags]
            authors_str = ', '.join(authors)
            pages = pages_tag.get_text(strip=True) if pages_tag else "N/A"
            
            # 格式：作者（第一行）+换行+标题和页码（第二行）
            formatted_text = f"{authors_str}:\n{title} {pages}"
            results.append([formatted_text])
            
            

# 写入 CSV 文件（启用换行）
csv_file = 'papers_csv/tro2023_grasp_papers.csv'
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Paper'])
    writer.writerows(results)

print(f"\n✅ 共找到 {len(results)} 篇包含 'grasp' 的论文。")
print(f"📄 已保存为：{csv_file}")
