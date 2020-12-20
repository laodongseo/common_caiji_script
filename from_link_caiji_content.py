# ‐*‐ coding: utf‐8 ‐*‐
"""
从url的txt里采集每篇内容
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

    def parse(self, html):
        if html:
            doc= pq(str(html))
            title = doc('h1').text().replace('?','').replace('？','').replace('/','')
            p_list = doc('.detailc p').items()
            f = open('{0}{1}.txt'.format(save_path,title), 'w',encoding='utf-8')
            for p in p_list:
                duanluo = p.text().strip()
                # duan = str(p)  # 一行
                # if '<a' in duan:
                #     duan = re.sub('<a href=".*?16px;">','<a>',duan)
                # if 'img' in duan:
                #     num = random.randint(1,200)
                #     duan = re.sub('src=".*?.jpg"','src="/jiandian1/{0}xiu.jpg"'.format(num),duan)
                # duan = duan.replace('http://www.wanshifu.com','').replace('万师傅','天地一修')
                # 图片不写入
                if duanluo:
                    f.write(duanluo + '\n')
            f.flush()
            f.close()
            time.sleep(10)
            print('ok一个')

    # 统计每个域名排名的词数
    def run(self):
        while 1:
            url = q.get()
            print(url)
            try:
                html = self.get_html(url)
                self.parse(html)
            except Exception as e:
                print(e)
            finally:
                q.task_done()
                gc.collect()


if __name__ == "__main__":
    start = time.time()
    save_path = './39/'
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    q = Spider_Content.read('link_title_baidianfeng.txt')

    # 设置线程数
    for i in list(range(1)):
        t = Spider_Content()
        t.setDaemon(True)
        t.start()
    q.join()

    end = time.time()

