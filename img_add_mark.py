# -*- coding: utf-8 -*-
"""
普及：图片的坐标轴起点是左上角
按位置比例指定位置
给图片添加文字水印或者图片水印
"""
import os,shutil
from PIL import Image, ImageDraw, ImageFont
import threading


# 添加文字水印
def add_text_watermark(image_path, watermark_text, font_path, font_size, rotate_angle, w_percent,h_percent,outputpath):
	# 打开原始图片
	image = Image.open(image_path)
	width, height = image.size
	# print(width,height)
	start_coord = int(width * w_percent),int(height * h_percent)
	# print(start_coord)

	# 创建一个与原始图片大小相同的透明图层
	transparent = Image.new('RGBA', image.size, (255, 255, 255, 0))

	# 设置字体和大小
	font = ImageFont.truetype(font_path, font_size)

	# 在透明图层上绘制文字水印
	draw = ImageDraw.Draw(transparent)
	draw.text(start_coord, watermark_text, font=font, fill=(0, 0, 255, 20), anchor='mm')

	# 旋转透明图层
	transparent = transparent.rotate(rotate_angle, expand=1)

	# 将透明图层添加到原始图片上
	image.paste(transparent, (0, 0), transparent)

	# 保存添加了水印的图片
	image.save(outputpath)


def add_logo_watermark(input_image_path, output_image_path, watermark_image_path=None, position=(1, 1)):
	# 打开原始图片
	base_image = Image.open(input_image_path).convert("RGBA")

	# 添加图片水印
	if watermark_image_path is not None:
		watermark_image = Image.open(watermark_image_path).convert("RGBA")
		watermark_size = watermark_image.size
	else:
		raise ValueError("Watermark image or text must be provided")

	# 计算水印位置
	x = int((watermark_size[0]) * position[0])
	y = int((watermark_size[1]) * position[1])

	# 合并原始图片和水印图片
	base_image.paste(watermark_image, (x, y), mask=watermark_image)

	# 保存输出图片,RGBA模式不能保存为JPEG格式
	base_image = base_image.convert('RGB') if 'jpg' in output_image_path or 'jpeg' in output_image_path else base_image
	base_image.save(output_image_path)


# 添加文字水印
def func_text(directorys):
	for directory in directorys:
		for dirnow, sondirs, sonfiles in os.walk(directory):
			print(f'当前目录:{dirnow},包含子目录:{sondirs},包含文件:{len(sonfiles)}')
			newdir = dirnow + '_addtext'
			shutil.rmtree(newdir) if os.path.exists(newdir) else True
			os.mkdir(newdir) if not os.path.exists(newdir) else True
			for sonfile in sonfiles:
				thefile = os.path.join(dirnow,sonfile)
				textmark_dic={
				'image_path':thefile,
				'watermark_text':'自备百科知识\n如有侵权请联系删除',
				'font_path':r'C:\Windows\Fonts\simfang.ttf',
				'font_size':55,
				'rotate_angle':40,
				'w_percent':0.2, #水印文字结尾距离左上角的宽
				'h_percent':0.25, #水印文字结尾距离左上角的高
				'outputpath': os.path.join(newdir,sonfile)
				}
				add_text_watermark(**textmark_dic)

# 添加图片水印
def func_img(directorys):
	for directory in directorys:
		for dirnow, sondirs, sonfiles in os.walk(directory):
			print(f'当前目录:{dirnow},包含子目录:{sondirs},包含文件:{len(sonfiles)}')
			newdir = dirnow + '_addlogo' # 新的存储目录
			shutil.rmtree(newdir) if os.path.exists(newdir) else True
			os.mkdir(newdir) if not os.path.exists(newdir) else True
			for sonfile in sonfiles:
				thefile = os.path.join(dirnow,sonfile)
				dict_img = {
						'input_image_path':thefile,
						'output_image_path':os.path.join(newdir,os.path.basename(sonfile)),
						'watermark_image_path':logo_img,
						'position':(0.03,0.05)
						}
				add_logo_watermark(**dict_img)


if __name__ == '__main__':
	logo_img = 'sc_20231101140940.jpg' #图片logo
	# 指定初始目录
	directorys = ['seo']
	func_img(directorys)
