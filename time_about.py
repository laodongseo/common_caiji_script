# 获取昨日时间戳
def get_last_unix():
    today = datetime.date.today()
    last_day = today + timedelta(days=-1)
    last_day = last_day.strftime('%Y-%m-%d:00:00:00')
    print(last_day)
    # 转为时间数组
    last_day = time.strptime(last_day, '%Y-%m-%d:00:00:00')
    # 转为时间戳
    last_day_unix = time.mktime(last_day)
    # 转为13位时间戳
    last_day_unix = int(round(last_day_unix)) * 1000
    return last_day_unix


# 获取某几天的时间戳
def get_time_unix(num):
    unix_times = []
    today = datetime.date.today()
    for i in range(1,num+1):
        the_day = today + timedelta(days=int('-{0}'.format(i)))
        the_day = the_day.strftime('%Y-%m-%d:00:00:00')
        # 转为时间数组
        the_day = time.strptime(the_day, '%Y-%m-%d:00:00:00')
        # 转为时间戳
        the_day_unix = time.mktime(the_day)
        # 转为13位时间戳
        the_day_unix = int(round(the_day_unix)) * 1000
        unix_times.append(the_day_unix)
    return unix_times


# 格式化今天的日期
from datetime import date

today = date.today()
# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
print("d1 =", d1)

# Textual month, day and year	
d2 = today.strftime("%B %d, %Y")
print("d2 =", d2)

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)

# Month abbreviation, day and year	
d4 = today.strftime("%b-%d-%Y")
print("d4 =", d4)

# 正则匹配日期
import datetime
from datetime import date
import re
s = "Jason's birthday is on 1991-09-21 1991-9-21"
match = re.search(r'\d{4}-\d{1,2}-\d{1,2}', s)
date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
print(date)
https://blog.softhints.com/python-regex-match-date/
    
# ‐*‐ coding: UTF-8 ‐*‐
from datetime import  datetime
from datetime import timedelta


# 日期对象
today_obj = datetime.now() # datetime对象
print(today_obj,type(today_obj))
print(today_obj.year) # 年,整型数值
print(today_obj.month) # 月,整型数值
print(today_obj.day) # 日,整型数值
print(today_obj.hour) # 时,整型数值
print(today_obj.minute) # 分,整型数值
print(today_obj.second) # 秒,整型数值
print('----------------------------')

# 时间差,timedelta对象
date_diff = timedelta(days=10)
print(date_diff,type(date_diff))
print(today_obj - date_diff)  # 10天前
date_diff = timedelta(days=-10)
print(today_obj - date_diff)  # 10天后
print('=================================')
# 字符串转为日期对象
str_date = '2021-11-11 11:11:11'
date_obj = datetime.strptime(str_date,"%Y-%m-%d %H:%M:%S")
print(date_obj,type(date_obj))
print('---------------------------------')
# 日期对象转为字符串
today_obj = datetime.now() # datetime对象
str_date = today_obj.strftime("%Y-%m-%d %H:%M:%S")
print(str_date)

