# -*- coding:UTF-8 -*-
"""
excel有2个字段 字段2为编码url
"""
import pandas as pd
from urllib.parse import unquote
df = pd.read_excel('燕窝价格 - 百度.xlsx')

lis_ser = []
for i in df.iterrows():
    ser = i[1]
    print(ser)
    url_encode = ser[1]
    try:
        url = unquote(url_encode, 'utf-8')
    except Exception as e:
        print('失败')
        url = 'error'
    ser['real_url'] = url
    lis_ser.append(ser)

df_last = pd.DataFrame(lis_ser)
df_last.to_excel('aaaaa.xlsx',index=False)
