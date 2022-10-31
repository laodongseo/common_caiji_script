# ‐*‐ coding: utf‐8 ‐*‐
"""

采集 https://bj.5i5j.com/question/992193.html
他们的回答经纪人
"""

import requests
from pyquery import PyQuery as pq
import threading
import queue
import time
import gc
import re,os
import random
from urllib.parse import urlparse
import traceback,json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



# 设置允许弹窗
js_allow_pop = """
document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-privacy-page").shadowRoot.querySelector("#pages > settings-subpage.iron-selected > settings-category-default-radio-group").shadowRoot.querySelector("#enabledRadioOption").shadowRoot.querySelector("#button > div.disc").click()
""".strip()
url_pop = 'chrome://settings/content/popups'


def set_driver(driver):
	try:
		# 防止反爬
		driver.get('http://www.python66.com/stealth.min.js')
		time.sleep(0.5)
		js_hidden = driver.page_source
		driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
		  "source": js_hidden
		})

		# 设置允许弹窗(headless模式执行失败)
		# driver.get(url_pop)
		# time.sleep(0.5)
		# driver.execute_script(js_allow_pop)
	except Exception as e:
		traceback.print_exc()
	finally:
		return driver



def close_handle(driver):
	if len(driver.window_handles) > 1:
		for handle in driver.window_handles[0:-1]:
			driver.switch_to.window(handle)
			time.sleep(1)
			driver.close()
		# 检测关闭结束
		while True:
			if len(driver.window_handles) == 1:
				break
		# 切到唯一窗口
		driver.switch_to.window(driver.window_handles[0])


def get_driver(chrome_path,chromedriver_path,ua):
	ua = ua
	option = Options()
	option.binary_location = chrome_path
	# option.add_argument('disable-infobars')
	option.add_argument("user-agent=" + ua)
	option.add_argument("--no-sandbox")
	option.add_argument("--disable-dev-shm-usage")
	option.add_argument("--disable-gpu")
	option.add_argument("--disable-features=NetworkService")
	option.add_argument("window-size=1000,1080")
	option.add_argument("--disable-features=VizDisplayCompositor")
	# option.add_argument('headless')
	option.add_argument('log-level=3') #屏蔽日志
	option.add_argument('--ignore-certificate-errors-spki-list') #屏蔽ssl error
	option.add_argument('-ignore -ssl-errors') #屏蔽ssl error
	option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
	option.add_experimental_option('useAutomationExtension', False)
	No_Image_loading = {"profile.managed_default_content_settings.images": 1}
	option.add_experimental_option("prefs", No_Image_loading)
	option.add_argument("--disable-blink-features")
	option.add_argument("--disable-blink-features=AutomationControlled")
	driver = webdriver.Chrome(options=option,executable_path=chromedriver_path)
	driver = set_driver(driver)
	return driver


def read(filepath):
	q = queue.Queue()
	for i in open(filepath, 'r', encoding='utf-8'):
		i = i.strip()
		q.put(i)
	return q



# 获取源码
def get_html(driver,url):
	global OneHandle_UseNum
	if OneHandle_UseNum > OneHandle_MaxNum:
		driver.execute_script("window.open('')")
		time.sleep(1)
		close_handle(driver)
	driver.get(url)
	OneHandle_UseNum += 1
	try:
		div_obj=WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "wd-details-box")))
	except Exception as e:
		traceback.print_exc()
	else:
		html = driver.page_source
		return html


# 获取问题列表+下一页地址
def parse( html,whole_domain):
	contents = []
	next_page = ''
	if html:
		doc= pq(str(html))
		div_list = doc('.que-list-box .que-list-item .quePeo-infos').items()
		for div in div_list:
			a = div('.quePeo-head a')
			json_str = a.attr('giojson')
			jingjiren_id = json.loads(json_str)['agentid_var']
			jingjiren_name = div('.quePeo-name .quePeo-top strong').text().strip()
			contents.append((jingjiren_id,jingjiren_name))
		if '下一页' in html:
			page_a = doc('a.cPage')
			next_page = page_a.attr('href')
			next_page = f'{whole_domain}{next_page}'
	return contents,next_page


#带协议的域名
def get_domain(url):
	whole_domain = 'xxx'
	res=urlparse(url)
	try:
		domain = res.netloc
		whole_domain = f'https://{domain}'
	except Exception as e:
		print('domain:',e)
	return whole_domain


def save(row,contents):
	for hang in contents:
		hang_str = '\t'.join(hang)
		f.write(f'{row}\t{hang_str}\n')
		f.flush()


# 统计每个域名排名的词数
def run():
	global IsHeader
	driver = get_driver(ChromePath,ChromeDriver_path,UA)
	while 1:
		row = q.get()
		url = row.split('\t')[-1]
		print(url)
		print(row)
		whole_domain = get_domain(url)
		try:
			html = get_html(driver,url)
			contents,next_page = parse(html,whole_domain)
			save(row,contents)
			while True:
				if next_page:
					html = get_html(driver,next_page)
					contents,next_page = parse(html,whole_domain)
					save(row,contents)
					time.sleep(2)
				else:
					break
		except Exception as e:
			traceback.print_exc(file=open('error.txt','a+'))
		finally:
			q.task_done()
			gc.collect()
			time.sleep(1)


if __name__ == "__main__":
	start = time.time()
	OneHandle_UseNum,OneHandle_MaxNum = 1,1 # 计数1个handle打开网页次数(防止浏览器崩溃)
	ChromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
	ChromeDriver_path = 'D:/install/pyhon36/chromedriver.exe'
	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'

	save_path = './'
	q = read('xq_question.txt')
	f = open('xq_question_answer.txt','w',encoding='utf-8')
	# 设置线程数
	for i in list(range(1)):
		t = threading.Thread(target=run,)
		t.setDaemon(True)
		t.start()
	q.join()
	end = time.time()
	f.close()



