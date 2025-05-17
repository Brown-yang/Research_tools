import pandas as pd
import os



csv_dir = 'papers_csv/'

# 所有csv文件路径
csv_files = [
    'cvpr2024_grasp_papers.csv',
    'cvpr2023_grasp_papers.csv',
    'icra2023_grasp_papers.csv',
    'icra2024_grasp_papers.csv',
    'iros2023_grasp_papers.csv',
    'iros2024_grasp_papers.csv',
    'tro2023_grasp_papers.csv',
    'tro2024_grasp_papers.csv'
]


all_df = []

for file in csv_files:
    filepath = os.path.join(csv_dir, file)  # 拼接成完整路径
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        continue
    
    # 添加 Source 字段（如 ICRA2023）
    source_name = file.replace('_grasp_papers.csv', '').upper()
    
    df = pd.read_csv(filepath)
    tmp = df['Paper']
    tmp.name = source_name  # 修改 Series 的列名（即 name）
     
    all_df.append(tmp)

result_df = pd.concat(all_df, axis=1)  # 每列是一个 source

# 保存到本地
output_path = os.path.join(csv_dir, 'grasp_papers_by_source_columns.csv')
result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"✅ 已保存合并文件到：{output_path}")

