import re

# 使用原始字符串（raw string）避免转义问题
text = r"""
发件人:	chunming.wang@bitech-automotive.com
发送时间:	2024年8月16日星期五 20:39
收件人:	Tao Min (BiTECH/ESE); Fang Fang (BiTECH/PM); Huang Xiong (BiTECH/ESW3); Hou Shifan (BiTECH/ESW)
主题:	[Chery_T1E_int_Domestic_chip_7_inch_TFT_ICU - 变更管理(CR) #48408] CR009_奇瑞T1E国产化项目新增EPB功能0x4F6信号超时处理

Issue #48408 <http://redmine.bitech-auto.com/redmine/issues/48408#change-379749>  has been updated by Niuniu Lu. 
________________________________[变更记录]



________________________________[变更记录]


变更管理(CR) #48408: CR009_奇瑞T1E国产化项目新增EPB功能0x4F6信号超时处理 <http://redmine.bitech-auto.com/redmine/issues/48408#change-379749> 


*	Author: Tao Min (BiTECH/ESE)
*	Status: Confirmed
*	Priority: Normal
*	Assignee: Niuniu Lu
*	Category: 
*	Target version: 
*	ECR Number: n.a.
*	Planned SW Version / 计划软件版本: SWP02.05.00
*	Baseline Ver. / 基线版本: SWP02.04.05
*	Design Spec Link / 设计文档链接: 
*	Hardware Version / 硬件版本: 
*	Int. in Ver. SoC / 集成版本SoC: 
*	Int. in Ver. MCU / 集成版本MCU: 
*	Code Commit ID / 代码提交ID: 
*	Regression Tester / 回归测试者: 
*	Regression Test Day / 回归测试日: 
*	Impacted Modules / 影响功能块: Epbm.c
*	Test Spec Link / 测试用例链接: Z:\02_Projects\01_Chery\64_Chery_T1E 国际国产化芯片_ 7 inch TFT _ICU\10_Software\06_Systemtest\IT_Test\ITS_CR009_奇瑞T1E国产化项目新增EPB功能0x4F6信号超时处理.xlsx
*	Verification Report / 验证报告: Z:\02_Projects\01_Chery\64_Chery_T1E 国际国产化芯片_ 7 inch TFT _ICU\10_Software\06_Systemtest\IT_Test\ITS_CR009_奇瑞T1E国产化项目新增EPB功能0x4F6信号超时处理.xlsx
*	Deployment details / 部署详情: http://10.179.48.141:3008/deploy/508?component=jenkins&issue_id=48408
*	Commit history / 提交历史: http://10.179.48.141:3008/deploy/508?component=gerrit&issue_id=48408

Files CR009_奇瑞T1E国产化项目新增EPB功能0x4F6信号超时处理.docx <http://redmine.bitech-auto.com/redmine/attachments/download/33131/CR009_%E5%A5%87%E7%91%9ET1E%E5%9B%BD%E4%BA%A7%E5%8C%96%E9%A1%B9%E7%9B%AE%E6%96%B0%E5%A2%9EEPB%E5%8A%9F%E8%83%BD0x4F6%E4%BF%A1%E5%8F%B7%E8%B6%85%E6%97%B6%E5%A4%84%E7%90%86.docx>  (91.8 KB)

________________________________[变更记录]

You have received this notification because you have either subscribed to it, or are involved in it.
To change your notification preferences, please click here: http://hostname/my/account

发件人:	chunming.wang@bitech-automotive.com
发送时间:	2024年8月16日星期五 20:30
收件人:	Fang Fang (BiTECH/PM); Huang Xiong (BiTECH/ESW3); Zhang Hongli (BiTECH/EST2); Hou Shifan (BiTECH/ESW)
主题:	[Chery_T1E_int_Domestic_chip_7_inch_TFT_ICU - Bug #48497] (Checked) 二级菜单超速报警 OFF文言翻译与实表不一致

Issue #48497 <http://redmine.bitech-auto.com/redmine/issues/48497#change-379748>  has been updated by Niuniu Lu. 
________________________________[变更记录]

*	File 二级菜单超速报警 OFF.jpg <http://redmine.bitech-auto.com/redmine/attachments/33533/%E4%BA%8C%E7%BA%A7%E8%8F%9C%E5%8D%95%E8%B6%85%E9%80%9F%E6%8A%A5%E8%AD%A6%20OFF.jpg>  added
*	Status changed from Confirmed to Checked
*	Assignee changed from Niuniu Lu to Zhang Hongli (BiTECH/EST)
*	Regression Test Ver. / 回归测试版本 set to swp02.06.00
*	Regression Tester / 回归测试者 set to Niuniu Lu
*	Regression Test Day / 回归测试日 set to 08/16/2024
*	Verification Report / 验证报告 set to /

验证结果：Pass
验证版本：swp02.06.00
验证环境：台架
验证时间：2024/8/16
验证人：卢妞妞
备注：验证Pass,该问题可关闭
详情可见图片二级菜单超速报警 OFF.jpg

________________________________[变更记录]


Bug #48497: 二级菜单超速报警 OFF文言翻译与实表不一致 <http://redmine.bitech-auto.com/redmine/issues/48497#change-379748> 


*	Author: Niuniu Lu
*	Status: Checked
*	Priority: Normal
*	Assignee: Zhang Hongli (BiTECH/EST)
*	Category: 
*	Target version: 
*	Planned SW Version / 计划软件版本: SWP02.06.00
*	Reproduce Steps / 问题再现步骤: 1.set D1 mode 2.进入二级菜单 3.进入超速报警设置，设置超速报警为OFF 4.返回二级菜单 期待结果：第3步之后，OFF为英语显示；第4步之后，二级超速报警的OFF为英语表示。 实际结果：第3步之后，OFF为英语显示；第4步之后，二级超速报警的OFF为阿语表示。 详情可见超速报警OFF.jpg，超速报警的文言翻译.png
*	Reproducibility Rate / 再现率: 100%
*	Severity / 严重度: A
*	Found In Version (SoC) / 发现版本: SWP02.05.00
*	Found In Version (MCU) / 发现版本: SWP02.05.00
*	Test Environment / 测试环境: On Bench
*	Found By / 发现者: Niuniu Lu
*	Found Date / 发现日: 08/09/2024
*	Recovery Method / 恢复方法: 暂无
*	Source of Bug / 问题来源: Internal test / 内部测试
*	Feature Category / 问题功能分类: Others / 其他
*	Cause Category / 原因区分: Coding / 编码
*	Root Cause / 问题原因说明: 阿语状态下文言未修改
*	Solution Type / 对策方针: 永久对策
*	Duplicate as / 重复问题票号: 
*	Fix Solution / 修复方案: 修改对应显示文言为OFF
*	Int. in Ver. SoC / 集成版本SoC: SWP02.06.00
*	Int. in Ver. MCU / 集成版本MCU: SWP02.06.00
*	Code Commit ID / 代码提交ID: I8fec19e1a6ffd36bc84c68f11240db2ee6acd466
*	Regression Test Ver. / 回归测试版本: swp02.06.00
*	Regression Tester / 回归测试者: Niuniu Lu
*	Regression Test Day / 回归测试日: 08/16/2024
*	Cross Check Require / 是否需要问题横展: No
*	Cross Check Actions / 问题横展检查: na
*	Impacted Modules / 影响功能块: setting
*	Tags / 标签选项: 
*	Bug Counterpart / Bug对应方: HMI_SubModule
*	Reopened Issue / 重开问题: No
*	Verification Report / 验证报告: /
*	From testcase/问题来源测试用例: Yes
*	Problem push/问题推送: No
*	Bug Owner/问题归属人: Hong Ziyang (BiTECH/ESW)
*	Belonging Department/部门归属: Other
*	Deployment details / 部署详情: http://10.179.48.141:3008/deploy/508?component=jenkins&issue_id=48497
*	Commit history / 提交历史: http://10.179.48.141:3008/deploy/508?component=gerrit&issue_id=48497

“超速报警 OFF”文言翻译与实表不一致
详情可见超速报警OFF.jpg，超速报警的文言翻译.png

Files 超速报警OFF.jpg <http://redmine.bitech-auto.com/redmine/attachments/download/33193/%E8%B6%85%E9%80%9F%E6%8A%A5%E8%AD%A6OFF.jpg>  (93.9 KB)
超速报警的文言翻译.png <http://redmine.bitech-auto.com/redmine/attachments/download/33194/%E8%B6%85%E9%80%9F%E6%8A%A5%E8%AD%A6%E7%9A%84%E6%96%87%E8%A8%80%E7%BF%BB%E8%AF%91.png>  (148 KB)
超速报警OFF.jpg <http://redmine.bitech-auto.com/redmine/attachments/download/33196/%E8%B6%85%E9%80%9F%E6%8A%A5%E8%AD%A6OFF.jpg>  (93.9 KB)
超速报警的文言翻译.png <http://redmine.bitech-auto.com/redmine/attachments/download/33197/%E8%B6%85%E9%80%9F%E6%8A%A5%E8%AD%A6%E7%9A%84%E6%96%87%E8%A8%80%E7%BF%BB%E8%AF%91.png>  (148 KB)
二级菜单超速报警 OFF.jpg <http://redmine.bitech-auto.com/redmine/attachments/download/33533/%E4%BA%8C%E7%BA%A7%E8%8F%9C%E5%8D%95%E8%B6%85%E9%80%9F%E6%8A%A5%E8%AD%A6%20OFF.jpg>  (152 KB)

________________________________[变更记录]

You have received this notification because you have either subscribed to it, or are involved in it.
To change your notification preferences, please click here: http://hostname/my/account
"""



# 使用 re.split() 切割
blocks = re.split(r'^________________________________\[变更记录\]\s*\n', text, flags=re.MULTILINE)

# 获取中间部分
if len(blocks) > 2:
    result = blocks[1].strip()
    print(result)