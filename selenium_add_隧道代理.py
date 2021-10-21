"""
dumpsys activity | grep mFocusedActivity
"""


import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
import re
from pyquery import PyQuery as pq
from datetime import datetime, date
import string
import zipfile
import time


# (auth认证用户名,密码)+(代理隧道域名,端口号)生成zip扩展文件
def create_proxyauth_extension(tunnelhost, tunnelport, proxy_username, proxy_password, scheme='http', plugin_path=None):
    """代理认证插件
    """
    if plugin_path is None:
        plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(
        host=tunnelhost,
        port=tunnelport,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_path


proxyauth_plugin_path = create_proxyauth_extension(
    tunnelhost="tps247.kdlapi.com",  # 隧道域名
    tunnelport="15818",  # 端口号
    proxy_username="xxxx",  # 用户名
    proxy_password="xxxx"  # 密码
)



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
	option.add_argument("window-size=800,600")
	option.add_argument("--disable-features=VizDisplayCompositor")
	# option.add_argument('headless')
	option.add_argument('log-level=3') #屏蔽日志
	option.add_argument('--ignore-certificate-errors-spki-list') #屏蔽ssl error
	option.add_argument('-ignore -ssl-errors') #屏蔽ssl error
	option.add_experimental_option("excludeSwitches", ["enable-automation"]) 
	option.add_experimental_option('useAutomationExtension', False)
	No_Image_loading = {"profile.managed_default_content_settings.images": 1} #2是不加载
	option.add_experimental_option("prefs", No_Image_loading)
	# 屏蔽webdriver特征
	option.add_argument("--disable-blink-features")
	option.add_argument("--disable-blink-features=AutomationControlled")
	# option.add_extension('E:/py3script-工作/5i5j/ip_chajian/ProxySwitchyOmega.crx')
	# option.add_argument('--proxy-server=http://tps247.kdlapi.com:15818')  # 隧道域名:端口号
	option.add_extension(proxyauth_plugin_path)
	driver = webdriver.Chrome(options=option,executable_path=chromedriver_path )
	return driver


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
chromedriver_path = 'D:/install/pyhon36/chromedriver.exe'
ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
driver = get_driver(chrome_path,chromedriver_path,ua)
with open('ip_test.txt','w',encoding='utf-8') as f:
	while True:
		driver.get('http://httpbin.org/get')
		time.sleep(3)
		html = driver.page_source
		lis = re.findall('"origin": ".*?",',html,re.S)
		f.write(''.join(lis) + '\n')
		f.flush()
