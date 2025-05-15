import customtkinter as ctk
from ui.styles import UIStyler
from ui.components.table import DataTable
from handlers.search import SearchHandler
from ui.components.params_row import QueryParamRow
from ui.components.multiselect_dropdown import MultiSelectDropdown


class MetaCSEApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MetaCSE v1.0.0 - Polylanger")
        self.geometry("1024x768")
        self.minsize(1024, 768)
        self.styler = UIStyler()

        # 查询变量
        self.query_var = ctk.StringVar(value='title="后台" && city="beijing"')

        # 控件变量
        self.thread_var = ctk.StringVar(value="5")
        self.page_var = ctk.StringVar(value="1")
        self.mode_var = ctk.StringVar(value="主机搜索")
        self.storage_var = ctk.StringVar(value="不保存")
        self.engine_var = ctk.StringVar(value="Fofa")
        # 主界面布局
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 初始化界面组件
        self.create_tab_view()
        self.create_footer()

        self.search_handler = SearchHandler()

    def create_tab_view(self):
        """创建标签页容器"""
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.pack(fill="both", expand=True)

        # 添加标签页
        self.tab_view.add("查询")
        self.tab_view.add("配置")
        self.tab_view.add("帮助")

        self.tab_view.configure(
            segmented_button_selected_color="#3498db", segmented_button_selected_hover_color="#2980b9"
        )

        # 构建查询页
        self.build_query_tab()

    def build_query_tab(self):
        """构建查询标签页内容"""
        tab = self.tab_view.tab("查询")

        # 主参数容器
        param_container = ctk.CTkFrame(tab)
        param_container.pack(fill="x", padx=10, pady=10, anchor="nw")

        # 参数配置
        params_config = [
            ("线程数:", ["5", "1", "10", "20", "30"]),
            ("查询页数:", ["1", "2", "3", "5", "10", "15"]),
            ("模式:", ["主机搜索"]),
            ("存储模式:", ["不保存", "本地存储", "云存储"]),
            # ("搜索引擎:", ["Fofa", "ZoomEye", "Shodan"]),
        ]
        self.param_row = QueryParamRow(param_container, params_config)
        self.param_row.pack(fill="x", padx=10, pady=10)

        # 搜索引擎多选组件
        engine_frame = ctk.CTkFrame(param_container)
        engine_frame.pack(side="left", padx=10)
        ctk.CTkLabel(engine_frame, text="搜索引擎:").pack(side="left", padx=5)
        self.engine_selector = MultiSelectDropdown(
            engine_frame, options=["Fofa", "Shodan", "Hunter", "Zoomeye", "360Quake"], width=180  # 增加宽度显示更多内容
        )
        self.engine_selector.pack(side="right", padx=5)

        # 查询输入行
        query_row = ctk.CTkFrame(tab, fg_color="transparent")
        query_row.pack(fill="x", padx=10, pady=10)
        self._build_query_input(query_row)

        # 数据表格
        self.table = DataTable(
            tab, columns=("ID", "engine", "IP", "PORT/DOMAIN", "OS", "TITLE"), col_proportions=[0.08, 0.15, 0.22, 0.1, 0.15, 0.3]
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_query_input(self, master):
        """构建查询输入组件"""
        ctk.CTkLabel(master, text="查询语句：").pack(side="left")
        entry = ctk.CTkEntry(master, width=600, textvariable=self.query_var, placeholder_text="输入查询语句...")
        entry.pack(side="left", padx=5, expand=True)

        btn = ctk.CTkButton(master, text="查询", width=80, command=self.on_query_click)
        btn.pack(side="left")

    def on_query_click(self):
        """处理查询事件"""
        query_params = {
            "query": self.query_var.get(),
            "search_engine": self.engine_selector.get_selected(),
            **self.param_row.get_params(),
        }
        # 模拟搜索并更新表格
        data = self.search_handler.execute_search(query_params)
        self.table.update_data(data)

    def create_footer(self):
        """创建页脚"""
        footer = ctk.CTkFrame(self.main_frame, height=30)
        footer.pack(fill="x", pady=5)

        text = "Version: v1.0.0 | Author: Polylanger | E-mail: qiang.zhangcs@outlook.com"
        ctk.CTkLabel(footer, text=text, text_color="#666").pack(pady=3)


if __name__ == "__main__":
    app = MetaCSEApp()
    app.mainloop()
