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

	# 解析源码
	def parse(self, html):
		doc= pq(str(html))
		div_obj = doc('div.content')
		img_objs = div_obj('img').items()
		imgs_list = [img.attr('src') for img in img_objs]
		imgs = '#'.join(imgs_list)

		div_html = div_obj.html()
		div_html = re.sub('\n|&#13;','',div_html)
		div_html = re.sub(r'<p>	<br /></p>|<p>	<br/></p>|<p>	<br></p>|<p>	<br ></p>','',div_html)
		no_str = '<!--<div class="arcbodyad"><a href="http://www.xiuzhanwang.com/" ><img src="/style/arcad.jpg" /></a></div>-->'
		div_html = re.sub(no_str,'',div_html)
		article = re.sub('<p>','<p>　　',div_html).strip()
		return article,imgs


	def run(self):
		global IsHeader
		while 1:
			row = q.get()
			url = row['url']
			print(url)
			try:
				html = self.get_html(url)
				if not html:
					q.put(url)
					continue
				article_imgs = self.parse(html)
			except Exception as e:
				traceback.print_exc()
				q.put(row)
				time.sleep(30)
			else:
				if isinstance(article_imgs,tuple) and len(article_imgs[0]) > 0:
					article,imgs = article_imgs
					row['article'] = article
					row['图片'] = imgs
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
				time.sleep(1.5)


if __name__ == "__main__":
	start = time.time()
	user_agent = {'User-Agent': 'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)'}
	q = Spider_Content.read('www.pc-daily.com_百度PC.xlsx')
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
