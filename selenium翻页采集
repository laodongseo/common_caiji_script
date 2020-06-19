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
import pandas as pd
import time
import tld
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_html(url):
    driver.get(url)
    # 等待页面加载
    page = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "page"))
    )
    html = driver.page_source
    get_name(html)
    while True:
        try:
            # 等待下一页
            next_page = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="page"]/a[5]'))
            )
        except Exception as e:
            print('无下一页',e)
            break
        else:
            next_page.click()
            page = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "page"))
            )
            html = driver.page_source
            get_name(html)


def get_name(html):
    doc = pq(html)
    title = doc('title').text()
    if '房天下' in title:
        xiaoqu_infos = doc('.houselist li .houseInfo').items()
        for xiaoqu_info in xiaoqu_infos:
            xiaoqu_link = xiaoqu_info('h3 .title').attr('href')
            xiaoqu_name = xiaoqu_info('h3 .title').text().replace('\n','')
            xiaoqu_fang_num = xiaoqu_info('h3 strong').text().replace('\n','')
            xiaoqu_qita = xiaoqu_info('p').text().replace('\n','')
            xiaoqu_loudong = xiaoqu_info('.unit').text().replace('\n','')
            # exit()
            f.write(
                '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(xiaoqu_name, xiaoqu_link, xiaoqu_fang_num, xiaoqu_qita, xiaoqu_loudong))
        f.flush()
    else:
        print('可能被ban....')
        return ['xxx','xxx']


if __name__ == "__main__":
    pc_ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    option = Options()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # 禁止图片加载
            'notifications': 2  # 禁止弹窗
        }
    }
    option.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=option)

    for line in open('config_school.txt','r',encoding='utf-8'):
        line = line.strip().split('\t')
        url,small_type,max_type = line
        # 结果保存文件
        f = open('{1}_{0}.txt'.format(max_type,small_type), 'a+', encoding='utf-8')
        # url队列
        get_html(url)
