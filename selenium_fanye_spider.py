# ‐*‐ coding: utf‐8 ‐*‐
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import traceback
import re
import os
from pyquery import PyQuery as pq
import threading

s1 = r""" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile" """



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


def read_excel(filepath):
		q = queue.Queue()
		df = pd.read_excel(filepath).dropna()
		for index,row in df.iterrows():
			q.put(row)
		return q


def parse_html(html,now_url):
	next_page = ''
	rows_all = []
	doc= pq(str(html))
	title = doc('title').text()
	if '口红' in title:
		tr_lefts = doc('div.items div.J_MouserOnverReq div.pic a').items() 
		next_page_obj = doc('li.next a.J_Ajax')
		next_page = next_page_obj.text()
		for td_obj in tr_lefts:
			text = td_obj('img').attr('alt')
			link = td_obj.attr('href')
			link = f'https://{link}'
			rows_all.append((text,link))
	return rows_all,next_page



def save(datas,url_str):
	df = row.to_frame().T
	with lock:
		if IsHeader == 0:
			df.to_csv(CsvResFile,encoding='utf-8-sig',mode='w+',index=False)
			IsHeader = 1
		else:
			df.to_csv(CsvResFile,encoding='utf-8-sig',mode='a+',index=False,header=False)
	f.flush()


def main():
	page_num = 1
	global driver,OneHandle_UseNum
	driver.get(IndexUrl)
	content_left = WebDriverWait(driver, 20).until(
			EC.visibility_of_element_located((By.CLASS_NAME, "total"))
	)
	html, now_url = driver.page_source, driver.current_url
	rows_all,next_page = parse_html(html,now_url)
	print('首页处理完毕:',next_page)
	save(rows_all,now_url)

	while True:
		if  not next_page:
			break
		page_num+=1
		# 点击翻页
		if OneHandle_UseNum > OneHandle_MaxNum:
			driver.execute_script("window.open('')")
			time.sleep(1)
			close_handle(driver)
		driver.execute_script(next_page_click_js)
		OneHandle_UseNum += 1
		time.sleep(3)
		print('点击页码',page_num)

		# 判断翻页是否加载完
		try:
			while 1:
				element = WebDriverWait(driver, 900).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[@class="item active"]/span')))
				print(element.text)
				if str(page_num) in element.text:
					break
				else:
					break
		except Exception as e:
			traceback.print_exc()
			f.write(driver.page_source)
			return
		print('当前页码',element.text)

		driver.execute_script(js_xiala)
		time.sleep(15)
		html, now_url = driver.page_source, driver.current_url
		rows_all,next_page = parse_html(html,now_url)
		print(f'当前页文本:{next_page}')
		save(rows_all,now_url)



if __name__ == "__main__":
	OneHandle_UseNum,OneHandle_MaxNum = 1,1 # 计数1个handle打开网页次数(防止浏览器崩溃)
	ChromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
	ChromeDriver_path = 'D:/install/pyhon36/chromedriver.exe'
	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
	lock = threading.Lock()
	q = read_excel('kwd-vrrw.net.xlsx')
	CsvResFile = 'kwd-vrrw.net_serpurl.csv'
	# 首页url
	IndexUrl = '' 
	next_page_click_js = 'document.querySelector("#mainsrp-pager > div > div > div > ul > li.item.next > a").click()'
	js_xiala = 'window.scrollBy(0,document.body.scrollHeight)'
	driver = get_driver(chrome_path,chromedriver_path,ua)
	f = open('res.txt','w',encoding='utf-8')
	main()
