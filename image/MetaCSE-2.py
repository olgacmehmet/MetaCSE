import customtkinter as ctk
from tkinter import ttk

class MetaCSEApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MetaCSE v1.0.0 - Polylanger")
        self.geometry("1024x768")
        
        # 配置主题和颜色
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 主布局容器
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 顶部标签导航
        self.create_tab_view()
        # 底部信息栏
        self.create_footer()
        
    def create_tab_view(self):
        # 创建标签容器
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.pack(fill="both", expand=True)
        
        # 添加三个标签页
        self.tab_view.add("查询")
        self.tab_view.add("配置")
        self.tab_view.add("帮助")
        
        # 配置标签样式
        self.tab_view.configure(
            segmented_button_selected_color="#3498db",
            segmented_button_selected_hover_color="#2980b9",
            text_color="white"
        )
        
        # 构建查询页内容
        self.build_query_tab()
        
    def build_query_tab(self):
        tab = self.tab_view.tab("查询")
        
        # 参数设置区域
        param_frame = ctk.CTkFrame(tab, corner_radius=5)
        param_frame.pack(fill="x", padx=10, pady=10)
        
        # 第一行参数
        row0 = ctk.CTkFrame(param_frame)
        row0.pack(fill="x", pady=5)
        
        labels = ["线程数:", "查询页数:", "模式:", "存储模式:", "搜索引擎:"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(row0, text=text, width=80).grid(row=0, column=i*2, padx=5)
            
            if text == "线程数:":
                opt = ctk.CTkOptionMenu(row0, values=["1", "5", "10", "20", "30"], width=80)
                opt.set("5")
            elif text == "查询页数:":
                opt = ctk.CTkOptionMenu(row0, values=[str(i) for i in [1,2,3,4,5,10,15,20,30,50,80,100,200,300,500,1000]], width=100)
                opt.set("1")
            else:
                opt = ctk.CTkOptionMenu(row0, values=["选项1", "选项2"], width=120)
                
            opt.grid(row=0, column=i*2+1, padx=5)
        
        # 查询输入区域
        query_row = ctk.CTkFrame(param_frame)
        query_row.pack(fill="x", pady=10)
        
        ctk.CTkLabel(query_row, text="查询语句:").pack(side="left", padx=5)
        ctk.CTkEntry(query_row, width=600).pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(query_row, text="查询", width=80).pack(side="left", padx=5)
        
        # 数据表格
        self.create_data_table(tab)
        
    def create_data_table(self, parent):
        # 表格容器
        table_frame = ctk.CTkFrame(parent, corner_radius=0)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 使用ttk Treeview保持表格功能
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#3498db", foreground="white", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=25)
        
        columns = ("ID", "IP", "PORT/DOMAIN", "OS", "TITLE")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
        
        # 设置列宽
        col_widths = [50, 160, 235, 90, 200]
        for col, width in zip(columns, col_widths):
            self.table.heading(col, text=col)
            self.table.column(col, width=width, anchor="center")
            
        # 添加滚动条
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=vsb.set)
        
        self.table.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
    def create_footer(self):
        footer = ctk.CTkFrame(self.main_frame, corner_radius=0, height=40)
        footer.pack(fill="x", pady=5)
        
        info_text = "Version: v1.0.0 | Author: Polylanger | E-mail: qiang.zhangcs@outlook.com | Repo: https://github.com/Polylanger/MetaCSE"
        ctk.CTkLabel(footer, 
                    text=info_text,
                    text_color="#95a5a6",
                    font=("Arial", 10)).pack(pady=5)

if __name__ == "__main__":
    app = MetaCSEApp()
    app.mainloop()