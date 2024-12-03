import json

import pandas as pd

# 加载Excel文件
excel_file = '数据整理-SLP-20240108.xlsx'
sheet_name = '原始数据'  # Excel表单名称

# 读取特定列
specific_columns = ['Name', 'shape', 'Surface modification', 'Substrate1', 'Substrate2']  # 假设你想读取A和C列
df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=specific_columns)

# 创建一个空字典来存储结果
unique_list = []

# 对每一列进行处理
for column in specific_columns:
    # 去除列中字符串的前后空格
    df[column] = df[column].str.strip()

    # 去除重复值和空字符串
    unique_values = df[column].dropna().unique()
    unique_values = [value for value in unique_values if value != ""]

    # 将列中的唯一值映射到一个数字
    column_dict = {value: idx for idx, value in enumerate(unique_values)}

    # 添加到结果字典中
    unique_list.append(column_dict)

unique_json = json.dumps(unique_list, indent=4)

# 显示结果
print(unique_json)
