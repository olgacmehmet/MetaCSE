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
        self.build_config_tab()

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


    def build_config_tab(self):
        """重构后的配置页构建方法"""
        tab = self.tab_view.tab("配置")
        tab.grid_columnconfigure((0, 1), weight=1, uniform="config_cols")
        tab.grid_rowconfigure(0, weight=1)

        # 主容器使用3:2的左右比例
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # 左侧面板（账号/API配置）
        left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 右侧面板（数据库/存储配置）
        right_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 构建子组件
        self._build_auth_section(left_panel)      # 认证信息区块
        self._build_api_keys_section(left_panel)  # API密钥区块
        self._build_storage_section(right_panel)  # 存储配置区块
        self._build_db_section(right_panel)       # 数据库配置区块
        self._build_actions_section(right_panel)  # 操作按钮区块

    def _build_auth_section(self, master):
        """认证信息区块"""
        frame = self._create_section_frame(master, "账户认证")
        fields = [
            ("账号:", "account_var", ""),
            ("密码:", "password_var", "", True),
            ("邮箱:", "email_var", "qiang.zhangcs@outlook.com"),
        ]
        self._create_form_rows(frame, fields)

    def _build_api_keys_section(self, master):
        """API密钥区块"""
        frame = self._create_section_frame(master, "引擎API配置")
        engines = [
            ("Zoomeye", "zoomeye_key_var"),
            ("Fofa", "fofa_key_var"),
            ("360Quake", "quake_key_var"),
            ("Shodan", "shodan_key_var"), 
            ("Hunter", "hunter_key_var"),
        ]
        for engine, var in engines:
            self._create_form_row(frame, f"{engine} API-KEY:", var)

    def _build_storage_section(self, master):
        """存储配置区块"""
        frame = self._create_section_frame(master, "存储配置")
        
        # 文件存储
        file_frame = ctk.CTkFrame(frame, fg_color="transparent")
        file_frame.pack(fill="x", pady=3)
        self._create_form_row(file_frame, "文件路径:", "file_path_var", "results.csv")
        
        # SQLite配置
        sqlite_frame = ctk.CTkFrame(frame, fg_color="transparent")
        sqlite_frame.pack(fill="x", pady=3)
        self._create_form_row(sqlite_frame, "SQLite路径:", "sqlite_path_var", "sqlite.db")

    def _build_db_section(self, master):
        """数据库配置区块（MySQL）"""
        frame = self._create_section_frame(master, "数据库配置(MySQL)")
        fields = [
            ("主机:", "mysql_host_var", "192.168.32.121"),
            ("端口:", "mysql_port_var", "3306"),
            ("数据库名:", "mysql_db_var", "metacse"),
            ("用户名:", "mysql_user_var", "root"),
            ("密码:", "mysql_pw_var", "", True),
        ]
        self._create_form_rows(frame, fields)

    def _build_actions_section(self, master):
        """操作按钮区块"""
        frame = self._create_section_frame(master, "操作控制")
        
        # 按钮网格布局
        buttons = [
            ("保存配置", "#27ae60", self.on_save_config),
            ("读取配置", "#2980b9", self.on_load_config),
            ("清空配置", "#c0392b", self.on_clear_config),
            ("数据库测试", "#8e44ad", self.on_test_db),
            ("清除token", "#f39c12", self.on_clear_token),
        ]
        
        # 创建两列按钮布局
        grid_frame = ctk.CTkFrame(frame, fg_color="transparent")
        grid_frame.pack(fill="x", pady=5)
        
        for i, (text, color, cmd) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                grid_frame, 
                text=text,
                fg_color=color,
                hover_color=self._darken_color(color),
                corner_radius=8,
                width=120,
                command=cmd
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # 语言选择
        lang_frame = ctk.CTkFrame(frame, fg_color="transparent")
        lang_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(lang_frame, text="界面语言:").pack(side="left", padx=5)
        self.lang_combo = ctk.CTkComboBox(
            lang_frame, 
            values=["中文", "English"], 
            variable=ctk.StringVar(value="中文"),
            dropdown_hover_color="#3498db",
            button_color="#3498db",
            width=100
        )
        self.lang_combo.pack(side="right")

    def _create_section_frame(self, master, title):
        """创建带标题的分区框架"""
        frame = ctk.CTkFrame(master, corner_radius=8)
        frame.pack(fill="x", pady=8, padx=2)
        
        # 标题装饰条
        header = ctk.CTkFrame(frame, height=28, fg_color="#f8f9fa")
        header.pack(fill="x", pady=(0,5))
        ctk.CTkLabel(
            header, 
            text=title,
            text_color="#2c3e50",
            font=("Microsoft YaHei", 11, "bold")
        ).pack(side="left", padx=10)
        
        return frame

    def _create_form_rows(self, master, fields):
        """批量创建表单行"""
        for field in fields:
            self._create_form_row(master, *field)

    def _create_form_row(self, master, label, var_name, default="", is_password=False):
        """创建标准表单行"""
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        if not hasattr(self, var_name):
            setattr(self, var_name, ctk.StringVar(value=default))
        
        # 标签部分
        ctk.CTkLabel(
            row, 
            text=label,
            width=100,
            anchor="e",
            font=("Microsoft YaHei", 10)
        ).pack(side="left", padx=5)
        
        # 输入字段
        entry = ctk.CTkEntry(
            row,
            textvariable=getattr(self, var_name),
            show="•" if is_password else "",
            border_color="#ddd",
            fg_color="#ffffff",
            text_color="#333"
        )
        entry.pack(side="right", expand=True, fill="x", padx=5)

    def _darken_color(self, hex_color, factor=0.8):
        """生成深色版本的颜色"""
        rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
        darker = [int(c * factor) for c in rgb]
        return f"#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}"

    # 以下是按钮事件处理函数（需要后续实现）
    def on_save_config(self):
        """保存配置逻辑"""
        pass

    def on_load_config(self):
        """加载配置逻辑"""
        pass

    def on_clear_config(self):
        """清空配置逻辑"""
        pass

    def on_test_db(self):
        """数据库测试逻辑"""
        pass

    def on_clear_token(self):
        """清除token逻辑"""
        pass

if __name__ == "__main__":
    app = MetaCSEApp()
    app.mainloop()
