from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
def switch_to_new_window_if_any(driver, old_handles_count):
    """如果点击搜索后弹出了新标签页，切过去"""
    try:
        WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > old_handles_count)
        driver.switch_to.window(driver.window_handles[-1])
    except:
        pass

# ==========================================
# 纯粹的页面内交互动作 (不再包含 driver.get)
# ==========================================

def action_caizhengbu(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="andsen"]')))
    search_input.send_keys(company)
    search_btn = driver.find_element(By.XPATH, '//a[@onclick="javascript:checkInput();"]')
    old_count = len(driver.window_handles)
    search_btn.click()
    switch_to_new_window_if_any(driver, old_count)

def action_haiguanzongshu(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "keyWords")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'view') and contains(@onclick, 'query')]")))
    old_count = len(driver.window_handles)
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)

def action_shangwuxinyong(driver, company):
    # 根据你原代码，这里只填字不点击
    input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "e_input-31")))
    input_box.clear()
    input_box.send_keys(company)

def action_ziranziyuanbu(driver, company):
    """自然资源部：触发搜索并跳转新标签页"""
    # 1. 定位并等待输入框就绪 (根据 id="searchText" 定位)
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "searchText")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'onSearch')]"))
    )
    old_count = len(driver.window_handles)
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)

'''应急管理：阶段一（点火）'''
def action_yingjiguanli(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "iptSword")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "query_btn")))
    old_count = len(driver.window_handles)
    search_button.click()
    switch_to_new_window_if_any(driver, old_count)
    # 不在这里填字了，切完窗口直接撤退！
def action_jiaotongbu(driver, company):
    """交通运输部搜索交互"""
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "qt")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button")))
    old_count = len(driver.window_handles)
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)
'''深交所-纪律处分'''
def action_shenjiaosuo_jlcf(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ZQ_JLCF_tab1_txtGjz")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-query-primary"))
    )
    old_count = len(driver.window_handles)
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)
'''深交所-监管措施'''
def action_shenjiaosuo_jgcs(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ZQ_JGCS_tab1_txtGjz")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-query-primary"))
    )
    old_count = len(driver.window_handles)
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)
'''全国建筑市场监管公共服务平台'''
def action_jianzushichang(driver, company):
    search_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '诚信记录主体')]/ancestor::div[contains(@class, 'el-col')]//input"))
    )
    search_input.clear()
    search_input.send_keys(company)
    old_count = len(driver.window_handles)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ssButton') and text()='查询']"))
    )
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)
'''应急管理：阶段三（截图前收尾）'''
def post_action_yingjiguanli(driver, company):
    # 此时页面已经彻底加载完毕，填进去的字绝对不会被覆盖
    search_input_new = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "sw")))
    search_input_new.clear()
    search_input_new.send_keys(company)
"""中国盐业协会：仅在搜索框输入文本，不执行点击"""
def post_action_zhongguoyanye(driver, company):
    # 定位并等待输入框就绪 (根据 name="q" 定位)
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
    # 清空输入框并填入公司名称
    search_input.clear()
    search_input.send_keys(company)

def action_zhengjianhui_normal(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "searchWord")))
    search_input.clear()
    search_input.send_keys(company)
    old_count = len(driver.window_handles)
    search_input.submit()
    switch_to_new_window_if_any(driver, old_count)

def action_zhengjianhui_govern(driver, company):
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "content")))
    search_input.clear()
    search_input.send_keys(company)
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "search-icon")))
    old_count = len(driver.window_handles)
    try:
        search_button.click()
    except:
        driver.execute_script("arguments[0].click();", search_button)
    switch_to_new_window_if_any(driver, old_count)

def action_chaozai(driver, company):
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "select_publicityType")))
    dropdown = Select(select_element)
    dropdown.select_by_visible_text("行政处罚")

def action_shangjiaosuo(driver, company, log_callback):
 # 1. 强行把这个标签页拽回物理屏幕的最前方！
    # 很多 Vue/React 组件在后台是“冻结”状态，不响应任何事件
    driver.switch_to.window(driver.current_window_handle)
    time.sleep(1) # 缓冲一下，让页面从休眠中醒来
    
    log_callback(f"    -> [上交所] 开始寻找页签...")
    tab_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-switch0 span.credibility"))
    )
    
    # 强制滚动到视图中央
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_button)
    time.sleep(1)
    
    log_callback(f"    -> [上交所] 执行多重破甲点击...")
    
    # 【攻击策略 A】：尝试点击它的“爸爸”（父级元素）
    try:
        parent_element = tab_button.find_element(By.XPATH, "..")
        parent_element.click()
        log_callback(f"    -> [上交所] 父级原生点击成功！")
    except:
        # 【攻击策略 B】：尝试对自身进行原生点击
        try:
            tab_button.click()
            log_callback(f"    -> [上交所] 自身原生点击成功！")
        except:
            # 【攻击策略 C】：终极必杀技！用 JS 伪造一个 100% 真实的物理鼠标事件（带冒泡机制）
            log_callback(f"    -> [上交所] 动用 JS 模拟真实鼠标点击...")
            driver.execute_script("""
                var evObj = new MouseEvent('click', {
                    bubbles: true, 
                    cancelable: true, 
                    view: window
                });
                arguments[0].dispatchEvent(evObj);
            """, tab_button)
    
    # 死等 5 秒，等待那个局部表格数据慢慢刷出来
    log_callback(f"    -> [上交所] 操作完毕，死等 5 秒数据...")
    time.sleep(5)
    
        

# 对于一步到位的网站，action 填 None 即可
WEB_CONFIG = {
    # === 国家部委及总局 ===
    '发改委-一般检索': {'url': 'https://so.ndrc.gov.cn/s?siteCode=bm04000007&ssl=1&token=&qt={company}', 'action': None, 'post_action': None},
    '财政部': {'url': 'http://www.mof.gov.cn/index.htm', 'action': action_caizhengbu, 'post_action': None},
    '工信部-一般检索': {'url': 'https://www.miit.gov.cn/search/index.html?websiteid=110000000000000&pg=&p=&tpl=&category=&jsflIndexSeleted=&q={company}', 'action': None, 'post_action': None},
    '能源局': {'url': 'https://www.nea.gov.cn/search.htm?kw={company}', 'action': None, 'post_action': None},
    '国家市场监管总局': {'url': 'https://www.samr.gov.cn/api-gateway/jpaas-jsearch-web-server/search?serviceId=db6d646f22e541d7a303940a8e8623cc&websiteid=&cateid=aef29dab559a4e9db9da54ff2e1eb92b&q={company}&sortType=2', 'action': None, 'post_action': None},
    '国家统计局': {'url': 'https://www.stats.gov.cn/search/s?qt={company}', 'action': None, 'post_action': None},
    '药监局-一般检索': {'url': 'https://www.nmpa.gov.cn/so/s?tab=all&qt={company}', 'action': None, 'post_action': None},
    '海关总署': {'url': 'http://search.customs.gov.cn/eportal/ui?pageId=7690f322e6a0410881e172afbfaaa25c', 'action': action_haiguanzongshu, 'post_action': None},
    '农业农村部-一般检索': {'url': 'https://www.moa.gov.cn/so/s?qt={company}', 'action': None, 'post_action': None},
    '商务部': {'url': 'https://search.mofcom.gov.cn/allSearch/?siteId=0&keyWordType=title&acSuggest={company}', 'action': None, 'post_action': None},
    '商务信用平台': {'url': 'https://www.315gov.cn/globalSearch.html?keywords={company}&appIds=all', 'action': action_shangwuxinyong, 'post_action': None},
    '生态环境部-一般检索': {'url': 'https://www.mee.gov.cn/searchnew/?searchword={company}', 'action': None, 'post_action': None},
    '应急管理': {'url': 'https://www.mem.gov.cn/', 'action': action_yingjiguanli, 'post_action': post_action_yingjiguanli},
    '住建部-一般检索': {'url': 'https://www.mohurd.gov.cn/api-gateway/jpaas-jsearch-web-server/search?serviceId=e2f3058e2a3b4f8abc93eb76e739e3e7&websiteid=&cateid=6ca0f12c0f0642ab8b1dc17028e12ea1&q={company}', 'action': None, 'post_action': None},
    '国家外汇管理局': {'url':'https://www.safe.gov.cn/safe/search/index.html?q={company}&siteid=safe&order=releasetime', 'action': None, 'post_action': None},
    '中国人民银行-一般检索':{'url':'https://wzdig.pbc.gov.cn/search/pcRender?sr=score+desc&pageId=c177a85bd02b4114bebebd210809f691&ext=&pNo=1&q={company}', 'action': None, 'post_action': None},
    '中国盐业协会':{'url':'https://www.cnsalt.cn/index/index/search.html?q={company}', 'action': None, 'post_action': post_action_zhongguoyanye},
    '中国电力企业联合会':{'url':'https://cec.org.cn/search/index.html?search={company}', 'action': None, 'post_action': None},
    #'中国政府采购':{'url':"https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw={company}&start_time=2025%3A10%3A20&end_time=2026%3A04%3A20&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName=", 'action': None, 'post_action': None},
    '交通运输部': {'url': 'https://www.mot.gov.cn/', 'action': action_jiaotongbu, 'post_action': None},
    '人力资源和社会保障部':{'url':'https://www.mohrss.gov.cn/hsearch/?searchword={company}', 'action': None, 'post_action': None },
    '安全生产领域失信生产经营单位': {'url': 'https://www.mem.gov.cn/', 'action': action_yingjiguanli, 'post_action': post_action_yingjiguanli},
    '自然资源部-一般检索':{'url':'https://www.mnr.gov.cn/','action': action_ziranziyuanbu, 'post_action': None},
    '自然资源部-高级检索':{'url':'https://www.mnr.gov.cn/','action': action_ziranziyuanbu, 'post_action': None},
    '全国建筑市场监管公共服务平台': {'url': 'https://jzsc.mohurd.gov.cn/since/index', 'action': action_jianzushichang, 'post_action': None},
    # === 证券交易及监管核查 ===
    '证监会-一般检索': {'url': 'http://www.csrc.gov.cn/', 'action': action_zhengjianhui_normal, 'post_action': None},
    '证监会-政府公开信息': {'url': 'http://www.csrc.gov.cn/csrc/c100033/zfxxgk_zdgk.shtml', 'action': action_zhengjianhui_govern, 'post_action': None},
    '发行人行贿核查': {'url': 'https://www.baidu.com/s?wd={company}%20行贿核查&rsv_btype=t&inputT=2224&rsv_t=b47e6furN%2Buws5yK33qvVaMI50O7yxzu2SUStbjtkTStWDxuTokDQSCATjFvvjLKMIr2&rsv_pq=910a7b9f00002f8f&rsv_sug3=15&rsv_sug1=10&rsv_sug7=100&rsv_sug4=2224', 'action': None, 'post_action': None},
    '深交所-纪律处分':{'url':'http://www.szse.cn/disclosure/bond/punish/index.html','action': action_shenjiaosuo_jlcf, 'post_action': None},
    '深交所-监管措施':{'url':'http://www.szse.cn/disclosure/bond/measure/index.html','action': action_shenjiaosuo_jgcs, 'post_action': None},
    # === 地方政府及其他专项 ===
    '地方政府处罚': {'url': 'https://www.hebei.gov.cn/s?q={company}&fix=1', 'action': None, 'post_action': None},
    '信用交通': {'url': 'http://219.143.235.38:8080/CreditTraffic/jsp/pc/integrationAll.jsp?flag=1&searchValue={company}', 'action': action_chaozai, 'post_action': None},
    
    # === 百度舆情检索 ===
    '百度_违约': {'url': 'https://www.baidu.com/s?wd={company}%20违约&rsv_btype=t&inputT=2224&rsv_t=b47e6furN%2Buws5yK33qvVaMI50O7yxzu2SUStbjtkTStWDxuTokDQSCATjFvvjLKMIr2&rsv_pq=910a7b9f00002f8f&rsv_sug3=15&rsv_sug1=10&rsv_sug7=100&rsv_sug4=2224', 'action': None, 'post_action': None},
    '百度_负面': {'url': 'https://www.baidu.com/s?wd={company}%20负面&rsv_btype=t&inputT=2224&rsv_t=b47e6furN%2Buws5yK33qvVaMI50O7yxzu2SUStbjtkTStWDxuTokDQSCATjFvvjLKMIr2&rsv_pq=910a7b9f00002f8f&rsv_sug3=15&rsv_sug1=10&rsv_sug7=100&rsv_sug4=2224', 'action': None, 'post_action': None},
}
   