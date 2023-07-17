# ‐*‐ coding: utf‐8 ‐*‐

"""
配置多个列表,指定起始页采集
抓取下一页的链接放到url队列
如果中间出现某个下一页抓取失败，则整个翻页抓取不全
"""

#‐*‐coding:utf‐8‐*‐
import requests
import threading
import queue,psutil
from pyquery import PyQuery as pq
import random
import pandas as pd
import time,os,chardet
import traceback
import gzip
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def read_excel(filepath):
    q = queue.Queue()
    df = pd.read_excel(filepath).dropna()
    for index,row in df.iterrows():
        if row['url']:
            q.put(row['url'])
    return q

# 获取chromedriver及其启动的浏览器pid
def get_webdriver_chrome_ids(driver):
    """
    浏览器pid是chromedriver的子进程
    """
    all_ids = []
    main_id = driver.service.process.pid
    all_ids.append(main_id)
    p = psutil.Process(main_id)
    child_ids = p.children(recursive=True)
    [all_ids.append(id_obj.pid) for id_obj in child_ids]
    return all_ids


# 根据pid杀死进程
def kill_process(p_ids):
    try:
        for p_id in p_ids:
            os.system(f'taskkill  /f /pid {p_id}')
    except Exception as e:
        pass
    time.sleep(1)



def get_driver(chrome_path,chromedriver_path,ua):
    ua = ua
    option = Options()
    option.binary_location = chrome_path
    # option.add_argument('disable-infobars')
    option.add_argument("user-agent=" + ua)
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-features=NetworkService")
    # option.add_argument("--window-size=1920x1080")
    option.add_argument("--disable-features=VizDisplayCompositor")
    option.add_argument('headless')
    option.add_argument('log-level=3') #屏蔽日志
    option.add_argument('--ignore-certificate-errors-spki-list') #屏蔽ssl error
    option.add_argument('-ignore -ssl-errors') #屏蔽ssl error
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    No_Image_loading = {"profile.managed_default_content_settings.images": 1}
    option.add_experimental_option("prefs", No_Image_loading)
    option.add_argument("--disable-blink-features")
    option.add_argument("--disable-blink-features=AutomationControlled")
    s = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=s,options=option)
    return driver

def close_handle():
    global driver
    if len(driver.window_handles) > 1:
        for handle in driver.window_handles[0:-1]:
            driver.switch_to.window(handle)
            time.sleep(1)
            driver.close()
        # 检测关闭结束,只剩1个handle
        while True:
            if len(driver.window_handles) == 1:
                break
        # 切到唯一窗口
        driver.switch_to.window(driver.window_handles[0])


# 获取源码
def get_html(url):
    global driver,OneHandle_UseNum
    # 1个tab达到最大使用次数,开新tab用
    if OneHandle_UseNum > OneHandle_MaxNum:
        # driver.switch_to.new_window('tab') # selenium4
        driver.execute_script(f"window.open('{url}')")
        close_handle()
        OneHandle_UseNum = 1
    else:
        driver.get(url)
    OneHandle_UseNum += 1
    html = driver.page_source
    url = driver.current_url
    return html,url



def parse_html(html,url):
    doc = pq(str(html))
    obj = doc('.tsp_nav a.tsp_next')
    if obj:
        next_page = obj.attr('href')
        print('\t',next_page)
        # q.put(f'https://www.pc6.com/{next_page}')
    else:
        print('无下一页')
    # 采集内容
    content = []
    list_li = doc('.d_list_txt ul li').items()
    for li in list_li:
        # time_str = li('span.c_tit a').eq(-1).text().strip()
        text = li('span.c_tit a').text().strip()
        link = li('a').attr('href')
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
                    row['title'] ,row['url'] = element
                    df = row.to_frame().T
                    with lock:
                        if IsHeader == 0:
                            df.to_csv(CsvFile,encoding='utf-8-sig',mode='w+',index=False,sep=',')
                            IsHeader = 1
                        else:
                            df.to_csv(CsvFile,encoding='utf-8-sig',mode='a+',index=False,sep=',',header=False)
        finally:
            q.task_done()
            time.sleep(2)


if __name__ == "__main__":
    OneHandle_UseNum,OneHandle_MaxNum = 1,1 
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chromedriver_path = r'D:/py3script/seleniumtest/chromedriver.exe'
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    driver = get_driver(chrome_path,chromedriver_path,ua)

    webdriver_chrome_ids = get_webdriver_chrome_ids(driver)
    print(f'webdriver+chrome的pid:{webdriver_chrome_ids}')
    
    con_excel = 'conf.xlsx'
    CsvFile = os.path.splitext(con_excel)[0] + '-sina-title.csv'
    IsHeader =0
    lock = threading.Lock()
    q = read_excel(con_excel)

    # 设置线程数
    for i in list(range(1)):
        t = threading.Thread(target=main)
        t.daemon = True
        t.start()
    q.join()
