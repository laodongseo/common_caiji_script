# --*--coding: utf-8 --*--
"""
指定起始页url
单线程翻页采集直到结束
"""
import pandas as pd
import traceback
from pyquery import PyQuery as pq
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


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


def get_driver(chrome_path,chromedriver_path):
	ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
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


def login_cms(user,pwd):
	url = 'https://cms.5i5j.com/'
	driver.get(url)
	ele_user = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.ID, "username"))
	)
	ele_user.clear()
	ele_user.click()
	for i in user:
		ele_user.send_keys(i)
		time.sleep(0.02)

	ele_pwd = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.ID, "password"))
	)

	ele_pwd.clear()
	ele_pwd.click()
	for i in pwd:
		ele_pwd.send_keys(i)
		time.sleep(0.02)

	# 点击登录
	ele_login = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.ID, "btn-submit"))
	)
	ele_login.click()

	name = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.CLASS_NAME, "hidden-xs"))
	)
	if name:
		print('login success...')


# 获取源码
def get_html(url):
	global OneHandle_UseNum
	if OneHandle_UseNum > OneHandle_MaxNum:
		driver.execute_script("window.open('')")
		time.sleep(1)
		close_handle(driver)
	driver.get(url)
	OneHandle_UseNum += 1
	time.sleep(2)
	try:
		WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.ID, "example2")))
	except Exception as e:
		traceback.print_exc()
	else:
		html = driver.page_source
		return html


def parse_html(html):
	texts = []
	next_page = None
	if html and 'AdminLTE' in html:
		try:
			doc = pq(html)
			tr_list = doc('tbody tr').items()
		except Exception as e:
			print('未提取到信息', e)
		else:
			for tr in tr_list:
				hang = []
				tds = tr('td').items()
				for td in tds:
					text = td.text()
					hang.append(text)
				texts.append(hang)
		if '下一页' in html:
			page_a = doc('.pageSty a').eq(0)
			next_page = page_a.attr('href')
	return texts,next_page


def save_data(texts):
	for hang in texts:
		str_text = '\t'.join(hang)
		if str_text:
			f.write('{0}\n'.format(str_text))
		f.flush()


def run(url):
	html = get_html(url)
	texts,next_link = parse_html(html)
	save_data(texts)
	while 1:
		if next_link:
			next_link = 'https://cms.5i5j.com' + next_link
			print('next:',next_link)
			html = get_html(next_link)
			tie_links,next_link = parse_html(html)
			save_data(tie_links)
			time.sleep(2)
		else:
			break


if __name__ == '__main__':
	OneHandle_UseNum,OneHandle_MaxNum = 1,1 # 计数1个handle打开网页次数(防止浏览器崩溃)
	ChromePath = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
	ChromeDriver_path = 'D:/install/pyhon36/chromedriver.exe'
	driver = get_driver(ChromePath,ChromeDriver_path)
	login_cms(user='xxx',pwd='yyyy')
	loop_q = pd.read_excel('config.xlsx').drop_duplicates(subset=['城市']).iterrows()

	for index,row in  loop_q:
		city,cid = row['城市'],row['城市ID']
		if cid in [1, 7, 9, 19]:
			continue
		url = f'https://cms.5i5j.com/export/exportcommunityindex?cityID={cid}&qyid=0&sqid=0&type=1&housenum=1'
		print(city,cid)
		f = open(f'./{city}-二手.txt','w',encoding='utf-8')
		run(url)
		f.flush()

		url = f'https://cms.5i5j.com/export/exportcommunityindex?cityID={cid}&qyid=0&sqid=0&type=2&housenum=1'
		print(city, cid)
		f = open(f'./{city}-租房.txt', 'w', encoding='utf-8')
		run(url)
		f.close()
