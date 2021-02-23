# ‐*‐ coding: utf‐8 ‐*‐
"""
从url的txt文件读取问题列表
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

    def parse(self, html,all_domain):
        contents = []
        next_page = ''
        if html:
            doc= pq(str(html))
            title = doc('h1').text().replace('?','').replace('？','').replace('/','')
            a_list = doc('.wd-item h3 a:last').items()
            for a in a_list:
                text,link = a.text(),a.attr('href')
                link = f'{all_domain}{link}'
                contents.append((text,link))
            if '下一页' in html:
                page_a = doc('a.cPage')
                next_page = page_a.attr('href')
                next_page = f'{all_domain}{next_page}'
        return contents,next_page


    def get_domain(self,url):
        all_domain = 'xxx'
        res=urlparse(url)
        try:
            domain = res.netloc
            all_domain = f'https://{domain}'
        except Exception as e:
            print('domain:',e)
        return all_domain


    def save(self,contents):
        for hang in contents:
            f.write('\t'.join(hang) + '\n')
            f.flush()


    # 统计每个域名排名的词数
    def run(self):
        while 1:
            url = q.get()
            print(url)
            all_domain = self.get_domain(url)
            try:
                html = self.get_html(url)
                contents,next_page = self.parse(html,all_domain)
                self.save(contents)
                while True:
                    if next_page:
                        html = self.get_html(next_page)
                        contents,next_page = self.parse(html,all_domain)
                        self.save(contents)
                        time.sleep(1)
                    else:
                        break
            except Exception as e:
                print(e)
            finally:
                q.task_done()
                gc.collect()
                time.sleep(1)


if __name__ == "__main__":
    start = time.time()
    save_path = './'
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    q = Spider_Content.read('xiaoqu_wenda_list.txt')
    f = open('xq_question.txt','w',encoding='utf-8')
    # 设置线程数
    for i in list(range(1)):
        t = Spider_Content()
        t.setDaemon(True)
        t.start()
    q.join()
    end = time.time()
    f.close()

