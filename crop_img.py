# -*- coding: utf-8 -*-
"""
按比例裁剪图片
"""

import pandas as pd  
import time
import cv2
import numpy as np
import os,shutil


def  cropped_img(imgpath,w_scale,h_scale,newimgpath):
	img = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), cv2.IMREAD_COLOR)
	h, w = img.shape[:2]
	if (h,w) != (720,960):
		h_scale,w_scale = 1,1
	new_h = int(h * h_scale)
	new_w = int(w * w_scale)

	# 确定裁剪区域的左上角坐标
	x1 = (w - new_w) // 2
	y1 = (h - new_h) // 2

	# 确定裁剪区域的右下角坐标
	x2 = x1 + new_w
	y2 = y1 + new_h

	# 获取裁剪区域的图像
	cropped_img = img[y1:y2, x1:x2]

	cv2.imwrite(newimgpath, cropped_img)



if __name__ == "__main__":
	# 指定目录
	directorys = 'imgsz'.split(',')
	for directory in directorys:
		for dirnow, sondirs, sonfiles in os.walk(directory):
			print(f'当前目录:{dirnow},包含子目录:{sondirs},包含文件:{len(sonfiles)}')
			newdir = dirnow + '_crop' # 新的存储目录
			shutil.rmtree(newdir) if os.path.exists(newdir) else True
			os.mkdir(newdir) if not os.path.exists(newdir) else True

			for file in sonfiles:
				thefile = os.path.join(dirnow,file)
				dict_img = {
				'imgpath':thefile,
				'w_scale':0.45,
				'h_scale':1,
				'newimgpath':os.path.join(newdir,file)
				}

				cropped_img(**dict_img)
