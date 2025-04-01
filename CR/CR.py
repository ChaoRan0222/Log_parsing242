# -*- encoding: utf-8 -*-
'''
@File    :   Bug.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025/2/28 10:36   念安        1.0         None
'''

import csv
from collections import defaultdict

# 状态优先级（数值越大，优先级越高）
status_priority = {
    "Closed": 4,
    "Checked": 3,
    "Confirmed": 2,
    "Resolved": 1
}

# 用于存储描述信息的字典
grouped_descriptions = defaultdict(list)
# 记录#对应的最新数据
data_by_id = {}

# 读取 CSV 文件并分组
with open('t1e_demestic_202401-202501allmsg_utf8CRing.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)  # 读取所有行数据
    fieldnames = reader.fieldnames  # 获取表头

    for row in rows:
        obj = row['#']  # 获取 '#'
        description = row['描述']  # 获取 '描述'
        grouped_descriptions[obj].append(description)

        # 如果当前ID已经存在，进行状态优先级判断
        if obj in data_by_id:
            existing_row = data_by_id[obj]
            if status_priority.get(row['状态'], 0) > status_priority.get(existing_row['状态'], 0):
                data_by_id[obj] = row  # 替换为状态优先级更高的记录

            # 更新最新的开始日期和计划完成日期
            existing_row['开始日期'] = row['开始日期']
            existing_row['计划完成日期'] = row['计划完成日期']
        else:
            data_by_id[obj] = row  # 记录最新的数据

# 更新描述字段，合并描述内容
for obj, row in data_by_id.items():
    row['描述'] = '\n'.join(grouped_descriptions[obj])

# 写入去重后的 CSV 文件
with open('t1e_demestic_202401-202501allmsg_utf8CR.csv', mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_by_id.values())  # 只写入最新的数据

print("CSV 文件更新完成！")
