# ‐*‐ coding: utf‐8 ‐*‐
"""
从小区ID的txt文件读取问题列表
https://nc.5i5j.com/xq-question/102400248140/
每个问题列表页翻页采集完
"""

import requests
from pyquery import PyQuery as pq
import threading
import queue
import time
import gc
import re
import random
from urllib.parse import urlparse
import traceback


class Spider_Content(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	@staticmethod
	def read(filepath):
		q = queue.Queue()
		for i in open(filepath, 'r', encoding='utf-8'):
			i = i.strip().split('\t')[0]
			q.put(i)
		return q

	# 获取源码
	def get_html(self, url, retry=2):
		try:
			r = requests.get(url=url, headers=user_agent, timeout=5)
		except Exception as e:
			print('获取源码失败', url, e)
			time.sleep(30)
			if retry > 0:
				self.get_html(url, retry - 1)
		else:
			html = r.text
			return html

	# 获取问题列表+下一页地址
	def parse(self, html,whole_domain):
		contents = []
		next_page = ''
		if html:
			doc= pq(str(html))
			title = doc('h1').text().replace('?','').replace('？','').replace('/','')
			a_list = doc('.wd-item .questlist-title a:last').items()
			for a in a_list:
				text,link = a.text(),a.attr('href')
				link = f'{whole_domain}{link}'
				contents.append((text,link))
			if '下一页' in html:
				page_a = doc('a.cPage')
				next_page = page_a.attr('href')
				next_page = f'{whole_domain}{next_page}'
		return contents,next_page


	#带协议的域名
	def get_domain(self,url):
		whole_domain = 'xxx'
		res=urlparse(url)
		try:
			domain = res.netloc
			whole_domain = f'https://{domain}'
		except Exception as e:
			print('domain:',e)
		return whole_domain


	def save(self,xq_id,url,contents):
		for hang in contents:
			hang_str = '\t'.join(hang)
			f.write(f'{xq_id}\t{url}\t{hang_str}\n')
			f.flush()


	# 统计每个域名排名的词数
	def run(self):
		while 1:
			xq_id = q.get()
			url = f'https://bj.5i5j.com/xq-question/{xq_id}/'
			print(url)
			whole_domain = self.get_domain(url)
			try:
				html = self.get_html(url)
				contents,next_page = self.parse(html,whole_domain)
				self.save(xq_id,url,contents)
				while True:
					if next_page:
						html = self.get_html(next_page)
						contents,next_page = self.parse(html,whole_domain)
						self.save(xq_id,url,contents)
						time.sleep(2)
					else:
						break
			except Exception as e:
				traceback.print_exc()
			finally:
				q.task_done()
				gc.collect()
				time.sleep(1)


if __name__ == "__main__":
	start = time.time()
	save_path = './'
	user_agent = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
	q = Spider_Content.read('xq_id.txt')
	f = open('xq_question.txt','w',encoding='utf-8')
	# 设置线程数
	for i in list(range(1)):
		t = Spider_Content()
		t.setDaemon(True)
		t.start()
	q.join()
	end = time.time()
	f.close()



