import re
import pandas as pd
from datetime import datetime, timedelta
import sys

if len(sys.argv) < 3:
    print("使用方法: python Buging.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]


# 读取txt文件
# with open('../t1e_demestic_202401-202501allmsg_20250304_[变更记录调整]_utf8.txt', 'r', encoding='utf-8') as file:
with open(input_file, 'r', encoding='utf-8') as file:
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
    'Category': r'\*?\s*Category:\s*(.*?)\s*(?=\*|$)',
    'Target version': r'\*?\s*Target version:\s*(.*?)\s*(?=\*|$)',
    'Planned SW Version / 计划软件版本':r'\*?\s*Planned SW Version / 计划软件版本:\s*(.*?)\s*(?=\*|$)',
    'Reproduce Steps': r'\*?\s*Reproduce Steps / 问题再现步骤:\s*(.*?)\s*(?=\*|$)',
    'Reproducibility Rate': r'\*?\s*Reproducibility Rate / 再现率:\s*(.*?)\s*(?=\*|$)',
    'Severity': r'\*?\s*Severity / 严重度:\s*(.*?)\s*(?=\*|$)',
    'Found In Version (SoC)': r'\*?\s*Found In Version \(SoC\) / 发现版本:\s*(.*?)\s*(?=\*|$)',
    'Found In Version (MCU)': r'\*?\s*Found In Version \(MCU\) / 发现版本:\s*(.*?)\s*(?=\*|$)',
    'Test Environment': r'\*?\s*Test Environment / 测试环境:\s*(.*?)\s*(?=\*|$)',
    'Found By': r'\*?\s*Found By / 发现者:\s*(.*?)\s*(?=\*|$)',
    'Found Date': r'\*?\s*Found Date / 发现日:\s*(.*?)\s*(?=\*|$)',
    'Recovery Method': r'\*?\s*Recovery Method / 恢复方法:\s*(.*?)\s*(?=\*|$)',
    'Source of Bug': r'\*?\s*Source of Bug / 问题来源:\s*(.*?)\s*(?=\*|$)',
    'Feature Category': r'\*?\s*Feature Category / 问题功能分类:\s*(.*?)\s*(?=\*|$)',
    'Root Cause': r'\*?\s*Root Cause / 问题原因说明:\s*(.*?)\s*(?=\*|$)',
    'Solution Type': r'\*?\s*Solution Type / 对策方针:\s*(.*?)\s*(?=\*|$)',
    'Fix Solution': r'\*?\s*Fix Solution / 修复方案:\s*(.*?)\s*(?=\*|$)',
    'Bug Counterpart': r'\*?\s*Bug Counterpart / Bug对应方:\s*(.*?)\s*(?=\*|$)',
    'Impacted Modules': r'\*?\s*Impacted Modules / 影响功能块:\s*(.*?)\s*(?=\*|$)',
    'Regression Test Ver.': r'\*?\s*Regression Test Ver. / 回归测试版本:\s*(.*?)\s*(?=\*|$)',
    'Regression Tester': r'\*?\s*Regression Tester / 回归测试者:\s*(.*?)\s*(?=\*|$)',
    'Regression Test Day': r'\*?\s*Regression Test Day / 回归测试日:\s*(.*?)\s*(?=\*|$)',
    'Duplicate as': r'\*?\s*Duplicate as / 重复问题票号:\s*(.*?)\s*(?=\*|$)',
    'CCB Conclusion': r'\*?\s*CCB Conclusion / CCB结论:\s*(.*?)\s*(?=\*|$)',
    'OPL Type': r'\*?\s*OPL Type / OPL 分类:\s*(.*?)\s*(?=\*|$)',
    'Expected Feedback Date': r'\*?\s*Expected Feedback Date / 期望回答日:\s*(.*?)\s*(?=\*|$)',
    'Cross Check Require': r'\*?\s*Cross Check Require / 是否需要问题横展:\s*(.*?)\s*(?=\*|$)',
    'Cross Check Actions': r'\*?\s*Cross Check Actions / 问题横展检查:\s*(.*?)\s*(?=\*|$)',
    'Tags': r'\*?\s*Tags / 标签选项:\s*(.*?)\s*(?=\*|$)',
    'Cause Category': r'\*?\s*Cause Category / 原因区分:\s*(.*?)\s*(?=\*|$)',
    'Reopened Issue': r'\*?\s*Reopened Issue / 重开问题:\s*(.*?)\s*(?=\*|$)',
    'Bug Owner': r'\*?\s*Bug Owner / Bug归属人:\s*(.*?)\s*(?=\*|$)',
    'Bug Department': r'\*?\s*Bug归属部门:\s*(.*?)\s*(?=\*|$)',
    'Close by': r'\*?\s*Close by / 闭环确认:\s*(.*?)\s*(?=\*|$)',
    'Deployment details': r'\*?\s*Deployment details / 部署详情:\s*(.*?)\s*(?=\*|$)',
    'Actual duedate': r'\*?\s*Actual duedate / 实际截止日期:\s*(.*?)\s*(?=\*|$)',
    'Object': r'Bug #(\d+):\s*([^<]+)',  # 匹配任务编号和描述
    # '描述': r'\*?\s*Commit history / 提交历史:\s*(.*?)\s*^________________________________',
    '标题': r'\[([^\]]+)\]',  # 提取[]内的内容 项目 和跟踪报告
    '主题': r'#\d+:\s*([^\n<]+)',
    '发送时间':r"发送时间:\s*(\d{4}年\d{1,2}月\d{1,2}日星期[一二三四五六日]\s+\d{1,2}:\d{2})",
    # '描述2': r'(?s)((?:has been (?:reported|updated) by.*?)(?:\n\*.*?(?:changed|updated).*?)+)'
    '描述':r'Files:(.*?)(?=You have received this notification|$)',
    '开始日期': r'\*?\s*Found Date / 发现日:\s*(.*?)\s*(?=\*|$)',
    '计划完成日期': r'\*?\s*Found Date / 发现日:\s*(.*?)\s*(?=\*|$)',
    'Code Commit ID / 代码提交ID': r'\*?\s*Code Commit ID / 代码提交ID:\s*(.*?)\s*(?=\*|$)',
    'Verification Report / 验证报告': r'\*?\s*Verification Report / 验证报告:\s*(.*?)\s*(?=\*|$)',
    'Int. in Ver. SoC / 集成版本SoC': r'\*?\s*Int. in Ver. SoC / 集成版本SoC:\s*(.*?)\s*(?=\*|$)',
    'Int. in Ver. MCU / 集成版本MCU': r'\*?\s*Int. in Ver. MCU / 集成版本MCU:\s*(.*?)\s*(?=\*|$)',
    'From testcase/问题来源测试用例': r'\*?\s*From testcase/问题来源测试用例:\s*(.*?)\s*(?=\*|$)',
    'Commit history / 提交历史': r'\*?\s*Commit history / 提交历史:\s*(https?://[^\s]*)',
    # 提取问题跟踪基础信息（has been updated/reported by）
    '问题跟踪': r'(?s)(Issue #\d+.*?has been (reported|updated) by (.*?))\s*[._]',
# 提取所有变更记录（包含Assignee变更）
    '变更记录': r'\*[\t ]*(Assignee changed from (.*?) to (.*?)|Status changed from (.*?) to (.*?)|(\w+.*? changed))(?=\n|\Z)',
    'Files':r'Files\s*([\s\S]+?)\s*?You have received this notification',
    '描述2': r'(?<=________________________________\[变更记录\]\n\n)(.*?)(?=\n\n________________________________\[变更记录\])',
    'id+主题': 'id+主题'
}


# 去掉 Bug 编号和链接的正则表达式
clean_bug_pattern = r'Bug#\d+:\s*|<.*?>'

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
            # row['项目'] = row['跟踪'] = row['#'] = ""  # 如果格式不匹配，清空值

    # 提取发送时间用于最后的描述字段中
    des_send_time_match = re.search(r"发送时间:\s*(\d{4}年\d{1,2}月\d{1,2}日星期[一二三四五六日]\s+\d{1,2}:\d{2})", record)
    if des_send_time_match:
        send_time = des_send_time_match.group(1).strip()
    else:
        send_time = "-------"  # 如果没有匹配到，设置为空
    # 在描述中追加“发送时间”
    row['描述'] = f"\n时间: {send_time}"

    # 提取“Commit history / 提交历史”内容
    # commit_history_match = re.search(commit_history_pattern, record, re.S)
    # if commit_history_match:
    #     commit_history = commit_history_match.group(1).strip()
    #     # 去除链接部分
    #     cleaned_commit_history = re.sub(r'<.*?>', '', commit_history)
    #     row['描述'] = cleaned_commit_history
    # else:
    #     row['描述'] = ""  # 如果没有匹配到，设置为空

        # # 提取“Files”部分（包括文件信息）
        # files_match = re.search(r'\*?\s*Commit history / 提交历史:\s*([^\n]+)(?=\s*Files)(.*?)(?=\s*__________|$)',
        #                         record, re.S)
        # if files_match:
        #     files_content = files_match.group(2).strip()
        #     row['Files'] = files_content
        # else:
        #     row['Files'] = ""  # 如果没有匹配到，设置为空

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


    # 更新"Planned SW Version / 计划软件版本"为空的字段为"TBD"
    if not row["Planned SW Version / 计划软件版本"]:
        row["Planned SW Version / 计划软件版本"] = "TBD"


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
    'Category': '类别',
    'Planned SW Version / 计划软件版本':'Planned SW Version / 计划软件版本',
    'Target version': '目标版本',
    'Reproduce Steps': 'Reproduce Steps / 问题再现步骤',
    'Reproducibility Rate': 'Reproducibility Rate / 再现率',
    'Severity': 'Severity / 严重度',
    'Found In Version (SoC)': 'Found In Version (SoC) / 发现版本',
    'Found In Version (MCU)': 'Found In Version (MCU) / 发现版本',
    'Test Environment': 'Test Environment / 测试环境',
    'Found By': 'Found By / 发现者',
    'Found Date': 'Found Date / 发现日',
    'Source of Bug':'Source of Bug / 问题来源',
    'Recovery Method': 'Recovery Method / 恢复方法',
    'Feature Category': 'Feature Category / 问题功能分类',
    'Code Commit ID / 代码提交ID':'Code Commit ID / 代码提交ID',
    'Verification Report / 验证报告':'Verification Report / 验证报告',
    'Int. in Ver. SoC / 集成版本SoC':'Int. in Ver. SoC / 集成版本SoC',
    'Int. in Ver. MCU / 集成版本MCU':'Int. in Ver. MCU / 集成版本MCU',
    'From testcase/问题来源测试用例':'From testcase/问题来源测试用例',
    'Commit history / 提交历史':'Commit history / 提交历史',
    'Root Cause': 'Root Cause / 问题原因说明',
    'Solution Type': 'Solution type / 对策方针',
    'Duplicate as': 'Duplicate as / 重复问题票号',
    'Fix Solution': 'Fix solution / 修复方案',
    'Regression Test Ver.': 'Regression Test Ver. / 回归测试版本',
    'Regression Tester': 'Regression Tester / 回归测试者',
    'Regression Test Day': 'Regression Test Day / 回归测试日',
    'CCB Conclusion': 'CCB Conclusion / CCB结论',
    'OPL Type': 'OPL Type / OPL 分类',
    'Cross Check Require': 'Cross Check Require / 是否需要问题横展',
    'Cross Check Actions': 'Cross Check Actions / 问题横展检查',
    'Impacted Modules': 'Impacted Modules / 影响功能块',
    'Tags': 'Tags / 标签选项',
    'Bug Counterpart': 'Bug Counterpart / Bug对应方',
    'Cause Category': 'Cause Category / 原因区分',
    'Reopened Issue': 'Reopened Issue / 重开问题',
    'Bug Owner': 'Bug Owner / Bug归属人',
    'Bug Department': 'Bug归属部门',
    'Close by': 'Close by / 闭环确认',
    'Deployment details': 'Deployment details / 部署详情',
    'Actual duedate': 'Actual duedate / 实际截止日期',
    '描述': '描述',
    'Files':'Files',
    'id+主题':'id+主题',

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
df = df[df['跟踪'] == 'Bug']
# print(df)

# 按 'Object' 和 '发送时间' 排序，保留每个 Object 最新的一条记录
df['发送时间'] = pd.to_datetime(df['发送时间'], errors='coerce')  # 转换为 datetime 类型，无法转换的会变为 NaT
df_sorted = df.sort_values(by=['Object', '开始日期'], ascending=[True, False])  # 按Object和发送时间排序
# df_latest = df_sorted.drop_duplicates('Object', keep='first')  # 保留每个 Object 最新的记录

# 如果 'Planned SW Version / 计划软件版本' 字段为空，设置为 'TBD'


# # 定义一个函数，用来合并相同 Object 的描述
def merge_descriptions(group):
    # 保留最新的一条记录（即发送时间最晚的那条）
    latest_record = group.iloc[0]
    # 将其他记录的描述合并到最新记录的描述中
    descriptions = group['描述'].iloc[1:].dropna().tolist()  # 排除空值
    if descriptions:
        latest_record['描述'] += ' '.join(descriptions)
    return latest_record


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
df_latest.to_csv('t1e_demestic_202401-202501allmsg_utf8Buging.csv', index=False, encoding='utf-8', date_format='%Y-%m-%d')

print("数据已成功提取并保存为 CSV 文件！")