import customtkinter as ctk


class MultiSelectDropdown(ctk.CTkFrame):
    """修复后的多选下拉组件"""

    def __init__(self, master, options, **kwargs):
        super().__init__(master, **kwargs)
        self.options = options
        self.selected = []
        self._menu_visible = False  # 菜单显示状态跟踪

        # 主显示区域
        self.label = ctk.CTkLabel(self, text="未选择引擎")
        self.label.pack(side="left", padx=5, fill="x", expand=True)

        # 下拉按钮
        self.button = ctk.CTkButton(self, text="▼", width=30, command=self.toggle_menu)
        self.button.pack(side="right")

        # 弹出菜单容器（使用Toplevel实现可靠覆盖）
        self.menu_window = None

    def toggle_menu(self):
        """切换菜单显示状态"""
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()
            self.menu_window = None
            self._menu_visible = False
        else:
            self._show_menu()

    def _show_menu(self):
        """显示多选菜单"""
        # 创建悬浮窗口
        self.menu_window = ctk.CTkToplevel(self)
        self.menu_window.overrideredirect(True)  # 隐藏标题栏
        self.menu_window.wm_attributes("-topmost", True)

        # 计算显示位置
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()

        # 设置菜单尺寸
        menu_width = max(self.winfo_width(), 200)
        menu_height = min(len(self.options) * 30 + 10, 300)

        # 定位菜单
        self.menu_window.geometry(f"{menu_width}x{menu_height}+{x}+{y}")

        # 添加可滚动区域
        scroll_frame = ctk.CTkScrollableFrame(self.menu_window)
        scroll_frame.pack(fill="both", expand=True)

        # 添加复选框
        self.vars = {}
        for opt in self.options:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(
                scroll_frame, text=opt, variable=var, command=lambda v=var, o=opt: self._update_selection(v, o)
            )
            cb.pack(fill="x", padx=5, pady=2)
            self.vars[opt] = var

        # 绑定外部点击关闭事件
        self.menu_window.bind("<FocusOut>", lambda e: self._close_menu())
        self._menu_visible = True

    def _update_selection(self, var, option):
        """更新选中状态"""
        if var.get():
            if option not in self.selected:
                self.selected.append(option)
        else:
            if option in self.selected:
                self.selected.remove(option)
        self.label.configure(text="已选: " + ", ".join(self.selected) if self.selected else "未选择引擎")

    def _close_menu(self):
        """安全关闭菜单"""
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()
            self.menu_window = None
            self._menu_visible = False

    def get_selected(self):
        """获取选中项"""
        return self.selected.copy()

    def destroy(self):
        """重写销毁方法"""
        self._close_menu()
        super().destroy()
