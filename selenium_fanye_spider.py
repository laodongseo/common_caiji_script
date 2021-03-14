# ‐*‐ coding: utf‐8 ‐*‐
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import traceback
import re
import os
from pyquery import PyQuery as pq

s1 = r""" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile" """


class element_has_text(object):
  # locator是元祖
  def __init__(self, locator, text):
    self.locator = locator
    self.text = text

  def __call__(self, driver):
    # element = driver.find_element(*self.locator)
    element = WebDriverWait(driver, 900).until(EC.visibility_of_element_located((self.locator)))
    print(element)
    print(element.text)
    if self.text in element.text:
        return element
    else:
        return False




def get_driver(chrome_path,chromedriver_path,ua):
    ua = ua
    option = Options()
    option.binary_location = chrome_path
    # option.add_argument('disable-infobars')
    # option.add_argument("user-agent=" + ua)
    # option.add_argument("--no-sandbox")
    # option.add_argument("--disable-dev-shm-usage")
    # option.add_argument("--disable-gpu")
    # option.add_argument("--disable-features=NetworkService")
    # # option.add_argument("--window-size=1920x1080")
    # option.add_argument("--disable-features=VizDisplayCompositor")
    # # option.add_argument('headless')
    # option.add_argument('log-level=3') #屏蔽日志
    # option.add_argument('--ignore-certificate-errors-spki-list') #屏蔽ssl error
    # option.add_argument('-ignore -ssl-errors') #屏蔽ssl error
    # option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    # option.add_experimental_option('useAutomationExtension', False)
    # No_Image_loading = {"profile.managed_default_content_settings.images": 1}
    # option.add_experimental_option("prefs", No_Image_loading)
    # # 屏蔽webdriver特征
    # option.add_argument("--disable-blink-features")
    # option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=option,executable_path=chromedriver_path)
    return driver



def parse_html(html,now_url):
    next_page = ''
    rows_all = []
    doc= pq(str(html))
    title = doc('title').text()
    if '口红' in title:
        tr_lefts = doc('div.items div.J_MouserOnverReq div.pic a').items() 
        next_page_obj = doc('li.next a.J_Ajax')
        next_page = next_page_obj.text()
        for td_obj in tr_lefts:
            text = td_obj('img').attr('alt')
            link = td_obj.attr('href')
            link = f'https://{link}'
            rows_all.append((text,link))
    return rows_all,next_page



def save(datas,url_str):
    for data in datas:
        data_str = '\t'.join(data)
        f.write(f'{data_str}\t{url_str}\n')
    f.flush()


def main():
    page_num = 1
    global driver
    # driver.get('https://login.taobao.com/member/login.jhtml')
    # wait = WebDriverWait(driver, 60)
    # element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 's-name')))
    driver.get('https://s.taobao.com/search?q=口红')
    content_left = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "total"))
    )
    html, now_url = driver.page_source, driver.current_url
    rows_all,next_page = parse_html(html,now_url)
    print('首页处理完毕:',next_page)
    # print(rows_all)
    if not next_page:
        return
    save(rows_all,now_url)
    while True:
        if  next_page:
            page_num+=1
            print('点击页码',page_num)
            # 点击翻页
            driver.execute_script(next_page_click_js)
            # time.sleep(10)
            # 判断翻页是否加载完
            # wait = WebDriverWait(driver, 900)
            try:
                # element = wait.until(element_has_text((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[@class="item active"]/span'),str(page_num)))
                while 1:
                    element = WebDriverWait(driver, 900).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[@class="item active"]/span')))
                    print(element)
                    print(element.text)
                    if str(page_num) in element.text:
                        break
                    else:
                        break
            except Exception as e:
                print(e)
                f.write(driver.page_source)
                return
            print('当前页码',element.text)
            driver.execute_script(js_xiala)
            time.sleep(15)
            html, now_url = driver.page_source, driver.current_url
            rows_all,next_page = parse_html(html,now_url)
            print(f'翻页文本:{next_page}')
            save(rows_all,now_url)
        else:
            break


if __name__ == "__main__":
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    chromedriver_path = 'D:/install/pyhon36/chromedriver.exe'
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    next_page_click_js = 'document.querySelector("#mainsrp-pager > div > div > div > ul > li.item.next > a").click()'
    js_xiala = 'window.scrollBy(0,document.body.scrollHeight)'
    driver = get_driver(chrome_path,chromedriver_path,ua)
    f = open('res.txt','w',encoding='utf-8')
    main()
