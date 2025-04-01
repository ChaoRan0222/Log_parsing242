# -*- encoding: utf-8 -*-
'''
@File    :   show.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025/3/5 13:36   念安        1.0         None
'''

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

PROCESS_MAPPING = {
    "Bug": ("../Bug/Buging.py", "../Bug/Bug.py"),
    "CR": ("../CR/CRing.py", "../CR/CR.py"),
    "Feature": ("../Feature/Featureing.py", "../Feature/Feature.py"),
    "Integration": ("../Integration/Integrationing.py", "../Integration/Integration.py"),
    "OPL": ("../OPL/OPLing.py", "../OPL/OPL.py"),
    "Task": ("../Task/Tasking.py", "../Task/Task.py")
}

def select_input_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if input_file_path:
        input_file_label.config(text=f"已选择文件: {input_file_path}")

def select_output_directory():
    global output_directory
    output_directory = filedialog.askdirectory()
    if output_directory:
        output_directory_label.config(text=f"生成文件将保存到: {output_directory}")

def process_selected(selection):
    if not input_file_path:
        messagebox.showerror("错误", "请先选择输入文件！")
        return
    if not output_directory:
        messagebox.showerror("错误", "请先选择生成文件的保存位置！")
        return

    input_file = input_file_path
    first_script, second_script = PROCESS_MAPPING[selection]

    # 检查脚本文件是否存在
    if not os.path.exists(first_script):
        messagebox.showerror("错误", f"{first_script} 文件不存在！")
        return
    if not os.path.exists(second_script):
        messagebox.showerror("错误", f"{second_script} 文件不存在！")
        return

    # 生成第一个文档的路径
    first_output_file = os.path.join(output_directory, f"{selection}_first_output.csv")
    try:
        subprocess.run(["python", first_script, input_file, first_output_file], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"{first_script} 处理出错: {e}")
        return

    # 生成第二个文档的路径
    second_output_file = os.path.join(output_directory, f"{selection}_second_output.csv")
    try:
        subprocess.run(["python", second_script, first_output_file, second_output_file], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"{second_script} 处理出错: {e}")
        return

    messagebox.showinfo("完成", f"{selection} 处理完成！")

# 初始化全局变量
input_file_path = ""
output_directory = ""

# 创建主窗口
root = tk.Tk()
root.title("数据处理可视化界面")

# 选择输入文件按钮
select_input_button = tk.Button(root, text="选择输入文件", command=select_input_file)
select_input_button.pack(pady=10)

input_file_label = tk.Label(root, text="未选择文件")
input_file_label.pack()

# 选择输出目录按钮
select_output_button = tk.Button(root, text="选择生成文件的保存位置", command=select_output_directory)
select_output_button.pack(pady=10)

output_directory_label = tk.Label(root, text="未选择保存位置")
output_directory_label.pack()

# 创建处理按钮
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

for process in PROCESS_MAPPING.keys():
    button = tk.Button(button_frame, text=process, command=lambda p=process: process_selected(p))
    button.pack(side=tk.LEFT, padx=10)

# 运行主循环
root.mainloop()