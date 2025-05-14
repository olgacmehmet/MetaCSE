import customtkinter as ctk


class QueryParamRow(ctk.CTkFrame):
    """查询参数行组件"""

    def __init__(self, master, params_config, **kwargs):
        super().__init__(master, **kwargs)
        self.params_config = params_config
        self.vars = {}
        self._build_row()

    def _build_row(self):
        """构建参数行"""
        param_objects = []
        for label_text, options in self.params_config:
            label = ctk.CTkLabel(self, text=label_text)
            var = ctk.StringVar(value=options[0])
            menu = ctk.CTkOptionMenu(self, values=options, variable=var)
            self.vars[label_text[:-1]] = var  # 移除标签末尾冒号
            param_objects.extend([label, menu])

        # 动态网格布局
        for col, widget in enumerate(param_objects):
            widget.grid(row=0, column=col, padx=5, pady=3)

    def get_params(self):
        """获取当前参数"""
        return {name: var.get() for name, var in self.vars.items()}
