# 文件路径: main.py

import customtkinter as ctk
import threading
import requests
import webbrowser
from tkinter import messagebox

# 导入你拆分出去的各个功能 UI
from views.integrity_check_ui import IntegrityCheckFrame
from views.bill_merge_ui import billMergeFrame

# ===== 版本与更新配置 =====
# ===== 版本与更新配置 =====
CURRENT_VERSION = "v1.0.1"  
UPDATE_JSON_URL = "https://raw.githubusercontent.com/sundance0604/ibdw/main/update.json"

class IBDWApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 在标题中显示当前版本号
        self.title(f"IBDW (IB Dirty Work) - 投行执行自动化工具 {CURRENT_VERSION}")
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

        # 4. 后台异步检测更新，防止主界面卡顿
        self.check_for_updates()

    # ==========================================
    # 更新检测核心逻辑
    # ==========================================
    def check_for_updates(self):
        """开启后台线程进行网络请求，避免阻塞主 UI 线程"""
        threading.Thread(target=self._fetch_update_info, daemon=True).start()

    def _fetch_update_info(self):
        """实际的网络请求逻辑"""
        try:
            # 设置 timeout 防止网络问题导致线程长期挂起
            response = requests.get(UPDATE_JSON_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("version")
                download_url = data.get("url")
                update_notes = data.get("notes", "有新版本可用，建议更新以获取最新功能。")

                # 如果发现远端版本号与当前版本号不一致
                if latest_version and latest_version != CURRENT_VERSION:
                    # 使用 after 方法切回主线程进行 UI 弹窗，Tkinter 规定不能在子线程中直接操作 UI
                    self.after(1000, self.prompt_update, latest_version, download_url, update_notes)
        except Exception as e:
            # 静默处理网络异常，不打扰用户正常使用
            print(f"检测更新失败 (请检查网络或更新地址): {e}")

    def prompt_update(self, latest_version, download_url, update_notes):
        """弹出更新提示框"""
        msg = f"检测到新版本: {latest_version}\n当前版本: {CURRENT_VERSION}\n\n更新日志:\n{update_notes}\n\n是否立即前往下载最新版本？"
        # 弹窗询问用户
        if messagebox.askyesno("发现新版本", msg):
            webbrowser.open(download_url) # 自动通过系统默认浏览器打开下载链接

    # ==========================================
    # 原有的 UI 与路由逻辑
    # ==========================================
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
        # 先隐藏所有的页面
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