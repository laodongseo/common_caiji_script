# -*- encoding=utf8 -*-
"""
netstat  -aon|findstr  端口号
tasklist|findstr 端口号
https://jingyan.baidu.com/article/72ee561ab81a2ae16138dfcc.html
"""
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

# 获取目标python脚本产生的python进程id
def get_process_id(py_script_name):
    ids = []
    result = os.popen('wmic process where name="python.exe" get processid,commandline')
    res = result.read()
    res = res.strip().splitlines()
    for line in res:
        print(line)
        if py_script_name in line:
            lis = line.split(' ')
            for element in lis:
                element = element.strip()
                re_ret = re.search('^\d+$',element)
                if re_ret:
                    id = re_ret.group()
                    ids.append(id)
    return ids
