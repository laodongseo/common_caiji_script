# ‐*‐ coding: utf‐8 ‐*‐
"""
从excel的url列里采集每篇内容
"""

import requests
from pyquery import PyQuery as pq
import threading
import queue
import time
import gc
import re,chardet
import random,traceback
from urllib.parse import urlparse
import pandas as pd


class Spider_Content(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	@staticmethod
	def read(filepath):
		q = queue.Queue()
		for index,row in pd.read_excel(filepath).iterrows():
			q.put(row)
		return q

	# 获取源码
	def get_html(self, url, retry=1):
		try:
			r = requests.get(url=url, headers=user_agent, timeout=15)
		except Exception as e:
			print('获取源码失败', url, e)
			time.sleep(30)
			if retry > 0:
				self.get_html(url, retry - 1)
		else:
			data = r.content
			code = chardet.detect(data)['encoding']
			html = data.decode(code,errors='ignore')
			return html

	def parse(self, html):
		doc= pq(str(html))
		p_list = doc('.info-zi p').items()
		texts = []
		for p in p_list:
			text = p.text().strip()
			texts.append(text) if text else True
		article = ''.join([f'<p>　　{text}</p>' for text in texts])
		return article


	def run(self):
		global IsHeader
		while 1:
			row = q.get()
			url = row['url']
			print(url)
			try:
				html = self.get_html(url)
				article = self.parse(html)
			except Exception as e:
				traceback.print_exc()
			else:
				if isinstance(article,str) and len(article) > 0:
					row['article'] = article
					df = row.to_frame().T
					with lock:
						if IsHeader == 0:
							df.to_csv(TodayCsvFile,encoding='utf-8-sig',mode='w+',index=False)
							IsHeader = 1
						else:
							df.to_csv(TodayCsvFile,encoding='utf-8-sig',mode='a+',index=False,header=False)
			finally:
				q.task_done()
				gc.collect()
				time.sleep(2)


if __name__ == "__main__":
	start = time.time()
	user_agent = {'User-Agent': 'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)'}
	q = Spider_Content.read('txt合并.xlsx')
	TodayCsvFile = f'res_new.csv'
	lock = threading.Lock()
	IsHeader = 0

	# 设置线程数
	for i in list(range(1)):
		t = Spider_Content()
		t.setDaemon(True)
		t.start()
	q.join()

	end = time.time()
	print((end - start))

