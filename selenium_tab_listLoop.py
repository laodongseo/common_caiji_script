"""
http://chromedriver.storage.googleapis.com/index.html
"""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from pyquery import PyQuery as pq
import pandas as pd
import os

headers = ['姓名','公司','链接']


def close_handle():
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


def parse(html):
	infos = []
	doc = pq(html)
	li_objs = doc('#wap_pager_data li').items()
	for li_obj in li_objs:
		a_obj = li_obj('section a')
		link = a_obj.attr('href')
		ceo_name = a_obj('h5').text().strip()
		gongsi_name = li_obj('section aside').text().strip()
		infos.append((ceo_name,gongsi_name,link))
	return infos


def save_csv(infos):
	global label_csv
	if label_csv==0:
		df_init = pd.DataFrame(columns=headers)
		df_init.to_csv(CsvFile,encoding='utf-8-sig',mode='a+',index=False)
		label_csv=1
	else:
		df_data = pd.DataFrame(data=infos,columns=headers)
		df_data.to_csv(CsvFile,encoding='utf-8-sig',mode='a+',index=False,header=False)


def main(page_max):
	global OneHandle_UseNum
	time.sleep(15)
	lis_page = list(range(1,3750+1))
	while True:
		if len(lis_page)==0:
			break
		for i in sorted(lis_page):
			if OneHandle_UseNum > OneHandle_MaxNum:
				driver.execute_script("window.open('')")
				time.sleep(1)
				close_handle()
			driver.get(f'https://www.trjcn.com/ceo/?page={i}')
			OneHandle_UseNum += 1
			print(i)
			try:
				div_obj=WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.ID, "wap_pager_data")))
				html = driver.page_source
				infos = parse(html)
				if isinstance(infos,list) and len(infos) > 0:
					save_csv(infos)
			except Exception as e:
				lis_page.append(i)
				f.write(f'{i}\n')
				f.flush()
			else:
				lis_page.remove(i)
			finally:
				time.sleep(1)


if __name__ == "__main__":
	OneHandle_UseNum,OneHandle_MaxNum = 1,1 # 计数1个handle打开网页次数(防止浏览器崩溃)
	label_csv = 0
	f = open('error.txt','w',encoding='utf-8')
	chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
	chromedriver_path=r'D:/py3script/selenium测试/chromedriver.exe'
	options = uc.ChromeOptions()
	# options.add_argument('--headless')
	driver = uc.Chrome(options=options,driver_executable_path=chromedriver_path,browser_executable_path=chrome_path)
	CsvFile = '投融界ceo.csv'
	main(1)
	f.close()
