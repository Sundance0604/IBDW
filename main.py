# 文件路径: main.py

import customtkinter as ctk

# 导入你拆分出去的各个功能 UI
from views.integrity_check_ui import IntegrityCheckFrame
from views.bill_merge_ui import billMergeFrame
class IBDWApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IBDW (IB Dirty Work) - 投行执行自动化工具")
        self.geometry("1000x800")
        
        # 主窗口分为两列：左侧导航(列0)，右侧内容(列1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. 初始化侧边导航栏
        self.setup_navigation()

        # 2. 实例化各个子功能页面（将它们实例化，但不马上显示）
        self.integrity_frame = IntegrityCheckFrame(self)
        self.bill_merge_frame = billMergeFrame(self)
        
        # 3. 默认显示“诚信核查”页面
        self.show_frame("integrity")

    def setup_navigation(self):
        """左侧导航栏布局"""
        self.nav_frame = ctk.CTkFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(4, weight=1) # 让下方留白

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="IBDW 工具箱", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 导航按钮
        self.nav_btn_1 = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10, 
                                       text="▶ 诚信核查自动截图",
                                       command=lambda: self.show_frame("integrity"))
        self.nav_btn_1.grid(row=1, column=0, sticky="ew")
        
        # 预留未来的功能按钮
        self.nav_btn_2 = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10, 
                                       text="▶ 发票与回单合并",
                                       command=lambda: self.show_frame("bill_merge"))
        self.nav_btn_2.grid(row=2, column=0, sticky="ew")

    def show_frame(self, name):
        """核心路由逻辑：负责切换右侧显示的页面"""
        # 先隐藏所有的页面（如果有多个功能，在这里全写上 forget）
        self.integrity_frame.grid_forget()
        self.bill_merge_frame.grid_forget()

        # 根据传入的名字，把对应的页面 grid 出来
        if name == "integrity":
            self.integrity_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "bill_merge":
            self.bill_merge_frame.grid(row=0, column=1, sticky="nsew")

if __name__ == "__main__":
    app = IBDWApp()
    app.mainloop()