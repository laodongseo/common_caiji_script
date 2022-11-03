# coding:utf8
"""
检查泛解析域名是否访问通
domains.txt放域名(不需要http)
"""

import requests   
from threading import Thread
from threading import Lock
import queue
import re,traceback
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


headers = {
'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
}


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
	option.add_argument('headless')
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
		div_obj=WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.TAG_NAME, "title")))
	except Exception as e:
		traceback.print_exc()
	else:
		html = driver.page_source
		return html


def  run():
	driver = get_driver(ChromePath,ChromeDriver_path,UA)
	while True:
		if q.qsize() > 0:
			url = q.get()
			for url in [f'http://{url}/',f'http://xxx.{url}/']:
				print(url)
				html = get_html(driver,url)
				o_title = re.search('<title>(.*?)</title>',str(html),re.S|re.I)
				title = o_title.group(1) if o_title else '无标题'
				print(f'\t{title}')
				f.write(f'{url}\t{title}\n')
				f.flush()
				time.sleep(2)
		else:
			break
				




if __name__ == "__main__":
	OneHandle_UseNum,OneHandle_MaxNum = 1,1 # 计数1个handle打开网页次数(防止浏览器崩溃)
	ChromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
	ChromeDriver_path = 'D:/install/pyhon36/chromedriver.exe'
	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
	q = queue.Queue()
	f = open('title.txt','w',encoding='utf-8')
	for line in open('domains.txt','r',encoding='utf-8'):
		line = line.strip()
		q.put(line)
	run()
