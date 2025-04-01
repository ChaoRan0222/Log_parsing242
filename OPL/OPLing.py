import re
import pandas as pd
from datetime import datetime, timedelta

# 读取txt文件
with open('../t1e_demestic_202401-202501allmsg_20250304_[变更记录调整]_utf8.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 打印读取的文件内容前500个字符，检查是否正确加载
# print(content[:500])

# 以每个“发件人:”和结尾“通知”划分每个任务
tasks = re.split(r'发件人', content, flags=re.DOTALL)

# 检查分割后的任务
print(f"共找到 {len(tasks)} 个任务。")
for idx, task in enumerate(tasks[:5]):  # 打印前5个任务作为调试
    print(f"任务 {idx}: {task[:20]}")  # 打印任务的前20个字符，以便检查

# 定义提取字段的正则表达式
patterns = {
    'Author': r'\*?\s*Author:\s*(.*?)\s*(?=\*|$)',
    'Status': r'\*?\s*Status:\s*(.*?)\s*(?=\*|$)',
    'Priority': r'\*?\s*Priority:\s*(.*?)\s*(?=\*|$)',
    'Assignee': r'\*?\s*Assignee:\s*(.*?)\s*(?=\*|$)',
    'Work Product Link / 成果物链接': r'\*?\s*Work Product Link / 成果物链接:\s*(.*?)\s*(?=\*|$)',
    'Feedback / OPL 回复': r'\*?\s*Feedback / OPL 回复:\s*(.*?)\s*(?=\*|$)',
    'Object': r'OPL #(\d+):\s*([^<]+)',  # 匹配任务编号和描述
    # '描述': r'\*?\s*Commit history / 提交历史:\s*(.*?)\s*^________________________________',
    '标题': r'\[([^\]]+)\]',  # 提取[]内的内容 项目 和跟踪报告
    '主题': r'#\d+:\s*([^\n<]+)',
    '发送时间': r"发送时间:\s*(\d{4}年\d{1,2}月\d{1,2}日星期[一二三四五六日]\s+\d{1,2}:\d{2})",
    'Close by': r'\*?\s*Close by / 闭环确认\s*([^\n]*)',  # 匹配同一行内容
    '描述':r'Files:(.*?)(?=You have received this notification|$)',
    '开始日期': r'\*?\s*Found Date / 发现日:\s*(.*?)\s*(?=\*|$)',
    '计划完成日期': r'\*?\s*Found Date / 发现日:\s*(.*?)\s*(?=\*|$)',
    # 提取问题跟踪基础信息（has been updated/reported by）
    '问题跟踪': r'(?s)(Issue #\d+.*?has been (reported|updated) by (.*?))\s*[._]',
# 提取所有变更记录（包含Assignee变更）
    '变更记录': r'\*[\t ]*(Assignee changed from (.*?) to (.*?)|Status changed from (.*?) to (.*?)|(\w+.*? changed))(?=\n|\Z)',
    'Files':r'Files\s*([\s\S]+?)\s*?You have received this notification',
    '描述2': r'(?<=________________________________\[变更记录\]\n\n)(.*?)(?=\n\n________________________________\[变更记录\])',
}


# 去掉 Task 编号和链接的正则表达式
clean_bug_pattern = r'Task#\d+:\s*|<.*?>'

# 提取“Commit history / 提交历史”字段
commit_history_pattern = r'\*?\s*Commit history / 提交历史:\s*(.*?)(?=\n\s*\n|$)'

# 新增变更记录提取正则
change_log_pattern = r'(\* .+?)\n(?=\* |_{10,})'


# 存储提取的数据
data = []

# 遍历记录并提取字段
for record in tasks:
    row = {}
# 提取每个字段
    # 修改这部分代码（在for循环内部）
    for key, pattern in patterns.items():
        try:
            match = re.search(pattern, record, re.S)
            if match:
                field_value = match.group(1).strip()

                # 清理字段值（包括Bug编号和链接）
                cleaned_field_value = re.sub(clean_bug_pattern, '', field_value).strip()

                # 提取基础描述内容
                desc_match = re.search(patterns['描述'], record)
                base_desc = []

                # 提取发送时间字符串
                send_time_str = re.search(patterns['发送时间'], record)
                if send_time_str:
                    send_time_str = send_time_str.group(1).strip()
                    try:
                        # 使用正则提取主要日期部分（忽略星期信息）
                        date_part = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', send_time_str)
                        if date_part:
                            # 转换为datetime对象（格式：2024年3月15日 -> %Y年%m月%d日）
                            start_date = datetime.strptime(date_part.group(1), '%Y年%m月%d日')
                            # 开始日期 = 发送时间的日期部分
                            row['开始日期'] = start_date.strftime('%Y-%m-%d')
                            # 计划完成日期 = 开始日期 + 5天
                            planned_date = start_date + timedelta(days=5)
                            row['计划完成日期'] = planned_date.strftime('%Y-%m-%d')
                    except Exception as e:
                        print(f"日期解析失败: {send_time_str}，错误: {e}")
                        row['开始日期'] = ""
                        row['计划完成日期'] = ""
                else:
                    row['开始日期'] = ""
                    row['计划完成日期'] = ""




                # 日期格式转换（在清理后的值上进行）
                if key in ['Found Date', 'Actual duedate', 'Expected Feedback Date',
                           'Regression Test Day','计划完成日期'] and cleaned_field_value:
                    try:
                        # 尝试解析原始格式 mm/dd/yyyy
                        date_obj = datetime.strptime(cleaned_field_value, '%m/%d/%Y')
                        # 如果是Found Date，加5天
                        if key == '计划完成日期':
                            date_obj += timedelta(days=5)
                        cleaned_field_value = date_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        # 如果解析失败，尝试其他可能的格式（根据需要添加）
                        try:
                            date_obj = datetime.strptime(cleaned_field_value, '%Y-%m-%d')
                            if key == '计划完成日期':
                                date_obj += timedelta(days=5)
                            cleaned_field_value = date_obj.strftime('%Y-%m-%d')
                        except:
                            print(f"无法识别的日期格式：{cleaned_field_value}")

                # 将最终处理后的值存入row
                row[key] = cleaned_field_value
                print(f"{key}: {cleaned_field_value}")
            else:
                row[key] = ""
                print(f"{key}: ''")
        except Exception as e:
            print(f"提取字段 {key} 时发生错误: {e}")
            row[key] = ""

        # 如果“标题”字段存在，则提取项目、跟踪、#号后的数字
    if '标题' in row and row['标题']:
        theme_parts = row['标题'].split()
        if len(theme_parts) >= 3:
            row['项目'] = theme_parts[0]  # 项目
            row['跟踪'] = theme_parts[2]  # 跟踪
            # row['#'] = theme_parts[2].replace('#', '')  # #后数字
        # else:
        #     row['项目'] = row['跟踪'] = row['#'] = ""  # 如果格式不匹配，清空值

    # 提取发送时间用于最后的描述字段中
    des_send_time_match = re.search(r"发送时间:\s*(\d{4}年\d{1,2}月\d{1,2}日星期[一二三四五六日]\s+\d{1,2}:\d{2})", record)
    if des_send_time_match:
        send_time = des_send_time_match.group(1).strip()
    else:
        send_time = "-------"  # 如果没有匹配到，设置为空
    # 在描述中追加“发送时间”
    row['描述'] = f"\n时间: {send_time}"


        # 提取问题跟踪信息
    track_match = re.search(patterns['问题跟踪'], record, re.DOTALL)
    if track_match:
        action_type = "报告" if track_match.group(2) == 'reported' else "更新"
        operator = track_match.group(3).strip()
        row['问题跟踪'] = f"{action_type}人: {operator}"

    # 提取所有变更记录
    changes = re.findall(patterns['变更记录'], record, re.MULTILINE)
    change_logs = []

    for change in changes:
        # 提取时间
        change_with_time = f"[时间] {send_time}\n" if send_time else ""
        # Assignee变更处理
        if change[0]:
            old = re.sub(r'$$.*?$$', '', change[1]).strip()  # 移除括号内容
            new = re.sub(r'$$.*?$$', '', change[2]).strip()
            if old and new:  # 只有在old和new都不为空时才添加
                change_logs.append(f"负责人变更: {old} → {new}")
        # Status变更处理
        elif change[3]:
            change_logs.append(f"状态变更: {change[3]} → {change[4]}")
        # 其他变更类型
        elif change[5]:
            change_logs.append(f"其他变更: {change[5]}")

    # 结构化描述字段
    desc_parts = []
    if '问题跟踪' in row:
        desc_parts.append(f"[问题跟踪]\n{row['问题跟踪']}")
    if change_logs:
        desc_parts.append("[变更记录]\n" + "\n".join(change_logs))

    # row['描述'] = "\n".join([row['描述']] + desc_parts)

    # 提取 "描述2" 并合并到 "描述"
    desc2_match = re.search(patterns['描述2'], record, re.S)
    if desc2_match:
        desc2_content = desc2_match.group(1).strip()
        if desc2_content:  # 确保描述2有内容
            row['描述'] += f"\n[附加描述]\n{desc2_content}"







    # 添加一行数据
    data.append(row)

# 7. 定义CSV的列顺序（第一行字段名称）
columns_mapping = {
    '主题':'主题',
    'Object': '#',
    '开始日期': '开始日期',
    '计划完成日期':'计划完成日期',
    '% 完成':'% 完成',
    '项目': '项目',
    '跟踪': '跟踪',
    'Status': '状态',
    'Priority': '优先级',
    'Author': '作者',
    'Assignee': '指派给',
    'Work Product Link / 成果物链接': 'Work Product Link / 成果物链接',
    'Close by': 'Close by / 闭环确认',
    'Feedback / OPL 回复':'Feedback / OPL 回复',
    '描述': '描述',
    'Files':'Files'
}



# 解析“发送时间”并转换为 datetime 对象
def parse_send_time(send_time_str):
    try:
        # 使用正则提取时间字符串并转换
        match = re.search(r"发送时间:\s*(\d{4}年\d{1,2}月\d{1,2}日星期[一二三四五六日]\s+\d{1,2}:\d{2})", send_time_str)
        if match:
            send_time_str = match.group(1).strip()
            # 尝试解析“发送时间”
            date_obj = datetime.strptime(send_time_str, '%Y年%m月%d日星期%a %H:%M')
            return date_obj
    except Exception as e:
        print(f"解析发送时间时发生错误: {e}")
    return None



# 提取“发送时间”字段并转换为datetime格式
for row in data:
    send_time_str = row.get('发送时间', '')
    if send_time_str:
        row['发送时间'] = parse_send_time(send_time_str)

# 处理每一行的 '% 完成' 字段
for row in data:
    # 获取 'Status' 字段的值
    status = row.get('Status', '').strip()

    # 根据 Status 设置 % 完成
    if status in ['Closed', 'Checked', 'Resolved', 'Confirmed']:
        row['% 完成'] = '100%'
    elif status in ['New', 'Rejected', 'In Progress','Deferred']:
        row['% 完成'] = '0%'
    else:
        row['% 完成'] = ''  # 如果没有匹配的状态，则可以设置为空

# 创建DataFrame并排序
df = pd.DataFrame(data)
# 新增过滤逻辑：只保留跟踪字段为"Bug"的条目
# 先标准化数据（去除首尾空格，处理空值）
df['跟踪'] = df['跟踪'].str.strip().fillna('')
# 然后过滤
df = df[df['跟踪'] == 'OPL']
# print(df)

# 按 'Object' 和 '发送时间' 排序，保留每个 Object 最新的一条记录
df['发送时间'] = pd.to_datetime(df['发送时间'], errors='coerce')  # 转换为 datetime 类型，无法转换的会变为 NaT
df_sorted = df.sort_values(by=['Object', '开始日期'], ascending=[True, False])  # 按Object和发送时间排序
# df_latest = df_sorted.drop_duplicates('Object', keep='first')  # 保留每个 Object 最新的记录



# # 定义一个函数，用来合并相同 Object 的描述
def merge_descriptions(group):
    # 保留最新的一条记录（即发送时间最晚的那条）
    latest_record = group.iloc[0]
    # 将其他记录的描述合并到最新记录的描述中
    descriptions = group['描述'].iloc[1:].dropna().tolist()  # 排除空值
    if descriptions:
        latest_record['描述'] += ' '.join(descriptions)
    return latest_record

#
# # 进行列重命名，并避免 inplace 操作
# # df_latest = df_latest.rename(columns=columns_mapping)
# df_latest = df_sorted.rename(columns=columns_mapping)
#
#
# # 重新排列列的顺序
# df_latest = df_latest[list(columns_mapping.values())]
#
# # 保存为CSV文件
# df_latest.to_csv('t1e_demestic_202401-202501allmsg_utf8_OPLing.csv', index=False, encoding='utf-8', date_format='%Y-%m-%d')
#
# print("数据已成功提取并保存为 CSV 文件！")

# 确保 "Object" 字段是字符串类型
df_sorted['Object'] = df_sorted['Object'].astype(str).fillna('')

# 生成 "id+主题" 字段
df_sorted['id+主题'] = df_sorted['跟踪'] + ' #' + df_sorted['Object'] + ' ' + df_sorted['主题']

# 进行列重命名，并避免 inplace 操作
df_latest = df_sorted.rename(columns=columns_mapping)

# 重新排列列顺序，把 "id+主题" 放在最前面
columns_order = ['id+主题'] + list(columns_mapping.values())  # 确保它是第一列
df_latest = df_latest[columns_order]

# 保存 CSV 文件
df_latest.to_csv('t1e_demestic_202401-202501allmsg_utf8OPLing.csv', index=False, encoding='utf-8', date_format='%Y-%m-%d')

print("数据已成功提取并保存为 CSV 文件！")
