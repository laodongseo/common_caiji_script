# ‐*‐ coding: utf‐8 ‐*‐
"""
第一轮获取N个ip后
1个ip开启1个线程并发抓取,每个ip(线程)设置最大使用次数
第一轮ip使用结束,获取第二轮ip
"""
import requests
import threading
import queue
from pyquery import PyQuery as pq
import time
import traceback
import gc
import pandas as pd
import json


my_header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

# 请求接口
api_url = 'https://dps.kdlapi.com/api/getdps/?orderid=911936246240517&num=10&signature=xxs3ctfxbm57zic8xs73qpvp16ico8gu&pt=1&format=json&sep=1'


# 获取接口返回ip,请求1次
def get_ip(api_url,retry=0):
    try:
        r = requests.get(url=api_url,headers=my_header, timeout=15)
    except Exception as e:
        print('func get_ip',e)
        if retry > 0:
            get_ip(api_url, retry - 1)
    else:
        html = r.json()
        if html['code']==0:
            proxy_list = html['data']['proxy_list']
            return proxy_list


# 获取excel数据入队列
def read_excel(excel_path,my_sheet):
    q = queue.Queue()
    df = pd.read_excel(excel_path,sheet_name=my_sheet)
    for index,row_series in df.iterrows():
        q.put(row_series)
    return q


# 获取拼多多源码,异常由min()捕获
def get_html(session,my_url,my_header,proxies):
    r = session.get(url=my_url,headers=my_header,proxies=proxies,timeout=30)
    html = r.content.decode('utf-8',errors='ignore')
    return html


# 解析数据
def parse_html(html):
    doc = pq(str(html))
    str_content = doc('#__NEXT_DATA__').text().strip()
    dict_content = json.loads(str_content)
    pageProps = dict_content['props']['pageProps']
    if pageProps['error'] == 'no_error':
        content = doc('div.card-wrapper .no-goods-tip p').text()
        if '未查询到相关商品' in content:
            return '无商品'

        # 商品列表(元素为字典)
        goods_list = pageProps['list']
        num_all = len(goods_list) # 商品数量
        # 循环列表构造dataframe结构
        df_page = pd.DataFrame(columns=['goodsId','salesTip','minGroupPrice','categoryName'])
        for good in goods_list:
            goodsId = good['goodsId'] # int数据
            salesTip = good['salesTip'].strip()
            if '万' in str(salesTip):
                salesTip = salesTip.replace('万','').replace('+','')
                salesTip = float(salesTip) * 10000
            if '万' not in str(salesTip) and '+' in str(salesTip):
                salesTip = salesTip.replace('+','')
                salesTip = float(salesTip)
            minGroupPrice = good['minGroupPrice']/1000 # int数据
            categoryName = good['categoryName'] # 有的商品无类目
            categoryName = categoryName.strip() if categoryName else '无类目'
            df_page = df_page.append({'goodsId':goodsId,'salesTip':salesTip,'minGroupPrice':minGroupPrice,'categoryName':categoryName},ignore_index=True)
        # 转为浮点型序列(转int有safe问题)
        df_page['salesTip'] = df_page.loc[:,'salesTip'].astype('float64')
        if df_page['salesTip'].sum() == 0:
            return f'无销量|{categoryName}'

        bool_if = df_page['salesTip'] == df_page['salesTip'].max()
        series_max_good = df_page[bool_if].iloc[0]
        max_good = series_max_good.to_dict()
        return max_good,num_all
    else:
        return '异常查询'


def main(ip_port,proxies):
    t_name = threading.currentThread().name # 线程名
    session = requests.session()
    session.keep_alive = False
    for i in range(1,max_req_num+1):
        series_row = q.get()
        kwd = series_row['关键词']
        url = f"https://youhui.pinduoduo.com/search/landing?keyword={kwd}"
        print(f'{t_name},{ip_port},第{i}次,{url}')
        try:
            html = get_html(session,url,my_header,proxies)
            if not html:
                print('未获取源码,重入队列')
                q.put(series_row)
                continue
            if '"success":false' in html:
                print('触发安全策略,重入对列',html)
                q.put(series_row)
                continue
            info_good = parse_html(html)
            if '无商品' == info_good:
                series_row['goodsId'] = 0
                series_row['salesTip'] = 0
                series_row['minGroupPrice'] = 0
                series_row['categoryName'] = '无'
            elif '无销量' in info_good:
                series_row['goodsId'] = 0
                series_row['salesTip'] = 0
                series_row['minGroupPrice'] = 0
                series_row['categoryName'] = info_good.split('|')[-1]
            elif '异常查询' == info_good:
                print('异常查询,重入队列')
                q.put(series_row)
                continue
            else:
                print(info_good)
                max_good,num_all = info_good   # max_good为dict
                series_row['goodsId'] = max_good['goodsId']
                series_row['salesTip'] = max_good['salesTip']
                series_row['minGroupPrice'] = max_good['minGroupPrice']
                series_row['categoryName'] = max_good['categoryName']
            line = series_row.tolist()
            line = [str(i) for i in line]
            line = '\t'.join(line)
            # 计算价格
            if series_row['minGroupPrice'] !=0:
                value = round(float(series_row['价格']) / float(series_row['minGroupPrice']),2)
            else:
                value = 0
            lock.acquire()
            f.write(f'{line}\t{value}\n') # 多线程加锁防止写入错乱
            lock.release()
            f.flush()
            time.sleep(sleep_time)
        except requests.exceptions.ProxyError as e:
            print(f'proxyError:停止使用此ip,{ip_port}',e)
            break
        except requests.exceptions.ReadTimeout as e:
            print(f'ReadTimeout:停止使用此ip,{ip_port}', e)
            break
        except requests.exceptions.ConnectTimeout as e:
            print(f'ConnectTimeout:停止使用此ip,{ip_port}', e)
            break
        except Exception as e:
            print('main...',e)
            traceback.print_exc(file=open('log_pdd_kuaidaili.txt', 'a'))
        finally:
            q.task_done()
            gc.collect()
            time.sleep(sleep_time)


def run():
    while True:
        proxy_list = get_ip(api_url)
        print(proxy_list)
        if proxy_list:
            thread_list = []
            for ip_port in proxy_list:
                proxies = {
                    "http": f"http://2330371368:m5e6rs9f@{ip_port}",
                    "https": f"http://2330371368:m5e6rs9f@{ip_port}",
                }
                t = threading.Thread(target=main,args=((ip_port,proxies)))
                thread_list.append(t)
                t.setDaemon(True)
                t.start()
            for t in thread_list:
                t.join()
        else:
            print('ip用尽...请检查订单确认')
            break
        time.sleep(0.1)
        print('获取下一轮ip')


if __name__ == "__main__":
    # excel文件及目标sheet
    excel_file, my_sheet = '关键词列表样式.xlsx', 'Sheet1'
    # 关键词队列
    q = read_excel(excel_file, my_sheet)
    # 结果保存文件
    f = open('taobao_vs_pdd_res.txt', 'w', encoding='utf-8')
    lock = threading.Lock()
    max_req_num = 120  # 设置1个ip最多用几次
    sleep_time = int(180 / max_req_num)  # 1个ip访问pdd时间间隔
    run()
    q.join()
    f.flush()
    f.close()
