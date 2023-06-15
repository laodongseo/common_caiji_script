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
import time
import traceback


def read_excel(filepath):
    q = queue.Queue()
    df = pd.read_excel(filepath).dropna()
    for index,row in df.iterrows():
        q.put(row)
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
        html = r.text
        url = r.url
        return html,url


def parse_html(html,url):
    doc = pq(str(html))
    page_next = doc('.pagenxt')
    if page_next:
        next_page = page_next.attr('href')
        print(next_page)
        q.put(next_page)
    else:
        print('无下一页')
    # 采集内容
    content = []
    list_a = doc('.content_box .right ul li a').items()
    for a in list_a:
        text = a('.question').text()
        link = a.attr('href')
        print(text,link)
        content.append((text,link))
    f.flush()


def main():
    global IsHeader
    while 1:
        row = q.get()
        url = row['url']
        try:
            html,now_url = get_html(url)
            content = parse_html(html,now_url)
        except Exception as e:
            traceback.print_exc() 
        else:
            if isinstance(content,tuple):
                row['title'] ,row['content'] = content
                df = row.to_frame().T
                with lock:
                    if IsHeader == 0:
                        df.to_csv(CsvFile,encoding='utf-8-sig',mode='w+',index=False,sep=',')
                        IsHeader = 1
                    else:
                        df.to_csv(CsvFile,encoding='utf-8-sig',mode='a+',index=False,sep=',',header=False)
        finally:
            q.task_done()
            time.sleep(5)


if __name__ == "__main__":
    my_header = {
'Host': 'www.loupan.com',
'Referer': 'http://bj.loupan.com/ask/',
'User-Agent':'Mozilla/5.0(Windows NT 6.1; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/79.0.3945.79Safari/537.36',
}
    con_excel = 'con.xlsx'
    CsvFile = os.path.splitext(con_excel)[0] + '采集结果.csv'
    IsHeader =0
    lock = threading.Lock()
    q = read_excel(con_excel)

    # 设置线程数
    for i in list(range(1)):
        t = threading.Thread(target=main)
        t.setDaemon(True)
        t.start()
    q.join()
    f.flush()
    f.close()
