from urllib.parse import quote
import time
from DrissionPage.common import Keys
# ==========================================
# 纯粹的页面内交互动作 (DrissionPage 版)
# ==========================================
import time

'''深交所-监管措施 (包含纪律处分逻辑也一样)'''
def action_shenjiaosuo_jgcs(page, company):

    time.sleep(1) 
    inp = page.ele('#ZQ_JGCS_tab1_txtGjz')
    inp.input(company, clear=True)
    time.sleep(0.5) 
    try:
        page.ele('css:button.btn-query-primary').click(by_js=True)
    except:
        inp.input('\n')
'''深交所-监管措施 (包含纪律处分逻辑也一样)'''
def action_shenjiaosuo_jlcf(page, company):

    time.sleep(1) 
    inp = page.ele('#ZQ_JLCF_tab1_txtGjz')
    inp.input(company, clear=True)
    time.sleep(0.5) 
    try:
        page.ele('css:button.btn-query-primary').click(by_js=True)
    except:
        inp.input('\n')

'''自然资源部-一般/高级检索'''
def action_ziranziyuanbu(page, company):
    search_input = page.ele('#searchText')
    search_input.clear()
    search_input.input(company) 
    time.sleep(0.5)
    search_input.run_js(f'this.value = "{company}";')
    search_button = page.ele('xpath://a[contains(@onclick, "onSearch")]')
    search_button.click(by_js=True)

'''全国建筑市场监管公共服务平台 (Element-UI 框架)'''
def action_jianzushichang(page, company):
    input_xpath = "xpath://span[contains(text(), '诚信记录主体')]/ancestor::div[contains(@class, 'el-col')]//input"
    search_input = page.ele(input_xpath)
    search_input.clear()
    search_input.input(company) 
    search_input.run_js(f'this.value = "{company}";')
    search_input.run_js("this.dispatchEvent(new Event('input', { bubbles: true }));")
    search_input.run_js("this.dispatchEvent(new Event('change', { bubbles: true }));")
    time.sleep(2)
    search_input.input(Keys.ENTER)
'''盐行业信用管理'''
def action_yanhangyexinyong(page, company):
    page.ele('#indexKeyWord').input(company, clear=True)
def action_caizhengbu(page, company):
    page.ele('@id=andsen').input(company, clear=True)
    page.ele('@onclick:checkInput()').click(by_js=True)

def action_haiguanzongshu(page, company):
    page.ele('#keyWords').input(company, clear=True)
    page.ele('xpath://div[contains(@class, "view") and contains(@onclick, "query")]').click(by_js=True)

def action_shangwuxinyong(page, company):
    page.ele('@name=e_input-31').input(company, clear=True)
'''应急管理：阶段一（点火）'''
def action_yingjiguanli(page, company):
    page.ele('#iptSword').input(company, clear=True)
    page.ele('#query_btn').click(by_js=True)

def action_jiaotongbu(page, company):
    """交通运输部搜索交互"""
    page.ele('#qt').input(company, clear=True)
    page.ele('#button').click(by_js=True)
'''应急管理：阶段三（截图前收尾）'''
def post_action_yingjiguanli(page, company):
    page.ele('#sw').input(company, clear=True)

"""中国盐业协会：仅在搜索框输入文本，不执行点击"""
def post_action_zhongguoyanye(page, company):
    page.ele('@name=q').input(company, clear=True)
'''上交所-纪律处分/监管措施'''
def action_shangjiaosuo(page):
    tab_xpath = "xpath://span[contains(@class, 'credibility') and text()='监管']"
    target_tab = page.ele(tab_xpath)
    target_tab.click(by_js=True)  
'''生态环境部-高级检索'''
def action_shengtaihuanjingbu_gaoji(page, company):
    tab_xpath = "xpath://span[contains(@class, 'p_gaoji') and text()='高级检索']"
    target_tab = page.ele(tab_xpath)
    target_tab.click(by_js=True)
    time.sleep(1) 
    search_input = page.ele('#total') 
    search_input.clear()
    search_input.input(company)
    search_input.run_js(f'this.value = "{company}";')
    time.sleep(1)
    adv_search_btn = page.ele('#advSearch')
    adv_search_btn.click(by_js=True)
'''证监会-一般检索'''
def action_zhengjianhui_normal(page, company):
    input_box = page.ele('#searchWord')
    input_box.input(company, clear=True)
    input_box.input('\n') # 模拟回车提交
'''证监会-高级检索'''
def action_zhengjianhui_gaoji(page, company):
    input_box = page.ele('#searchWord')
    input_box.input(company, clear=True)
    input_box.input('\n') # 模拟回车提交
    page.wait.new_tab(timeout=5) 
    new_page = page.latest_tab
    search_btn_1 = new_page.ele('#highSearch')
    search_btn_1.click(by_js=True)
    search_btn_2 = new_page.ele('#advanceSearch')
    search_btn_2.click(by_js=True)
'''工信部-高级检索'''
def action_gongxinbu_gaoji(page, company):
    adv_xpath = "xpath://span[@class='ui-search-btn-adv' and text()='高级检索']"
    adv_span = page.ele(adv_xpath)
    adv_span.click(by_js=True)
    time.sleep(1)
    input_pq_xpath = "xpath://input[@id='pq']"
    search_input = page.ele(input_pq_xpath)
    search_input.clear()
    search_input.input(company)
    search_input.run_js(f'this.value = "{company}";')
    time.sleep(1)
    search_btn_xpath = "xpath://input[@id='ipt_btn']"
    search_btn = page.ele(search_btn_xpath)
    search_btn.click(by_js=True)
'''中国人民银行-高级检索'''
def action_renminyinhang_gaoji(page, company):
    time.sleep(1)
    input_qAll = "xpath://input[@name='qAll']"
    search_input = page.ele(input_qAll)
    search_input.clear()
    search_input.input(company)
    search_input.run_js(f'this.value = "{company}";')
    time.sleep(1)
    search_btn = page.ele('#button')
    search_btn.click(by_js=True)
    page.wait.new_tab(timeout=5) 
    new_page = page.latest_tab
    new_page_search_input = new_page.ele('#q')
    new_page_search_input.clear()
    new_page_search_input.input(company)
    new_page_search_input.run_js(f'this.value = "{company}";')
'''住建部-高级检索'''
def action_zhujianshu_gaoji(page, company):
    search_btn_1 = page.ele('#senior')
    search_btn_1.click(by_js=True)
    time.sleep(1)
    search_input = page.ele('#gq')
    search_input.clear()
    search_input.input(company)
    search_input.run_js(f'this.value = "{company}";')
    time.sleep(1)
    search_btn_xpath = "xpath://button[contains(text(), '开始检索')]"
    search_btn_2 = page.ele(search_btn_xpath)
    search_btn_2.click(by_js=True)
'''农业农村部-高级检索'''
def action_nongyenongcun_gaoji(page, company):
    search_btn_1 = page.ele('#toolbar_adv')
    search_btn_1.click(by_js=True)
    time.sleep(1)
    input_xpath_1 = "xpath://input[@placeholder='请输入包含任意关键词']"
    search_input_1 = page.ele(input_xpath_1)
    search_input_1.clear()
    search_input_1.input(company)
    time.sleep(1)
    search_btn_2_xpath = "xpath://div[contains(@class, 'search-btn') and contains(text(), '开始搜索')]"
    search_btn_2 = page.ele(search_btn_2_xpath)
    search_btn_2.click(by_js=True)
    time.sleep(1)
    input_xpath_2 = 'xpath://input[@placeholder="请输入搜索词"]'
    search_input_2 = page.ele(input_xpath_2)
    search_input_2.clear()
    search_input_2.input(company)

def action_zhengjianhui_govern(page, company):
    page.ele('#content').input(company, clear=True)
    page.ele('.search-icon').click(by_js=True)

def action_chaozai(page, company):
    page.ele('#select_publicityType').select('行政处罚')



# 对于一步到位的网站，action 填 None 即可
WEB_CONFIG = {
    # === 国家部委及总局 ===
    '发改委-一般检索': {'url': 'https://so.ndrc.gov.cn/s?siteCode=bm04000007&ssl=1&token=&qt={company}', 'action': None, 'post_action': None},
    '财政部': {'url': 'http://www.mof.gov.cn/index.htm', 'action': action_caizhengbu, 'post_action': None},
    '工信部-一般检索': {'url': 'https://www.miit.gov.cn/search/index.html?websiteid=110000000000000&pg=&p=&tpl=&category=&jsflIndexSeleted=&q={company}', 'action': None, 'post_action': None},
    '工信部-高级检索': {'url': 'https://www.miit.gov.cn/search/index.html?websiteid=110000000000000&pg=&p=&tpl=&category=&jsflIndexSeleted=&q={company}', 'action': action_gongxinbu_gaoji, 'post_action': None},
    '能源局': {'url': 'https://www.nea.gov.cn/search.htm?kw={company}', 'action': None, 'post_action': None},
    '国家市场监管总局': {'url': 'https://www.samr.gov.cn/api-gateway/jpaas-jsearch-web-server/search?serviceId=db6d646f22e541d7a303940a8e8623cc&websiteid=&cateid=aef29dab559a4e9db9da54ff2e1eb92b&q={company}&sortType=2', 'action': None, 'post_action': None},
    '国家统计局': {'url': 'https://www.stats.gov.cn/search/s?qt={company}', 'action': None, 'post_action': None},
    '药监局-一般检索': {'url': 'https://www.nmpa.gov.cn/so/s?tab=all&qt={company}', 'action': None, 'post_action': None},
    '海关总署': {'url': 'http://search.customs.gov.cn/eportal/ui?pageId=7690f322e6a0410881e172afbfaaa25c', 'action': action_haiguanzongshu, 'post_action': None},
    '农业农村部-一般检索': {'url': 'https://www.moa.gov.cn/so/s?qt={company}', 'action': None, 'post_action': None},
    '农业农村部-高级检索': {'url': 'https://www.moa.gov.cn/so/s?qt={company}', 'action': action_nongyenongcun_gaoji, 'post_action': None},
    '商务部': {'url': 'https://search.mofcom.gov.cn/allSearch/?siteId=0&keyWordType=title&acSuggest={company}', 'action': None, 'post_action': None},
    '商务信用平台': {'url': 'https://www.315gov.cn/globalSearch.html?keywords={company}&appIds=all', 'action': action_shangwuxinyong, 'post_action': None},
    '生态环境部-一般检索': {'url': 'https://www.mee.gov.cn/searchnew/?searchword={company}', 'action': None, 'post_action': None},
    '生态环境部-高级检索': {'url': 'https://www.mee.gov.cn/searchnew/?searchword={company}', 'action': action_shengtaihuanjingbu_gaoji, 'post_action': None},
    '应急管理': {'url': 'https://www.mem.gov.cn/', 'action': action_yingjiguanli, 'post_action': post_action_yingjiguanli},
    '住建部-一般检索': {'url': 'https://www.mohurd.gov.cn/api-gateway/jpaas-jsearch-web-server/search?serviceId=e2f3058e2a3b4f8abc93eb76e739e3e7&websiteid=&cateid=6ca0f12c0f0642ab8b1dc17028e12ea1&q={company}', 'action': None, 'post_action': None},
    '国家外汇管理局': {'url':'https://www.safe.gov.cn/safe/search/index.html?q={company}&siteid=safe&order=releasetime', 'action': None, 'post_action': None},
    '中国人民银行-一般检索':{'url':'https://wzdig.pbc.gov.cn/search/pcRender?sr=score+desc&pageId=c177a85bd02b4114bebebd210809f691&ext=&pNo=1&q={company}', 'action': None, 'post_action': None},
    '中国人民银行-高级检索':{'url':'https://wzdig.pbc.gov.cn/search/pcRender?pageId=ba91211b4019456db06f6678d71f5047', 'action': action_renminyinhang_gaoji, 'post_action': None},
    '中国盐业协会':{'url':'https://www.cnsalt.cn/index/index/search.html?q={company}', 'action': None, 'post_action': post_action_zhongguoyanye},
    '中国电力企业联合会':{'url':'https://cec.org.cn/search/index.html?search={company}', 'action': None, 'post_action': None},
    '交通运输部': {'url': 'https://www.mot.gov.cn/', 'action': action_jiaotongbu, 'post_action': None},
    '人力资源和社会保障部':{'url':'https://www.mohrss.gov.cn/hsearch/?searchword={company}', 'action': None, 'post_action': None },
    '安全生产领域失信生产经营单位': {'url': 'https://www.mem.gov.cn/', 'action': action_yingjiguanli, 'post_action': post_action_yingjiguanli},
    '自然资源部-一般检索':{'url':'https://www.mnr.gov.cn/','action': action_ziranziyuanbu, 'post_action': None},
    '自然资源部-高级检索':{'url':'https://www.mnr.gov.cn/','action': action_ziranziyuanbu, 'post_action': None},
    '全国建筑市场监管公共服务平台': {'url': 'https://jzsc.mohurd.gov.cn/since/index', 'action': action_jianzushichang, 'post_action': None},
    '盐行业信用管理':{'url':'http://yan.bcpcn.com/website/xyjl.jsp?keyword={company}&searchtype=1&page=1', 'action': action_yanhangyexinyong, 'post_action': None},
    '中国政府采购网':{'url':'https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&start_time=&end_time=&timeType=2&searchparam=&searchchannel=0&dbselect=bidx&kw=快手&bidSort=0&pinMu=0&bidType=0&buyerName=&projectId=&displayZone=&zoneId=&agentName=', 'action': None, 'post_action': None},
    '发改委-高级检索':{'url':'https://so.ndrc.gov.cn/s?qt="{company}"&siteCode=bm04000007&tab=all&keyPlace=0&sort=&days=0&fileType=&timeOption=0&adv=1', 'action': None, 'post_action': None},
    # === 证券交易及监管核查 ===
    '证监会-一般检索': {'url': 'http://www.csrc.gov.cn/', 'action': action_zhengjianhui_normal, 'post_action': None},
    '证监会-高级检索': {'url': 'http://www.csrc.gov.cn/', 'action': action_zhengjianhui_gaoji, 'post_action': None},
    '证监会-政府公开信息': {'url': 'http://www.csrc.gov.cn/csrc/c100033/zfxxgk_zdgk.shtml', 'action': action_zhengjianhui_govern, 'post_action': None},
    '发行人行贿核查': {'url': 'https://www.baidu.com/s?wd={company}%20行贿核查&rsv_btype=t&inputT=2224&rsv_t=b47e6furN%2Buws5yK33qvVaMI50O7yxzu2SUStbjtkTStWDxuTokDQSCATjFvvjLKMIr2&rsv_pq=910a7b9f00002f8f&rsv_sug3=15&rsv_sug1=10&rsv_sug7=100&rsv_sug4=2224', 'action': None, 'post_action': None},
    '深交所-纪律处分':{'url':'http://www.szse.cn/disclosure/bond/punish/index.html','action': action_shenjiaosuo_jlcf, 'post_action': None},
    '深交所-监管措施':{'url':'http://www.szse.cn/disclosure/bond/measure/index.html','action': action_shenjiaosuo_jgcs, 'post_action': None},
    '上交所-纪律处分':{'url':'https://www.sse.com.cn/home/search/index.shtml?webswd={company}', 'action': action_shangjiaosuo, 'post_action': None},
    '上交所-监管措施':{'url':'https://www.sse.com.cn/home/search/index.shtml?webswd={company}', 'action': action_shangjiaosuo, 'post_action': None},
    # === 地方政府及其他专项 ===
    '地方政府处罚': {'url': 'https://www.hebei.gov.cn/s?q={company}&fix=1', 'action': None, 'post_action': None},
    '信用交通': {'url': 'http://219.143.235.38:8080/CreditTraffic/jsp/pc/integrationAll.jsp?flag=1&searchValue={company}', 'action': action_chaozai, 'post_action': None},
    
    # === 百度舆情检索 ===
    '百度_违约': {'url': 'https://www.baidu.com/s?wd={company}%20违约&rsv_btype=t&inputT=2224&rsv_t=b47e6furN%2Buws5yK33qvVaMI50O7yxzu2SUStbjtkTStWDxuTokDQSCATjFvvjLKMIr2&rsv_pq=910a7b9f00002f8f&rsv_sug3=15&rsv_sug1=10&rsv_sug7=100&rsv_sug4=2224', 'action': None, 'post_action': None},
    '百度_负面': {'url': 'https://www.baidu.com/s?wd={company}%20负面&rsv_btype=t&inputT=2224&rsv_t=b47e6furN%2Buws5yK33qvVaMI50O7yxzu2SUStbjtkTStWDxuTokDQSCATjFvvjLKMIr2&rsv_pq=910a7b9f00002f8f&rsv_sug3=15&rsv_sug1=10&rsv_sug7=100&rsv_sug4=2224', 'action': None, 'post_action': None},
}