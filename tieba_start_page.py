# --*--coding: utf-8 --*--
import requests
import re
from pyquery import PyQuery as pq
import time


class Tieba(object):

    def __init__(self,name):
        self.url = 'https://tieba.baidu.com/f?ie=utf-8&kw={}'.format(name)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }


    def get_data(self,url,retry=1):
        try:
            r = requests.get(url=url,headers=self.headers, timeout=5)
        except Exception as e:
            print('获取源码失败', url, e)
            if retry > 0:
                time.sleep(30)
                self.get_data(url, retry - 1)
        else:
            status = r.status_code
            if status == 200:
                html = r.text
                return html


    def parse_data(self,data):
        tie_links = []
        next_link = ''
        # 干掉注释,规范html
        doc = pq(str(data).replace('<!--','').replace('-->',''))
        title = doc('title').text()
        if '-百度贴吧' in title:
            next_obj = doc('#frs_list_pager .next')
            tiezis_obj = doc('#thread_list li.j_thread_list div.threadlist_title a').items()
            next_link = next_obj.attr('href')
            for tiezi in tiezis_obj:
                link = tiezi.attr('href')
                tie_links.append(link)
        else:
            print('源码异常....暂停1分钟')
            time.sleep(60)
        return tie_links,next_link



    def save_data(self,tie_list):
        for tiezi in tie_list:
            print(tiezi)
            f.write('{0}\n'.format(tiezi))
        f.flush()


    def run(self):
        data = self.get_data(self.url)
        tie_links,next_link = self.parse_data(data)
        self.save_data(tie_links)
        while 1:
            if next_link:
                next_link = 'https:' + next_link if 'https://' not in next_link else next_link
                print(next_link)
                data = self.get_data(next_link)
                tie_links,next_link = self.parse_data(data)
                self.save_data(tie_links)
                time.sleep(5)
            else:
                break

if __name__ == '__main__':
    f = open('tiezi.txt','w',encoding='utf-8')
    tieba = Tieba('外链吧')
    tieba.run()
    f.flush()
    f.close()
