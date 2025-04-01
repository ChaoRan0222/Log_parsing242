# -*- encoding: utf-8 -*-
'''
@File    :   Summary.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025/3/5 11:03   念安        1.0         None
'''

import os
import pandas as pd

# 定义文件夹和文件路径
folders = ["Bug", "CR", "Feature", "Integration", "OPL", "Task"]
files = [os.path.join(folder, f"t1e_demestic_202401-202501allmsg_utf8{folder}.csv") for folder in folders]

# 读取所有 CSV 文件
dfs = [pd.read_csv(file, encoding='utf-8') for file in files]

# 合并所有数据
df = pd.concat(dfs, ignore_index=True)

# 确保 'ID' 和 '描述' 字段存在
if 'ID' in df.columns and '描述' in df.columns:
    # 按 'ID' 进行分组，并合并 '描述' 字段
    df['描述'] = df.groupby('ID')['描述'].transform(lambda x: '\n'.join(x.dropna().astype(str)))

    # 去重，保留每个 ID 的第一条记录
    df = df.drop_duplicates(subset=['ID'])

# 保存合并后的文件
output_file = "t1e_demestic_202401-202501allmsg_utf8_nianan.csv"
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"合并完成，文件已保存至 {output_file}")
