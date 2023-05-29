"""
读取excel中的url
采集文章保存
"""

#‐*‐coding:utf‐8‐*‐
import requests
import threading
import queue
from pyquery import PyQuery as pq
import time,traceback,random
import pandas as pd
import os

my_header = {
		'Accept':'application/json,text/plain,*/*',
		'Accept-Encoding':'deflate',
		'Connection':'keep-alive',
		'Host':'index.baidu.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0',
		}


def read_excel(filepath):
	q = queue.Queue()
	df = pd.read_excel(filepath).dropna())
	for index,row in df.iterrows():
		q.put(row)
	return q


# 获取源码
def get_html(url,retry=1):
	try:
		r = requests.get(url=url,headers=my_header,timeout=20)
	except Exception as e:
		print('获取源码失败',e)
		time.sleep(30)
		if retry > 0:
			get_html(url,retry-1)
	else:
		html = r.text
		return html


def parse(html):
	doc = pq(str(html))
	title = doc('h1.title').text().strip()
	p_tags = doc('article.single p').items()
	article = ' '.join([p.outer_html() for p in p_tags])
	return title,article


# 线程函数 
def main():
	global IsHeader
	while 1:
		row = q.get()
		url = row['url']
		print(url)
		try:
			html = get_html(url)
			title_article = parse(html)
		except Exception as e:
			traceback.print_exc()
			print('出错:',url)
			print(html,file=f_error)
			time.sleep(60)
		else:
			if isinstance(title_article,tuple):
					row['title'] ,row['content'] = title_article
					df = row.to_frame().T
					with lock:
						if IsHeader == 0:
							df.to_csv(CsvFile,encoding='utf-8-sig',mode='w+',index=False,sep=',')
							IsHeader = 1
						else:
							df.to_csv(CsvFile,encoding='utf-8-sig',mode='a+',index=False,sep=',',header=False)
			else:
				f_error.write(f'检查:{url}\n')
		finally:
			q.task_done()
			f_error.flush()
			time.sleep(3)


if __name__ == "__main__":
	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
	f_error = open('error.txt','w+',encoding='utf-8')
	excel_path = 'links.xlsx'
	q = read_excel(excel_path)
	CsvFile = os.path.splitext(excel_path)[0] + '采集结果.csv'
	IsHeader =0
	lock = threading.Lock()
	
	# 设置线程数
	for i in list(range(1)):
		t = threading.Thread(target=main)
		t.setDaemon(True)
		t.start()
	q.join()
