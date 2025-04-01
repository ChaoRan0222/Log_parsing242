# Python数据恢复工具 (Python Data Recovery Tool)

## 项目概述

这是一个专门用于从文本文件中提取和处理结构化数据的Python工具包。该工具主要针对从系统导出的消息记录（如邮件、问题跟踪系统等），能够识别、提取并整理各种类型的记录（Bug、CR、Feature、Integration、OPL、Task），形成有组织的数据表格。

## 主要功能

- 从文本文件中提取结构化数据（如Bug报告、CR请求、任务记录等）
- 支持多种记录类型的解析（Bug、CR、Feature、Integration、OPL、Task）
- 自动识别记录字段和属性（作者、状态、优先级、描述等）
- 合并同一ID/主题的多条记录，保留最新状态
- 将提取数据导出为CSV格式
- 提供图形用户界面(GUI)便于操作

## 项目结构

```
Python_DataRecovery02/
│
├── Bug/                  # Bug报告处理模块
│   ├── Buging.py         # Bug文本提取处理
│   └── Bug.py            # Bug数据整合与去重
│
├── CR/                   # 变更请求(CR)处理模块
│   ├── CRing.py          # CR文本提取处理
│   └── CR.py             # CR数据整合与去重
│
├── Feature/              # 功能特性处理模块
│   ├── Featureing.py     # Feature文本提取处理
│   └── Feature.py        # Feature数据整合与去重
│
├── Integration/          # 集成处理模块
│   ├── Integrationing.py # Integration文本提取处理
│   └── Integration.py    # Integration数据整合与去重
│
├── OPL/                  # OPL处理模块
│   ├── OPLing.py         # OPL文本提取处理
│   └── OPL.py            # OPL数据整合与去重
│
├── Task/                 # 任务处理模块 
│   ├── Tasking.py        # Task文本提取处理
│   └── Task.py           # Task数据整合与去重
│
├── Show/                 # 图形界面模块
│   └── show.py           # GUI界面实现
│
├── Common_Models.py      # 通用数据模型与处理函数
├── Summary.py            # 数据汇总处理
└── Test.py               # 测试脚本
```

## 处理流程

1. **数据提取**：使用正则表达式从原始文本文件中提取结构化数据
   - 各种`*ing.py`文件(Buging.py, CRing.py等)负责从原始文本中提取结构化信息
   - 提取的字段包括：作者、状态、优先级、描述、日期等

2. **数据整合**：对提取的数据进行整合、去重和规范化
   - 各种类型文件(Bug.py, CR.py等)负责数据整合和去重
   - 相同ID的记录会被合并，保留状态优先级最高的信息

3. **数据汇总**：将所有类型的数据整合到一起(Summary.py)
   - 合并多种类型的数据到一个综合报表

## 使用说明

### 图形界面操作

1. 运行`Show/show.py`启动图形界面
2. 点击"选择输入文件"按钮，选择需要处理的文本文件
3. 点击"选择生成文件的保存位置"按钮，选择输出目录
4. 点击相应的数据类型按钮(Bug、CR、Feature等)开始处理
5. 处理完成后会显示成功消息

### 命令行操作

也可以直接通过命令行运行各个处理脚本：

1. 运行数据提取脚本：
   ```
   python Bug/Buging.py <input_file> <output_file>
   ```

2. 运行数据整合脚本：
   ```
   python Bug/Bug.py <input_file> <output_file>
   ```

3. 运行数据汇总脚本：
   ```
   python Summary.py
   ```

## 数据字段说明

提取的数据包含多种字段，常见字段包括：

- `#`: 记录编号
- `项目`: 所属项目
- `跟踪`: 记录类型(Bug/CR/Feature等)
- `状态`: 当前状态(Closed/Checked/Confirmed等)
- `优先级`: 任务优先级
- `作者`: 创建者
- `指派给`: 负责人
- `描述`: 详细描述
- `开始日期`: 创建日期
- `计划完成日期`: 预计完成日期

## 注意事项

1. 输入文本文件需为UTF-8编码
2. 确保Python环境已安装必要依赖包(pandas, re等)
3. 各类型处理脚本有特定的正则表达式匹配模式，如需修改适应不同格式的文本，需调整相应正则表达式

## 依赖库

- pandas: 数据处理与CSV输出
- tkinter: 图形界面
- re: 正则表达式解析
- datetime: 日期时间处理
- subprocess: 子进程调用
- os: 文件系统操作

## 作者

念安 (2025/3/5) 