# 文件路径: views/integrity_check_ui.py

import os
import queue
import threading
import customtkinter as ctk
from tkinter import filedialog

# 导入爬虫逻辑
from modules.scraper.async_func_dp import WEB_CONFIG
from modules.scraper.async_screenshot_dp import run_batch_screenshot_task 

class IntegrityCheckFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        
        # --- 数据初始化 ---
        self.log_queue = queue.Queue()
        self.base_output_path = ctk.StringVar(value=os.getcwd())
        self.checkboxes = {}
        
        # 专门用于存储已添加公司的后台列表
        self.companies_data = [] 

        # --- 布局配置 ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) # 日志区占满剩余空间

        # --- 绘制 UI ---
        self.setup_ui()

    def setup_ui(self):
        # 1. 路径选择区域
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.path_entry = ctk.CTkEntry(self.path_frame, textvariable=self.base_output_path, state="disabled")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.path_btn = ctk.CTkButton(self.path_frame, text="选择截图保存目录", width=150, command=self.select_folder)
        self.path_btn.pack(side="right")

        # 2. 顶栏：输入公司 + 添加按钮 + 启动按钮
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.add_comp_entry = ctk.CTkEntry(self.input_frame, placeholder_text="输入单个公司名称...")
        self.add_comp_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.add_comp_entry.bind("<Return>", self.add_company) # 绑定回车键
        
        self.add_comp_btn = ctk.CTkButton(self.input_frame, text="➕ 添加", width=80, command=self.add_company)
        self.add_comp_btn.pack(side="left", padx=(0, 20))
        
        self.run_btn = ctk.CTkButton(self.input_frame, text="▶ 开始核查", fg_color="#2FA572", hover_color="#106A43", command=self.start_task)
        self.run_btn.pack(side="right")

        # 3. 公司展示列表
        self.comp_list_frame = ctk.CTkScrollableFrame(self, label_text="待核查公司列表", height=100)
        self.comp_list_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # 4. 网页选择区域
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="选择核查范围", height=120)
        self.scroll_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        
        for i, site_name in enumerate(WEB_CONFIG.keys()):
            cb = ctk.CTkCheckBox(self.scroll_frame, text=site_name)
            cb.select()
            cb.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.checkboxes[site_name] = cb

        # 5. 日志输出
        self.log_textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.log_textbox.configure(state="disabled")

    # ==========================================
    # 下面这些就是“第 2 步”和“第 3 步”的代码位置
    # 它们和 setup_ui() 是平级的兄弟关系
    # ==========================================

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.base_output_path.set(folder)

    def add_company(self, event=None):
        """将输入框内的公司加入列表"""
        comp_name = self.add_comp_entry.get().strip()
        
        if not comp_name:
            return 
            
        if comp_name in self.companies_data:
            self.write_log(f">>> [提示] 公司 '{comp_name}' 已在列表中，无需重复添加。\n")
        else:
            self.companies_data.append(comp_name)
            self.refresh_company_list()
            
        self.add_comp_entry.delete(0, "end") 

    def remove_company(self, comp_name):
        """从列表中移除指定的公司"""
        if comp_name in self.companies_data:
            self.companies_data.remove(comp_name)
            self.refresh_company_list()

    def refresh_company_list(self):
        """清空并重新渲染公司展示列表"""
        for widget in self.comp_list_frame.winfo_children():
            widget.destroy()

        for comp in self.companies_data:
            row_frame = ctk.CTkFrame(self.comp_list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            lbl = ctk.CTkLabel(row_frame, text=comp)
            lbl.pack(side="left", padx=5)

            del_btn = ctk.CTkButton(row_frame, text="✖", width=28, height=24, 
                                    fg_color="#D9534F", hover_color="#C9302C",
                                    command=lambda c=comp: self.remove_company(c))
            del_btn.pack(side="right", padx=5)

    def start_task(self):
        """启动核查任务"""
        selected_sites = [name for name, cb in self.checkboxes.items() if cb.get() == 1]
        companies = self.companies_data 
        base_output = self.base_output_path.get()

        if not companies:
            self.write_log(">>> [错误] 请至少添加一家公司\n")
            return
        if not selected_sites:
            self.write_log(">>> [错误] 请至少选择一个核查网页\n")
            return

        self.run_btn.configure(state="disabled")
        
        thread = threading.Thread(
            target=run_batch_screenshot_task, 
            args=(companies, self.log_queue, base_output, selected_sites),
            daemon=True
        )
        thread.start()
        self.after(100, self.listen_to_queue)

    def listen_to_queue(self):
        """监听日志队列"""
        try:
            while True:
                msg = self.log_queue.get_nowait()
                if msg == "DONE":
                    self.run_btn.configure(state="normal")
                else:
                    self.write_log(msg)
        except queue.Empty:
            pass
        self.after(100, self.listen_to_queue)

    def write_log(self, text):
        """写入日志到文本框"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", text)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")