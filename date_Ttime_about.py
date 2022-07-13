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


local_time = time.localtime()
today = time.strftime('%Y-%m-%d_%H-%M-%S', local_time)
