"""
多类列表,指定起始结尾翻页采集,保存为不同文件
配置文件是excel
http://www.loupan.com/ask/72-p{0}/  2   100    房屋类型
"""

#‐*‐coding:utf‐8‐*‐
import requests,chardet
import threading
import queue
from pyquery import PyQuery as pq
import random,os,shutil
import time,traceback
import pandas as pd


# 获取源码
def get_html(url,retry=1):
	try:
		ua = random.choice(UA_LIST)
		headers = {'User-Agent':ua}
		r = requests.get(url=url,headers=headers,timeout=30)
	except Exception as e:
		print('获取源码失败',e)
		time.sleep(6)
		if retry > 0:
			get_html(url,retry-1)
	else:
		data = r.content
		code = chardet.detect(data)['encoding']
		html = data.decode(code,errors='ignore')
		return html


# 源码分析
def parse(html):
	title_links = []
	doc = pq(html)
	a_list = doc('div.list ul li h2 a').items()
	for a in a_list:
		title = a.text()
		link = a.attr('href')
		title_links.append((title,link))

	if title_links:
		return title_links
	else:
		print('源码异常,可能反爬')
		time.sleep(30)


# 线程函数
def main():
	while 1:
		url = q.get()
		print('url',url)
		try:
			html = get_html(url)
			title_links = parse(html)
		except Exception as e:
			traceback.print_exc()
		else:
			if isinstance(title_links,list):
				for title,link in title_links:
					f.write(f'{title}\t{link}\n')
			f.flush()
		finally:
			q.task_done()
			time.sleep(1)


if __name__ == "__main__":
	# UA设置
	UA_LIST = [
	# 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
	# 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	# 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	# 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	# 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)'
		]
	SaveLocation = 'url文件'
	shutil.rmtree(SaveLocation) if os.path.exists(SaveLocation) else True
	os.mkdir(SaveLocation) if not os.path.exists(SaveLocation) else True

	for index,row in pd.read_excel('config.xlsx').iterrows():
		url,start,end,name_type = row['url'],row['start'],row['end'],row['name_type']
		txt_file = os.path.join(SaveLocation,f'{name_type}.txt')
		f = open(txt_file, 'w+', encoding='utf-8') # 结果保存文件
		# url队列
		q = queue.Queue()
		for i in range(start,int(end) + 1):
			my_url = url.format(i)
			q.put(my_url)

		# 设置线程数
		for i in list(range(1)):
			t = threading.Thread(target=main)
			t.setDaemon(True)
			t.start()
		q.join()
		f.flush()
		f.close()
