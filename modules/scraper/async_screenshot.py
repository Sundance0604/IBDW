import time
import os
import pyautogui
from urllib.parse import quote
import undetected_chromedriver as uc
from modules.scraper.async_func import WEB_CONFIG
import pyautogui

# 获取当前正在运行的 .py 文件的绝对路径并切换工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

'''使用内窥镜方式截图'''
def screenshot_selenium(driver, company_folder, filename):
    save_path = os.path.join(company_folder, f"{filename}.png")
    driver.save_screenshot(save_path) 
   
'''使用pyautogui方式截图（全屏）'''
def screenshot_pyautogui(company_folder, filename):
    save_path = os.path.join(company_folder, f"{filename}.png")
    # 换回 pyautogui，进行纯物理屏幕截图（带任务栏）
    pyautogui.screenshot(save_path)  
   

def get_clean_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument('--disable-popup-blocking')
    options.page_load_strategy = 'none'
    driver = uc.Chrome(options=options, driver_executable_path=r"chromedriver.exe")
    return driver

def run_batch_screenshot_task(companies, log_queue, base_output, selected_sites):
    driver = get_clean_driver()
    try:
        for company in companies:
            log_queue.put(f"\n[任务] 开始处理: {company}\n")
            company_folder = os.path.join(base_output, company)
            os.makedirs(company_folder, exist_ok=True)
            # 只处理用户勾选的站点
            active_config = {k: v for k, v in WEB_CONFIG.items() if k in selected_sites}
            company_folder = os.path.join(base_output, company)
            os.makedirs(company_folder, exist_ok=True)

            safe_company = quote(company)
            main_handle = driver.current_window_handle
            
            # 两个任务池
            initial_pool = {}  # 存放等待首页加载的句柄 {handle: filename}
            result_pool = {}   # 存放等待结果页加载的句柄 {handle: filename}

            # ==========================================
            # 阶段一：瞬间在后台并发打开所有主 URL (无阻塞改良版)
            # ==========================================
            for filename, config in active_config.items():
                target_url = config['url'].format(company=safe_company)
                
                # 1. 打开一个绝对不会阻塞的空白页
                driver.execute_script("window.open('about:blank');")
                
                # 2. 切过去，因为是空白页，瞬间就能切成功
                driver.switch_to.window(driver.window_handles[-1])
                current_handle = driver.current_window_handle
                
                # 3. 记录句柄
                initial_pool[current_handle] = filename
                
                # 4. 用 JS 赋予当前页面新网址。
                # 由于我们设置了 page_load_strategy = 'none'，这行代码发出去瞬间就会执行下一轮循环！
                driver.execute_script(f"window.location.href = '{target_url}';")
                
            # 全部分发完毕后，切回主窗口
            driver.switch_to.window(main_handle)

            # ==========================================
            # 阶段二：谁的首页最先加载完，就切过去“点火”
            # ==========================================
            while initial_pool:
                for handle in list(initial_pool.keys()): # 用 list 包裹方便在循环中删除元素
                    try:
                        driver.switch_to.window(handle)
                        # 检查底层 DOM 是否加载完毕
                        if driver.execute_script("return document.readyState;") == "complete":
                            filename = initial_pool.pop(handle)
                            action_func = active_config[filename]['action']
                            
                            if action_func:
                        
                                action_func(driver, company) # 执行输入和点击
                                # 动作结束后，无论有没有开新窗口，都把“当前所在窗口”扔进最终截图池
                                current_active_handle = driver.current_window_handle
                                result_pool[current_active_handle] = filename
                            else:
                                # 如果不需要动作（比如药监局），直接把它扔进截图池
                                result_pool[handle] = filename
                    except Exception as e:
                        initial_pool.pop(handle, None) # 出错就丢弃
                time.sleep(0.3)

            # ==========================================
            # 阶段三：所有动作已触发，谁的结果页加载完截谁
            # ==========================================
            while result_pool:
                for handle in list(result_pool.keys()):
                    try:
                        driver.switch_to.window(handle)
                        if driver.execute_script("return document.readyState;") == "complete":
                            filename = result_pool.pop(handle)
                            
                            # 【核心新增：截图前置动作拦截】
                            post_action_func = active_config[filename].get('post_action')
                            if post_action_func:
                                post_action_func(driver, company)
                            # 给动态数据(如 Ajax 列表)一点渲染时间
                            time.sleep(1) 
                            # 选取何种截图方式
                            screenshot_pyautogui(company_folder, filename)
                            driver.close() # 截完立即释放内存
                    except Exception as e:
                        result_pool.pop(handle, None)
                time.sleep(0.3)
                
            # 跑完一个公司，切回最初的那个主窗口
            driver.switch_to.window(main_handle)

    except Exception as e:
        log_queue.put(f">>> [错误] {company} 处理失败: {str(e)}\n")
    finally:
        driver.quit()
        log_queue
