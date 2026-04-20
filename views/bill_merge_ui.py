import os
import queue
import threading
import customtkinter as ctk
from tkinter import filedialog
from modules.bill.base_infor import process_pdf, process_single_image 

class billMergeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        
        # --- 数据初始化 ---
        self.log_queue = queue.Queue()
        self.output_path = ctk.StringVar(value=os.getcwd())
        self.api_key_var = ctk.StringVar()
        
        # 存储待处理的文件列表
        self.files_data = [] 

        # --- 布局配置 ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1) # 日志区占满剩余高度

        # --- 绘制 UI ---
        self.setup_ui()

    def setup_ui(self):
        # 1. 顶部配置区：识别类型、LLM选择、API KEY
        self.config_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.config_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # 识别类型下拉
        ctk.CTkLabel(self.config_frame, text="识别类型:").pack(side="left", padx=(0, 5))
        self.type_option = ctk.CTkOptionMenu(self.config_frame, values=["PDF", "图片"], width=100, command=self.on_type_change)
        self.type_option.pack(side="left", padx=(0, 20))

        # LLM 选择下拉
        ctk.CTkLabel(self.config_frame, text="大模型:").pack(side="left", padx=(0, 5))
        self.llm_option = ctk.CTkOptionMenu(self.config_frame, values=["千问", "KIMI"], width=100)
        self.llm_option.pack(side="left", padx=(0, 20))

        # API Key 输入框 (show="*" 隐藏真实输入内容)
        ctk.CTkLabel(self.config_frame, text="API KEY:").pack(side="left", padx=(0, 5))
        self.api_entry = ctk.CTkEntry(self.config_frame, textvariable=self.api_key_var, placeholder_text="在此输入API Key...", show="*")
        self.api_entry.pack(side="left", fill="x", expand=True)

        # 2. 输出目录选择区
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.path_entry = ctk.CTkEntry(self.path_frame, textvariable=self.output_path, state="disabled")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.path_btn = ctk.CTkButton(self.path_frame, text="选择输出目录", width=150, command=self.select_output_folder)
        self.path_btn.pack(side="right")

        # 3. 输入文件添加区
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.add_file_btn = ctk.CTkButton(self.input_frame, text="➕ 添加文件", command=self.add_files)
        self.add_file_btn.pack(side="left")
        
        self.run_btn = ctk.CTkButton(self.input_frame, text="▶ 开始提取", fg_color="#2FA572", hover_color="#106A43", command=self.start_task)
        self.run_btn.pack(side="right")

        # 4. 文件展示列表
        self.file_list_frame = ctk.CTkScrollableFrame(self, label_text="待处理文件列表", height=150)
        self.file_list_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # 5. 日志输出区
        self.log_textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.log_textbox.configure(state="disabled")

    # ==========================================
    # 交互与逻辑方法
    # ==========================================

    def on_type_change(self, choice):
        """当用户切换 'PDF/图片' 时触发，清空当前列表以防类型冲突"""
        if self.files_data:
            self.files_data.clear()
            self.refresh_file_list()
            self.write_log(f">>> [系统] 已切换至 {choice} 模式，清空原文件列表。\n")

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="选择识别结果保存目录")
        if folder:
            self.output_path.set(folder)

    def add_files(self):
        """打开文件选择对话框，根据当前选择的类型过滤文件后缀"""
        current_type = self.type_option.get()
        
        if current_type == "PDF":
            filetypes = [("PDF 文件", "*.pdf")]
        else:
            filetypes = [("图片文件", "*.png *.jpg *.jpeg *.bmp")]

        # 支持多选文件
        file_paths = filedialog.askopenfilenames(title=f"选择{current_type}文件", filetypes=filetypes)
        
        if not file_paths:
            return

        added_count = 0
        for path in file_paths:
            if path not in self.files_data:
                self.files_data.append(path)
                added_count += 1
            else:
                self.write_log(f">>> [提示] 文件已存在，跳过: {os.path.basename(path)}\n")
        
        if added_count > 0:
            self.refresh_file_list()

    def remove_file(self, file_path):
        """从列表中移除指定文件"""
        if file_path in self.files_data:
            self.files_data.remove(file_path)
            self.refresh_file_list()

    def refresh_file_list(self):
        """清空并重新渲染文件列表"""
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        for path in self.files_data:
            row_frame = ctk.CTkFrame(self.file_list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            # 只显示文件名，路径太长影响美观
            file_name = os.path.basename(path)
            lbl = ctk.CTkLabel(row_frame, text=file_name)
            lbl.pack(side="left", padx=5)

            del_btn = ctk.CTkButton(row_frame, text="✖", width=28, height=24, 
                                    fg_color="#D9534F", hover_color="#C9302C",
                                    command=lambda p=path: self.remove_file(p))
            del_btn.pack(side="right", padx=5)

    def start_task(self):
        """启动核查任务"""
        api_key = self.api_key_var.get().strip()
        out_dir = self.output_path.get()
        file_type = self.type_option.get()
        llm_type = self.llm_option.get()

        # --- 执行前校验 ---
        if not api_key:
            self.write_log(">>> [错误] 请输入 API KEY。\n")
            return
        if not self.files_data:
            self.write_log(">>> [错误] 请至少添加一个待处理文件。\n")
            return
        if not os.path.exists(out_dir):
            self.write_log(">>> [错误] 输出目录不存在。\n")
            return

        self.run_btn.configure(state="disabled")
        self.add_file_btn.configure(state="disabled")
        
        # 将当前的配置拷贝出来，传给线程
        task_files = list(self.files_data)

        # 启动后台线程
        thread = threading.Thread(
            target=self.run_extraction_background, 
            args=(task_files, file_type, llm_type, api_key, out_dir),
            daemon=True
        )
        thread.start()
        self.after(100, self.listen_to_queue)

    def run_extraction_background(self, files, file_type, llm_type, api_key, out_dir):
        """在后台线程中循环处理文件"""
        self.log_queue.put(f"=== 开始执行提取任务 (模式: {file_type}, 模型: {llm_type}) ===\n")
        
        try:
            for idx, file_path in enumerate(files, 1):
                file_name = os.path.basename(file_path)
                self.log_queue.put(f"[{idx}/{len(files)}] 正在处理: {file_name}...\n")
                
                # 定义一个给核心代码调用的日志回调函数
                def log_cb(msg):
                    self.log_queue.put(f"    -> {msg}\n")

                if file_type == "PDF":
                    process_pdf(file_path, out_dir, llm_type, api_key, log_cb)
                else:
                    process_single_image(file_path, out_dir, llm_type, api_key, log_cb)
                
                import time
                time.sleep(1) # 模拟处理耗时，接入真实代码后请删除此行
                self.log_queue.put(f"[{idx}/{len(files)}] {file_name} 处理完成。\n\n")
                
        except Exception as e:
            self.log_queue.put(f"[严重错误] 任务异常中断: {str(e)}\n")
        
        self.log_queue.put("DONE")

    def listen_to_queue(self):
        """监听日志队列"""
        try:
            while True:
                msg = self.log_queue.get_nowait()
                if msg == "DONE":
                    self.run_btn.configure(state="normal")
                    self.add_file_btn.configure(state="normal")
                    self.write_log("=== 全部任务执行完毕 ===\n")
                else:
                    self.write_log(msg)
        except queue.Empty:
            pass
        
        # 如果按钮还是禁用状态，说明任务还在跑，继续监听
        if self.run_btn.cget("state") == "disabled":
            self.after(100, self.listen_to_queue)

    def write_log(self, text):
        """写入日志到文本框"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", text)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")