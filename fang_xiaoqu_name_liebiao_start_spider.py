# --*--coding: utf-8 --*--
"""
配置文件excel量列
一列代表类型,一列代表列表页起始页
每一类列表页单线程翻页采集直到结束
"""
import requests
import re
from pyquery import PyQuery as pq
import time
import pandas as pd

class ListSpider(object):

    @staticmethod
    def get_config(excel_path):
        """
        配置多个列表首页url及分类
        """
        df_config = pd.read_excel(excel_path)
        return df_config


    def __init__(self,now_type,start_page):
        self.start_url = start_page
        self.now_type = now_type
        self.headers = {
            'authority':'esf.fang.com',
            'method':'GET',
            'scheme':'https',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':'deflate',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pt;q=0.5',
            'cache-control':'no-cache',
            'cookie':'global_cookie=29bssbz7ba96couqav96aote91ykjxt6482; global_wapandm_cookie=3knui28y6ulu6gmpkpf6x8k741nklaipx2b; newhouse_user_guid=F5C15BA2-BDC9-B9B1-27A7-3FA91C29FDA4; bdshare_firstime=1634712367757; lastscanpage=0; fang_hao123_layed=1; city=www1; csrfToken=c4A6Rr5krKvZ7OzNDkuICsD1; __utma=147393320.1909042886.1610686527.1636089454.1636338053.44; __utmc=147393320; __utmz=147393320.1636338053.44.40.utmcsr=www1.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=147393320.30.10.1636338053; g_sourcepage=esf_xq%5Eesf_pc; unique_cookie=U_qssa8nhfye36grq0g3fu5k1wm3wkvq1dv3g*15',
            'pragma':'no-cache',
            'referer':'https://esf.fang.com/housing/14632__0_3_0_0_1_0_0_0/',
            'sec-ch-ua':'"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'same-origin',
            'sec-fetch-user':'?1',
             'referer': 'https://esf.fang.com/',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
        }


    def get_html(self,url,retry=1):
        try:
            r = requests.get(url=url,headers=self.headers, timeout=10)
        except Exception as e:
            print(2-retry,'获取源码失败', url, e)
            if retry > 0:
                time.sleep(30)
                self.get_html(url, retry - 1)
        else:
            status = r.status_code
            if status == 200:
                html = r.text
                return html


    def parse_html(self,html):
        contents = []
        next_link = None
        doc = pq(html)
        # 获取翻页地址
        a_list = doc('.fanye a').items()
        for a_obj in a_list:
            text = a_obj.text().strip()
            if '下一页' in text:
                next_link = a_obj.attr('href')
        # next_link = doc('.pageSty a').eq(0).attr('href')
        dd_objs = doc('.houseList .list dl.plotListwrap  dd').items()
        for dd_obj in dd_objs:
            element_dict = {}
            # 小区名字和链接
            a_obj = dd_obj('p a.plotTit')
            xq_name = a_obj.text().strip()
            xq_link = a_obj.attr('href')
            element_dict['xq_name'] = xq_name
            element_dict['xq_link'] = xq_link
            # 小区租房二手房信息
            a_objs = dd_obj('ul.sellOrRenthy li a').items()
            num = 0
            for a_obj in a_objs:
                count = a_obj.text().strip()
                link = a_obj.attr('href')
                if num == 0:
                    element_dict['sale_count'] = count
                    element_dict['sale_link'] = link
                else:
                    element_dict['rent_count'] = count
                    element_dict['rent_link'] = link
                num+=1
            contents.append(element_dict)
        return contents,next_link


    def save_data(self,contents):
        for element_dict in contents:
            row = '\t'.join(list(element_dict.values()))
            f.write(f'{row}\n')
            f.flush()


    def run(self):
        html = self.get_html(self.start_url)
        if not html:
            print('列表首页获取失败')
            return
        contents,next_link = self.parse_html(html)
        self.save_data(contents)
        while 1:
            if next_link:
                # next_link = ''.join(next_link.split('__')[1:])
                next_link = f'https://esf.fang.com{next_link}'
                print(self.now_type,next_link)
                html = self.get_html(next_link)
                if not html:
                   print(next_link,'列表首页获取失败')
                   break
                contents,next_link = self.parse_html(html)
                self.save_data(contents)
                time.sleep(5)
            else:
                break

if __name__ == '__main__':
    f = open('bj_fang_xiaoqu.txt','w',encoding='utf-8')
    dfConfig = ListSpider.get_config(excel_path='./list_config.xlsx')
    for index_num,row_series in dfConfig.iterrows():
        now_type,start_page = row_series[['类别','url']].tolist()
        print(now_type,start_page)
        Spider = ListSpider(now_type,start_page)
        Spider.run()
        f.flush()
    f.close()
