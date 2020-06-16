"""
多类列表,指定起始结尾翻页采集,保存为不同文件
配置文件以制表符分割
url,max_num,small_type,max_type = line
small_type是小分类,max_type是大分类,方便命名文件用的
http://www.loupan.com/ask/72-p{0}/  2   工业用房    房屋类型
"""

#‐*‐coding:utf‐8‐*‐
import requests
import threading
import queue
from pyquery import PyQuery as pq
import random
import time
from urllib import parse

# 获取源码
def get_html(url,retry=0):
    try:
        header = random.choice(my_header)
        r = requests.get(url=url,headers=header,timeout=5)
    except Exception as e:
        print('获取源码失败',e)
        time.sleep(6)
        if retry > 0:
            get_html(url,retry-1)
    else:
        html = r.content.decode('utf-8',errors='ignore')  # 用r.text有时候识别错误
        return html


# 源码分析
def parse(html):
    title_links = []
    doc = pq(html)
    title = doc('title').text()
    if '楼盘网' in title:
        p_list = doc('.lit_wrap a .zx_t').items()
        for p in p_list:
            title = p.text()
            link = p.parent('a').attr('href')
            title_links.append((title,link))
    else:
        print('源码异常,可能反爬')
    return title_links


# 线程函数
def main():
    while 1:
        url = q.get()
        print('url',url)
        try:
            html = get_html(url)
            title_links = parse(html)
        except Exception as e:
            print('-----')
            print(e)
        else:
            for title,link in title_links:
                f.write('{0}\t{1}\n'.format(title,link))
                print(title,link)
            f.flush()
        finally:
            q.task_done()
            time.sleep(6)


if __name__ == "__main__":
    # UA设置
    my_header = [{
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'},
          {
              'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
          {
              'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
          {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
          {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
          ]

    for line in open('config.txt','r',encoding='utf-8'):
        line = line.strip().split('\t')
        url,max_num,small_type,max_type = line
        # 结果保存文件
        f = open('{0}_{1}.txt'.format(max_type,small_type), 'w+', encoding='utf-8')
        # url队列
        q = queue.Queue()
        for i in range(1,int(max_num) + 1):
            my_url = url.format(i) if max_num != 0 else url
            q.put(my_url)

        # 设置线程数
        for i in list(range(1)):
            t = threading.Thread(target=main)
            t.setDaemon(True)
            t.start()
        q.join()
        f.flush()
        f.close()
