# --*--coding: utf-8 --*--
"""
指定起始页url
单线程翻页采集直到结束
链家翻页url源码没有，需要属性拼接:page-data='{"totalPage":30,"curPage":1}
"""
import requests
import re
from pyquery import PyQuery as pq
import time
import random
from urllib.parse import urlparse
import json



def get_data(url,retry=1):
    ua = random.choice(UA)
    header = {'User-Agent':ua}
    try:
        r = requests.get(url=url,headers=header, timeout=5)
    except Exception as e:
        print('获取源码失败', url, e)
        if retry > 0:
            time.sleep(30)
            get_data(url, retry - 1)
    else:
        status = r.status_code
        if status == 200:
            html = r.text
            return html


def parse_data(html,url):
    texts = []
    total_page = None
    div_chengjiao = 'xxx'
    if html and '链家' in html:
        try:
            doc = pq(html)
            div_alls = doc('.listContent li.xiaoquListItem').items()
            page_fanye_obj = doc('.house-lst-page-box')
            for div_all in div_alls:
                # 获取成交
                a_chengjiao_objs = div_all('div.info div.houseInfo a').items()
                for a_chengjiao_obj in a_chengjiao_objs:
                    if 'chengjiao' in str(a_chengjiao_obj.attr('href')):
                        div_chengjiao = a_chengjiao_obj.text()
                # 获取小区名和url
                div_xiaoqu_obj = div_all('div.info div.title a')
                xiaoqu_name,xiaoqu_url = div_xiaoqu_obj.text(),div_xiaoqu_obj.attr('href')
                # 获取租房数
                xiaoqu_zu = div_all('div.info div.houseInfo a:last')
                xiaoqu_zu_info = xiaoqu_zu.text()
                # 获取二手房数
                xiaoqu_er_info = div_all('div.xiaoquListItemRight a').text()
                # print(xiaoqu_name,xiaoqu_url,xiaoqu_zu_info,xiaoqu_er_info,div_chengjiao)
                texts.append([xiaoqu_name,xiaoqu_url,xiaoqu_zu_info,xiaoqu_er_info,div_chengjiao])
                # texts = [str(i) for i in texts]
        except Exception as e:
            print('未提取到信息', e,url)
        if page_fanye_obj:
            data_page = page_fanye_obj.attr('page-data')
            data_page_dict = json.loads(data_page)
            total_page = data_page_dict['totalPage']

    return texts,total_page



def save_data(name,texts):
    for hang in texts:
        hang = [str(i) for i in hang]
        str_text = '\t'.join(hang)
        if str_text:
            f.write('{0}\t{1}\n'.format(name,str_text))
        f.flush()


def run(name,url):
    data = get_data(url)
    texts,total_page = parse_data(data,url)
    # print(texts)
    save_data(name,texts)
    print(name,total_page,'-----')
    if total_page:
        total_page = int(total_page)
        fanye_urls = []
        if total_page > 1:
            for i in range(2,int(total_page)+1):
                url = url.replace(r'?from=rec','')
                url_fanye_now = url + 'pg{0}/'.format(i)
                fanye_urls.append(url_fanye_now)
            print(fanye_urls)
            for fanye_url in fanye_urls:
                data = get_data(fanye_url)
                texts,total_page = parse_data(data,url)
                save_data(name,texts)
                time.sleep(5)

if __name__ == '__main__':
    f = open('xiaoqu_fangyuan1.txt','a',encoding='utf-8')
    f_error = open('error.txt','a',encoding='utf-8')
    # UA设置
    UA = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
          'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
          'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
          'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
          'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
          ]
    for line in open('shangquan_url1.txt','r',encoding='utf-8'):
        i = line.strip().split('\t')
        name,url = i
        try:
            run(name,url)
        except Exception as e:
            f_error.write(line + '\n')
            f_error.flush()
    f.close()
    f_error.close()
