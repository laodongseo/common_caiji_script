# --*--coding: utf-8 --*--
"""
指定起始页self.url
单线程翻页采集直到结束
采集cms后台精选问答全部id和title
采集完用save_excel.py合并
"""
import requests
import re
from pyquery import PyQuery as pq
import time
import os
from datetime import datetime


class Tieba(object):

	def __init__(self,now_id,cookie):
		self.url = f'https://cms.5i5j.com/knowledge/index/?city_id={now_id}&category1=0&category2=0&search_key=0&status=-1&status_id=-1&adminStatus=1&type=1&start_time=0&end_time=0&createruserid=-1&page='
		self.headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Encoding':'deflate',
			'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
			'Connection':'keep-alive',
			'Cookie':cookie,
			'Host':'cms.5i5j.com',
			'Referer':'https://cms.5i5j.com/knowledge/index',
			'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
			'sec-ch-ua-mobile':'?0',
			'Sec-Fetch-Dest':'document',
			'Sec-Fetch-Mode':'navigate',
			'Sec-Fetch-Site':'same-origin',
			'Sec-Fetch-User':'?1',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
		}


	def get_html(self,url,retry=1):
		try:
			r = requests.get(url=url,headers=self.headers, timeout=5)
		except Exception as e:
			print('获取源码失败', url, e)
			if retry > 0:
				time.sleep(30)
				self.get_html(url, retry - 1)
		else:
			status = r.status_code
			if status == 200:
				html = r.text
				return html
			else:
				print(status)


	def parse_html(self,html):
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



	def save_data(self,texts):
		for hang in texts:
			str_text = '\t'.join(hang)
			f.write('{0}\n'.format(str_text))
			f.flush()


	def run(self):
		data = self.get_html(self.url)
		texts,next_link = self.parse_html(data)
		self.save_data(texts)
		while 1:
			if next_link:
				next_link = 'https://cms.5i5j.com' + next_link
				print(next_link)
				data = self.get_html(next_link)
				tie_links,next_link = self.parse_html(data)
				self.save_data(tie_links)
				time.sleep(0.2)
			else:
				break

if __name__ == '__main__':
	today = time.strftime('%Y-%m-%d', time.localtime())
	if not os.path.exists(today):
		os.mkdir(today)
	cookie_str = open('cookie.txt','r',encoding='utf-8').readlines()[0].strip()
	city_id_dict = {'bj':1,'hz':2,'sz':5,'ty':6,'tj':7,'nj':8,'sh':9,'cd':15,'nj':16,'zz':18,'wx':19,'wh':20,'qd':21,'cz':25,'dg':99,'hf':51,'xa':52,'yt':53,'hhht':54,'lf':55,'ly':56,'cf':57,'suzhou':58}
	for city_id in city_id_dict.items():
		city,now_id = city_id
		f = open(f'./{today}/zhuanye-wenda_{city}.txt','w',encoding='utf-8')
		tieba = Tieba(now_id,cookie_str)
		tieba.run()
		f.flush()
		f.close()
