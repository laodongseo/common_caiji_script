# -*- coding:UTF-8 -*-
"""
把一份excel数据平均分组 添加栏目名
"""
import pandas as pd
import os


tags = 'a,b,c,d'.split(',')
excel_file = 'aa_res.xlsx'

df = pd.read_excel(excel_file)
all_num = df.shape[0]
group_num = int(all_num/len(tags))

print(all_num,group_num)
group_list = [(i,i+group_num) for i in range(0,all_num,group_num)]

num = 0
for i,j in group_list:
	df.loc[i:j,'栏目1']  = tags[num]
	num +=1

res_file = os.path.splitext(os.path.basename(excel_file))[0]
df.to_excel(f'{res_file}---.xlsx')
