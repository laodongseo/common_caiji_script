# -*- coding: utf-8 -*-
"""
目录下的图片上传到七牛云空间

"""

from qiniu import Auth, put_file, etag
import qiniu.config
import os   
import threading,traceback


# 获取某个目录下的特定文件(含路径,非递归),ext为文件后缀(带点)
def get_files(file_path,ext):
	file_list = []
	dir_or_files = os.listdir(file_path)
	# dir_or_file纯文件名+后缀,不带路径
	for dir_or_file in dir_or_files:
		# 给目录或者文件添加路径
		dir_file_path = os.path.join(file_path, dir_or_file)
		# 判断该路径为文件还是路径
		if not os.path.isdir(dir_file_path):
			if os.path.splitext(dir_file_path)[-1] == ext:
				file_list.append(dir_file_path)
	return file_list


def main():
	global up_num
	while True:
		if not file_list:
			break
		localfile = file_list.pop()
		upniu_img = f'{Img_File}/{os.path.basename(localfile)}'
		print(upniu_img)
		#生成上传 Token，可以指定过期时间等
		up_token = q.upload_token(bucket_name, upniu_img, 3600)
		try:
			ret,info = put_file(up_token, upniu_img, localfile, version='v2')
			if ret['key'] == upniu_img and ret['hash'] == etag(localfile):
				print(f'success:{up_num}')
				up_num += 1
		except Exception as e:
			traceback.print_exc()
			file_list.append(localfile)






if __name__ == "__main__":
	up_num = 1
	Img_File = 'myimg4'
	file_list = get_files(Img_File,'.jpg')
	print(len(file_list))
	#需要填写你的 Access Key 和 Secret Key
	access_key = 'xxxx'
	secret_key = 'yyyy'
	#要上传的空间
	bucket_name = '-----'
	#构建鉴权对象
	q = Auth(access_key, secret_key)

	for i in range(30):
		t = threading.Thread(target=main)
		t.setDaemon(False)
		t.start()
