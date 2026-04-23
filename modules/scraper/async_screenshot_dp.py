import time
import os
import pyautogui
from urllib.parse import quote
from DrissionPage import ChromiumPage, ChromiumOptions

# 引入 dp 版配置
from modules.scraper.async_func_dp import WEB_CONFIG

# 获取当前正在运行的 .py 文件的绝对路径并切换工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

def screenshot_pyautogui(company_folder, filename):
    save_path = os.path.join(company_folder, f"{filename}.png")
    # 纯物理屏幕截图（带任务栏）
    pyautogui.screenshot(save_path)  

def get_clean_page():
    """初始化 DrissionPage 浏览器对象"""
    co = ChromiumOptions()
    co.set_argument('--start-maximized')
    # 确保使用 ChromiumPage
    page = ChromiumPage(co)
    return page
def run_batch_screenshot_task(companies, log_queue, base_output, selected_sites, CONFIG):
    page = get_clean_page()
    try:
        for company in companies:
            log_queue.put(f"\n[任务] 开始处理: {company}\n")
            company_folder = os.path.join(base_output, company)
            os.makedirs(company_folder, exist_ok=True)
            
            active_config = {k: v for k, v in CONFIG.items() if k in selected_sites}
            safe_company = quote(company)
            
            main_tab_id = page.latest_tab.tab_id
            
            # 池子结构升级：增加 start_time 记录，用于超时判定
            # 格式: {tab_id: {"filename": filename, "start_time": float}}
            initial_pool = {}  
            result_pool = {}   

            # ==========================================
            # 阶段一：纯后台瞬间并发发包
            # ==========================================
            for filename, config in active_config.items():
                target_url = config['url'].format(company=safe_company)
                tab = page.new_tab('about:blank')
                initial_pool[tab.tab_id] = {"filename": filename, "start_time": time.time()}
                tab.run_js(f"setTimeout(() => {{ window.location.href = '{target_url}'; }}, 10);")

            # ==========================================
            # 阶段二：交互 & 新标签页智能捕获
            # ==========================================
            while initial_pool:
                for t_id in list(initial_pool.keys()): 
                    pool_data = initial_pool[t_id]
                    filename = pool_data["filename"]
                    elapsed = time.time() - pool_data["start_time"]
                    
                    try:
                        tab = page.get_tab(t_id)
                        is_complete = tab.run_js("return document.readyState;") == "complete"
                        
                        # 【核心升级】如果过了 25 秒还没 complete，不再死等，强行开始交互！
                        if is_complete or elapsed > 25:
                            if not is_complete:
                                log_queue.put(f"  -> [提示] {filename} 加载超时(25s)，强行尝试交互...\n")
                                
                            initial_pool.pop(t_id)
                            action_func = active_config[filename]['action']
                            
                            if action_func:
                                old_tabs = page.tab_ids
                                action_func(tab, company) 
                                
                                # 【核心升级】动态等新窗口，最多等 3 秒（每0.2秒轮询一次）
                                new_tab_id = None
                                for _ in range(15):
                                    time.sleep(0.2)
                                    current_tabs = page.tab_ids
                                    new_tabs = [t for t in current_tabs if t not in old_tabs]
                                    if new_tabs:
                                        new_tab_id = new_tabs[-1]
                                        break
                                
                                if new_tab_id:
                                    result_pool[new_tab_id] = {"filename": filename, "start_time": time.time()}
                                else:
                                    result_pool[t_id] = {"filename": filename, "start_time": time.time()}
                            else:
                                result_pool[t_id] = {"filename": filename, "start_time": time.time()}
                    except Exception as e:
                        # 【核心升级】使用 repr(e) 捕获“空白错误”的真实面目
                        log_queue.put(f"  -> [警告] {filename} 阶段二(交互)异常: {repr(e)}\n")
                        initial_pool.pop(t_id, None)
                time.sleep(0.3)

            # ==========================================
            # 阶段三：强制显示并截图
            # ==========================================
            while result_pool:
                for t_id in list(result_pool.keys()):
                    pool_data = result_pool[t_id]
                    filename = pool_data["filename"]
                    elapsed = time.time() - pool_data["start_time"]
                    
                    try:
                        tab = page.get_tab(t_id)
                        is_complete = tab.run_js("return document.readyState;") == "complete"
                        
                        # 同样，结果页最多等 15 秒渲染
                        if is_complete or elapsed > 15:
                            result_pool.pop(t_id)
                            
                            tab.run_cdp('Page.bringToFront')
                            
                            post_action_func = active_config[filename].get('post_action')
                            if post_action_func:
                                post_action_func(tab, company)
                                
                            time.sleep(0.5) # 留出一点缓冲避免动画没播完
                            
                            screenshot_pyautogui(company_folder, filename)
                            
                            try:
                                tab.close()
                            except:
                                pass # 关不掉就算了
                    except Exception as e:
                        log_queue.put(f"  -> [警告] {filename} 阶段三(截图)异常: {repr(e)}\n")
                        result_pool.pop(t_id, None)
                time.sleep(0.3)
                
            try:
                page.get_tab(main_tab_id).run_cdp('Page.bringToFront')
            except:
                pass

    except Exception as e:
        log_queue.put(f">>> [错误] {company} 处理全局失败: {repr(e)}\n")
    finally:
        page.quit()
        log_queue.put("DONE")