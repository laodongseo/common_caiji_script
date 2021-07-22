# -*- encoding=utf8 -*-
import psutil
import re
import os


# 通过进程名获取进程id
def processinfo(x):
  procs = list(psutil.process_iter()) # 获取所有服务列表
  for r in procs:
    print(r)
    p_name = r.name()
    if x == p_name:
        print(r)
        return r.pid
    

# 通过进程名获取监听端口
def get_port(p_name):
  '''通过pid获取端口号'''
  PID = processinfo(p_name)
  cmd = f'netstat -ano | findstr  {PID}'
  cmd_res = os.popen(cmd) # cmd_res是对象内存地址
  text = cmd_res.read()
  first_line = text.strip()
  print(first_line)
  line = re.sub(r'\s+',':',first_line)
  lis = line.split(':')
  if len(lis) > 2:
    p_port = lis[2] 
    return p_port
  else:
    print('端口获取异常')

if __name__ == "__main__":
    p_name = 'chromedriver.exe'
    my_port = get_port(p_name)
    print(my_port)
