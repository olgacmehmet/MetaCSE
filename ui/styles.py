# ui/styles.py
import customtkinter as ctk
from tkinter import ttk


class UIStyler:
    """界面样式管理类"""

    def __init__(self):
        self.style = ttk.Style()
        self.configure_theme()

    def configure_theme(self):
        """配置全局主题"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 表格样式配置
        style = ttk.Style()
        style.configure("Treeview.Heading",
                    background="#f0f0f0",  # 浅灰色
                    foreground="#2c3e50",  # 深灰色文字
                    font=("Microsoft YaHei", 24, "bold"),
                    borderwidth=1,
                    relief="solid",
                    padding=8)  # 增加标题内边距
        style.configure("Treeview", 
                    font=("Microsoft YaHei", 24),  # 数据字体13pt
                    rowheight=60,  # 行高增加到40像素
                    fieldbackground="#ffffff")
        
