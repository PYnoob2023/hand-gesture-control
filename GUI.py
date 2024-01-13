import tkinter as tk
from tkinter import messagebox
import os
import subprocess


def start_program():
    try:
        subprocess.run(["python", "007.py"])
    except Exception as e:
        messagebox.showerror("错误", f"启动程序时发生错误：{e}")


def start_bilibili():
    bilibili_path = r"C:\Program Files\bilibili\哔哩哔哩.exe"
    try:
        subprocess.Popen([bilibili_path])
    except Exception as e:
        messagebox.showerror("错误", f"启动哔哩哔哩时发生错误：{e}")


def show_instructions():
    instructions = """
    使用说明：

    手势 'five'：最大化当前窗口
    手势 'fist'：静音系统音量
    手势 'one'：向上滚动
    手势 'two'：向下滚动
    手势 'thumbUp'：模拟按下空格键

    持续手势 'one'：持续向上滚动
    持续手势 'two'：持续向下滚动

    手势 'three'：增加系统音量
    手势 'gun'：减小系统音量

    手势 'six'：退出程序
    """
    messagebox.showinfo("使用说明", instructions)


# 创建主窗口
root = tk.Tk()
root.title("手势控制程序")

# 启动程序按钮
start_program_button = tk.Button(root, text="启动程序", command=start_program)
start_program_button.pack(pady=10)

# 启动哔哩哔哩按钮
start_bilibili_button = tk.Button(root, text="启动哔哩哔哩", command=start_bilibili)
start_bilibili_button.pack(pady=10)

# 使用说明按钮
instructions_button = tk.Button(root, text="使用说明", command=show_instructions)
instructions_button.pack(pady=10)

# 运行主循环
root.mainloop()
