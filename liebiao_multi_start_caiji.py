# ‐*‐ coding: utf‐8 ‐*‐

"""
配置多个列表,指定起始页采集
抓取下一页的链接放到url队列
如果中间出现某个下一页抓取失败，则整个翻页抓取不全
"""

#‐*‐coding:utf‐8‐*‐
import requests
import threading
import queue
from pyquery import PyQuery as pq
import random
import pandas as pd
import time,os
import traceback
import gzip
from io import BytesIO


def read_excel(filepath):
    q = queue.Queue()
    df = pd.read_excel(filepath).dropna()
    for index,row in df.iterrows():
        q.put(row['url'])
    return q


# 获取源码
def get_html(url,retry=3):
    try:
        r = requests.get(url=url,headers=my_header, timeout=15)
    except Exception as e:
        print('获取源码失败', url, e)
        if retry > 0:
            time.sleep(30)
            get_html(url, retry - 1)
    else:
        url = r.url
        if r.headers.get('Content-Encoding') == 'gzip':
            html = gzip.GzipFile(fileobj=BytesIO(r.content)).read().decode('utf-8',errors='ignore')
        else:
            html = r.content.decode('utf-8',errors='ignore')
        return html,url


def parse_html(html,url):
    doc = pq(str(html))
    li_obj = doc('.pagination li').eq(-1)
    if li_obj:
        next_page = li_obj('a').attr('href')
        print('\t',next_page)
        q.put('https://www.yutu.cn' + next_page)
    else:
        print('无下一页')
    # 采集内容
    content = []
    list_a = doc('.comm-soft-lists div.comm-item h2 a.h2-tite').items()
    for a in list_a:
        text = a.text().strip()
        link = a.attr('href')
        print(text)
        content.append((text,link))
    return content


def main():
    global IsHeader
    while 1:
        url = q.get()
        print(url)
        try:
            html,now_url = get_html(url)
            content = parse_html(html,now_url)
        except Exception as e:
            traceback.print_exc() 
        else:
            if isinstance(content,list):
                for element in content:
                    row = pd.Series(dtype=object)
                    row['title'] ,row['content'] = element
                    row['list_url'] = url
                    df = row.to_frame().T
                    with lock:
                        if IsHeader == 0:
                            df.to_csv(CsvFile,encoding='utf-8-sig',mode='w+',index=False,sep=',')
                            IsHeader = 1
                        else:
                            df.to_csv(CsvFile,encoding='utf-8-sig',mode='a+',index=False,sep=',',header=False)
        finally:
            q.task_done()
            time.sleep(3)


if __name__ == "__main__":
    my_header = {
'Referer': 'http://www.baidu.com/',
'Accept-Encoding': 'identity',
'User-Agent':'Mozilla/5.0(Windows NT 6.1; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/79.0.3945.79Safari/537.36',
}
    con_excel = 'conf.xlsx'
    CsvFile = os.path.splitext(con_excel)[0] + '采集url-title.csv'
    IsHeader =0
    lock = threading.Lock()
    q = read_excel(con_excel)

    # 设置线程数
    for i in list(range(1)):
        t = threading.Thread(target=main)
        t.daemon = True
        t.start()
    q.join()
