import customtkinter as ctk
from tkinter import ttk

class DataTable(ctk.CTkFrame):
    """数据表格组件"""
    def __init__(self, master, columns, col_proportions, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns
        self.col_proportions = col_proportions
        
        self.tree = ttk.Treeview(
            self, 
            columns=columns, 
            show="headings",
            style="Treeview"
        )
        
        self._initialize_table()
        self._add_scrollbar()
        self.bind_events()
        
    def _initialize_table(self):
        """初始化表格列"""
        for col in self.columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, stretch=True)
        
    def _add_scrollbar(self):
        """添加滚动条"""
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def bind_events(self):
        """绑定调整事件"""
        self.tree.bind("<Configure>", self.adjust_columns)
        self.bind("<Configure>", self.adjust_columns)
    
    def adjust_columns(self, event=None):
        """动态调整列宽"""
        table_width = self.tree.winfo_width() - 20
        if table_width < 500:
            return
            
        # 按比例计算各列宽度    
        widths = [int(table_width * p) for p in self.col_proportions]
        
        # 设置列宽限制
        min_widths = [50, 100, 120, 80, 150]  # 对应各列最小宽度
        for col, width, minw in zip(self.columns, widths, min_widths):
            self.tree.column(col, width=max(width, minw))
            
    def update_data(self, data):
        """更新表格数据"""
        self.tree.delete(*self.tree.get_children())
        for idx, row in enumerate(data, 1):
            self.tree.insert("", "end", values=(str(idx), *row[1:]))
