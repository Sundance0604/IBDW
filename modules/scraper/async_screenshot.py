import time
import os
import pyautogui
from urllib.parse import quote
import undetected_chromedriver as uc
from modules.scraper.async_func import WEB_CONFIG
import pyautogui
import sys


'''使用内窥镜方式截图'''
def screenshot_selenium(driver, company_folder, filename):
    save_path = os.path.join(company_folder, f"{filename}.png")
    driver.save_screenshot(save_path) 
   
'''使用pyautogui方式截图（全屏）'''
def screenshot_pyautogui(company_folder, filename):
    save_path = os.path.join(company_folder, f"{filename}.png")
    # 换回 pyautogui，进行纯物理屏幕截图（带任务栏）
    pyautogui.screenshot(save_path)  
def get_real_base_path():
    """
    获取程序运行时的真实根目录，完美兼容 Python 源码运行和 PyInstaller 打包后的 EXE 运行。
    """
    if getattr(sys, 'frozen', False):
        # 1. EXE 运行模式：
        # 当被打包成 exe 后，sys.frozen 会变成 True。
        # 此时 sys.executable 会指向 IBDW.exe 的绝对路径（如 D:\IBDW\dist\IBDW\IBDW.exe）
        # 我们用 os.path.dirname 取它的父目录，就是真正的项目根目录（dist\IBDW）
        return os.path.dirname(sys.executable)
    else:
        # 2. 源码运行模式：
        # 当前脚本所在位置是: IBDW/modules/scraper/async_screenshot.py
        # 我们需要向上“扒”三层目录才能回到 IBDW 根目录
        current_file_path = os.path.abspath(__file__)     # .../IBDW/modules/scraper/async_screenshot.py
        scraper_dir = os.path.dirname(current_file_path)  # .../IBDW/modules/scraper
        modules_dir = os.path.dirname(scraper_dir)        # .../IBDW/modules
        root_dir = os.path.dirname(modules_dir)           # .../IBDW (最终的根目录)
        
        return root_dir

APP_ROOT_DIR = get_real_base_path()

def get_clean_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument('--disable-popup-blocking')
    options.page_load_strategy = 'none'
    
    # 【核心：精准拼接出 chromedriver.exe 的绝对路径】
    driver_path = os.path.join(APP_ROOT_DIR, "modules", "scraper", "chromedriver.exe")
    
    # 传入路径
    driver = uc.Chrome(options=options, driver_executable_path=driver_path)
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
