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


# 获取一个时间段时间戳
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
