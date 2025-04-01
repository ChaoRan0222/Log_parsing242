# -*- encoding: utf-8 -*-
'''
@File    :   Buging.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025/2/27 11:24   念安        1.0         None
'''

import re
import pandas as pd

# 读取txt文件
with open('[Chery_T1E_int_Domestic_chip_7_inch_TFT_ICU]msg.msg_UTF-8.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 以每个“发件人:”和结尾“通知”划分每个任务
tasks = re.split(r'发件人:.*?To change your notification preferences.*?account', content, flags=re.DOTALL)


# 定义提取字段的正则表达式
patterns = {
    'Author': r'\*?\s*Author:\s*(.*)',
    'Status': r'\*?\s*Status:\s*(.*)',
    'Priority': r'\*?\s*Priority:\s*(.*)',
    'Assignee': r'\*?\s*Assignee:\s*(.*)',
    'Category': r'\*?\s*Category:\s*(.*)',
    'Target version': r'\*?\s*Target version:\s*(.*)',
    'Reproduce Steps': r'\*?\s*Reproduce Steps / 问题再现步骤:\s*(.*)',
    'Reproducibility Rate': r'\*?\s*Reproducibility Rate / 再现率:\s*(.*)',
    'Severity': r'\*?\s*Severity / 严重度:\s*(.*)',
    'Found In Version (SoC)': r'\*?\s*Found In Version \(SoC\) / 发现版本:\s*(.*)',
    'Found In Version (MCU)': r'\*?\s*Found In Version \(MCU\) / 发现版本:\s*(.*)',
    'Test Environment': r'\*?\s*Test Environment / 测试环境:\s*(.*)',
    'Found By': r'\*?\s*Found By / 发现者:\s*(.*)',
    'Found Date': r'\*?\s*Found Date / 发现日:\s*(.*)',
    'Recovery Method': r'\*?\s*Recovery Method / 恢复方法:\s*(.*)',
    'Source of Bug': r'\*?\s*Source of Bug / 问题来源:\s*(.*)',
    'Feature Category': r'\*?\s*Feature Category / 问题功能分类:\s*(.*)',
    'Root Cause': r'\*?\s*Root Cause / 问题原因说明:\s*(.*)',
    'Solution Type': r'\*?\s*Solution Type / 对策方针:\s*(.*)',
    'Fix Solution': r'\*?\s*Fix Solution / 修复方案:\s*(.*)',
    'Bug Counterpart': r'\*?\s*Bug Counterpart / Bug对应方:\s*(.*)',
    'Impacted Modules': r'\*?\s*Impacted Modules / 影响功能块:\s*(.*)',
    'Regression Test Ver.': r'\*?\s*Regression Test Ver. / 回归测试版本:\s*(.*)',
    'Regression Tester': r'\*?\s*Regression Tester / 回归测试者:\s*(.*)',
    'Regression Test Day': r'\*?\s*Regression Test Day / 回归测试日:\s*(.*)',
    'Duplicate as': r'\*?\s*Duplicate as / 重复问题票号:\s*(.*)',
    'CCB Conclusion': r'\*?\s*CCB Conclusion / CCB结论:\s*(.*)',
    'OPL Type': r'\*?\s*OPL Type / OPL 分类:\s*(.*)',
    'Expected Feedback Date': r'\*?\s*Expected Feedback Date / 期望回答日:\s*(.*)',
    'Cross Check Require': r'\*?\s*Cross Check Require / 是否需要问题横展:\s*(.*)',
    'Cross Check Actions': r'\*?\s*Cross Check Actions / 问题横展检查:\s*(.*)',
    'Tags': r'\*?\s*Tags / 标签选项:\s*(.*)',
    'Cause Category': r'\*?\s*Cause Category / 原因区分:\s*(.*)',
    'Reopened Issue': r'\*?\s*Reopened Issue / 重开问题:\s*(.*)',
    'Bug Owner': r'\*?\s*Bug Owner / Bug归属人:\s*(.*)',
    'Bug Department': r'\*?\s*Bug归属部门:\s*(.*)',
    'Close by': r'\*?\s*Close by / 闭环确认:\s*(.*)',
    'Deployment details': r'\*?\s*Deployment details / 部署详情:\s*(.*)',
    'Actual duedate': r'\*?\s*Actual duedate / 实际截止日期:\s*(.*)',
    'Object': r'Bug #(\d+):\s*([^<]+)'  # 匹配任务编号和描述

}

# 去掉 Bug 编号和链接的正则表达式
clean_bug_pattern = r'Bug#\d+:\s*|<.*?>'

# 提取“Commit history / 提交历史”字段
commit_history_pattern = r'\*?\s*Commit history / 提交历史:\s*(.*?)\s*^________________________________'


# 存储提取的数据
data = []

# 遍历记录并提取字段
for record in tasks:
    row = {}


    # 提取每个字段
    for key, pattern in patterns.items():
        match = re.search(pattern, record, re.S)  # 使用re.S来匹配多行数据
        if match:
            field_value = match.group(1).strip()
            # 清理掉 Bug#xxx: 和 <http://...> 部分
            cleaned_field_value = re.sub(clean_bug_pattern, '', field_value)
            row[key] = cleaned_field_value.strip()  # 去除首尾空格
        else:
            row[key] = ""  # 如果没有匹配到，设置为空

    # 提取“主题”中的项目、跟踪、#号后的数字
    theme_pattern = r'[\[]([^\]]+)[\]]'  # 提取[]内的内容
    theme_match = re.search(theme_pattern, row.get('Priority', ''))
    if theme_match:
        theme_parts = theme_match.group(1).split()
        if len(theme_parts) >= 3:
            row['项目'] = theme_parts[0]  # 项目
            row['跟踪'] = theme_parts[1]  # 跟踪
            row['#'] = theme_parts[2].replace('#', '')  # #后数字


    # 提取“Commit history / 提交历史”内容
    commit_history_match = re.search(commit_history_pattern, record, re.S)
    if commit_history_match:
        commit_history = commit_history_match.group(1).strip()
        # 去除链接部分
        cleaned_commit_history = re.sub(r'<.*?>', '', commit_history)
        row['描述'] = cleaned_commit_history
    else:
        row['描述'] = ""  # 如果没有匹配到，设置为空



    # 添加一行数据
    data.append(row)

# 6. 创建DataFrame并保存为CSV
df = pd.DataFrame(data)

# 7. 定义CSV的列顺序（第一行字段名称）
columns_mapping={
    '#':'#',
    '项目':'项目',
    '跟踪':'跟踪',
    '':'父任务',
    'Status':'状态',
    'Priority':'优先级',
    'Object':'主题',
    'Author':'作者',
    'Assignee':'指派给',
    '':'更新于',
    'Category':'类别',
    'Target version':'目标版本',
    '':'开始日期',
    '':'计划完成日期',
    '':'预期时间',
    '':'预估工时统计',
    '':'% 完成',
    '':'创建于',
    '':'结束日期',
    '':'最近更新人',
    '':'相关的问题',
    '':'文件',
    '':'ECR Number',
    '':'Planned SW Version / 计划软件版本',
    '':'Baseline Ver. / 基线版本',
    '':'Work Product Link / 成果物链接',
    '':'Design Spec Link / 设计文档链接',
    '':'Code Commit ID / 代码提交ID',
    '':'Branch / Gerrit分支',
    '':'Tes Spec Link / 测试用例链接',
    '':'Verification Report / 验证报告',
    'Reproduce Steps':'Reproduce Steps / 问题再现步骤',
    '':'Feedback / OPL 回复',
    'Reproducibility Rate':'Reproducibility Rate / 再现率',
    'Severity':'Severity / 严重度',
    'Found In Version (SoC)':'Found In Version (SoC) / 发现版本',
    'Found In Version (MCU)':'Found In Version (MCU) / 发现版本',
    '':'Hardware Version / 硬件版本',
    'Test Environment':'Test Environment / 测试环境',
    'Found By':'Found By / 发现者',
    'Found Date':'Report date / 发现日',
    'Recovery Method':'Recovery Method / 恢复方法',
    'Feature Category':'Feature Category / 问题功能分类',
    'Root Cause':'Root Cause / 问题原因说明',
    'Solution Type':'Solution type / 对策方针',
    'Duplicate as':'Duplicate as / 重复问题票号',
    'Fix Solution':'Fix solution / 修复方案',
    '':'Fixed In Ver. SoC / 修复对应版本',
    '':'Fixed In Ver. MCU / 修正对应版本',
    'Regression Test Ver.':'Regression Test Ver. / 回归测试版本',
    'Regression Tester':'Regression Tester / 回归测试者',
    'Regression Test Day':'Regression Test Day / 回归测试日',
    'CCB Conclusion':'CCB Conclusion / CCB结论',
    'OPL Type':'OPL Type / OPL 分类',
    'Cross Check Require':'Cross Check Require / 是否需要问题横展',
    'Cross Check Actions':'Cross Check Actions / 问题横展检查',
    'Impacted Modules':'Impacted Modules / 影响功能块',
    'Tags':'Tags / 标签选项',
    'Bug Counterpart':'Bug Counterpart / Bug对应方',
    'Cause Category':'Cause Category / 原因区分',
    'Reopened Issue':'Reopened Issue / 重开问题',
    'Bug Owner':'Bug Owner / Bug归属人',
    'Bug Department':'Bug归属部门',
    'Close by':'Close by / 闭环确认',
    'Deployment details':'Deployment details / 部署详情',
    'Actual duedate':'Actual duedate / 实际截止日期',
    '':'T19FL_int_Domestic_Variant',
    '':'故事要点',
    '描述':'描述',
    '':'最近批注'
}

# 根据映射修改DataFrame列名
df.rename(columns=columns_mapping, inplace=True)

# 保存为CSV文件
df.to_csv('output.csv', index=False, encoding='utf-8')

print("数据已成功提取并保存为 CSV 文件！")
