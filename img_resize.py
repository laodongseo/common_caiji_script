# -*- coding: utf-8 -*-
"""
用open cv缩放图片
固定尺寸修改图片或者按比例修改图片
坑：opencv的imread方法不支持中文路径，读取返回None
cv2.imdecode(np.fromfile(img, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
"""
import cv2
import os 
import threading
import numpy as np

def get_files(file_path,exts):
	file_list = []
	dir_or_files = os.listdir(file_path)
	for dir_or_file in dir_or_files:
		dir_file_path = os.path.join(file_path, dir_or_file)
		if not os.path.isdir(dir_file_path):
			my_ext = os.path.splitext(dir_file_path)[-1]
			file_list.append(dir_file_path) if my_ext in exts else file_list
	return file_list


# 重置为固定尺寸
def resize_fixed(img,width,height):
	# 支持中文路径
	img_obj=cv2.imdecode(np.fromfile(img, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	print('Image Height,Width',img_obj.shape[0],img_obj.shape[1])
	resize_obj = cv2.resize(img_obj, (width,height))
	img_res = os.path.join(res_path,os.path.basename(img))
	cv2.imwrite(img_res,resize_obj)
	print(img,'resize_fixed')


# 宽高指定比例缩放
def resize_scale(img,x_scale,y_scale):
	# 支持中文路径
	img_obj=cv2.imdecode(np.fromfile(img, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	print('Image Height,Width',img_obj.shape[0],img_obj.shape[1])
	resize_obj = cv2.resize(img_obj, None, fx = x_scale, fy = y_scale)
	img_res = os.path.join(res_path,os.path.basename(img))
	cv2.imwrite(img_res,resize_obj)
	print(img,'resize_scale')


def main():
	while True:
		if not file_list:
			break
		img_path = file_list.pop()
		resize_fixed(img_path,300,300)


if __name__ == '__main__':
	img_path = 'python6图'
	res_path = 'new'
	file_list = get_files(img_path,['.jpg','.png'])
	t_funs = []
	for i in range(5):
		 t = threading.Thread(target=main,args=())
		 t.setDaemon = True
		 t.start()
		 t_funs.append(t)
	for t in t_funs:
		t.join()
	print('end...')
