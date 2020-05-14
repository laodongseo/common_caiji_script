"""
多类列表,只指定起始页采集,保存为不同文件
配置文件以制表符分割
url,small_type,max_type = line
small_type是小分类,max_type是大分类,方面命名文件用的
因为是抓取下一页的链接放到url队列
如果中间出现某个下一页抓取失败，则整个翻页抓取不全
"""

#‐*‐coding:utf‐8‐*‐
import requests
import threading
import queue
from pyquery import PyQuery as pq
import random
import time



# 获取源码
def get_html(url,retry=3):
    try:
        r = requests.get(url=url,headers=my_header, timeout=5)
    except Exception as e:
        print('获取源码失败', url, e)
        if retry > 0:
            time.sleep(30)
            get_html(url, retry - 1)
    else:
        html = r.text
        url = r.url
        return html,url


def get_wenda(html,url):
    doc = pq(html)
    title = doc('title').text()
    if '楼盘网' in title and 'ask' in url:
        page_next = doc('.pagenxt')
        if page_next:
            next_page = page_next.attr('href')
            print(next_page)
            q.put(next_page)
            list_a = doc('.content_box .right ul li a').items()
            for a in list_a:
                text = a('.question').text()
                link = a.attr('href')
                print(text,link)
                f.write('{0}\t{1}\n'.format(text,link))
            f.flush()

        else:
            print('无下一页')
    else:
        print('可能被ban....')
        return ['xxx','xxx']


def main():
    while 1:
        url = q.get()
        print(url)
        try:
            html,now_url = get_html(url)
            get_wenda(html,now_url)
        except Exception as e:
            print(e)  
        finally:
            q.task_done()
            time.sleep(5)


if __name__ == "__main__":
    my_header = {
'Host': 'www.loupan.com',
'Referer': 'http://bj.loupan.com/ask/',
'Upgrade-Insecure-Requests': '1',
'User-Agent':'Mozilla/5.0(Windows NT 6.1; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/79.0.3945.79Safari/537.36',
}

    for line in open('config.txt','r',encoding='utf-8'):
        line = line.strip().split('\t')
        url,small_type,max_type = line
        # 结果保存文件
        f = open('{0}_{1}.txt'.format(max_type,small_type), 'w+', encoding='utf-8')
        # url队列
        q = queue.Queue()
        for i in range(1):
            q.put(url)

        # 设置线程数
        for i in list(range(1)):
            t = threading.Thread(target=main)
            t.setDaemon(True)
            t.start()
        q.join()
        f.flush()
        f.close()
