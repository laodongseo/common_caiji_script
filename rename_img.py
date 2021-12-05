# -*- coding:utf-8 -*-
"""

重命名图片文件,删除文件名的中文
"""
import os
import re


# 获取某目录下的特定文件(含路径),ext为后缀(带点)
def get_files(file_path, ext='.jpg'):
    file_list = []
    dir_or_files = os.listdir(file_path)
    for dir_or_file in dir_or_files:
        # 添加路径
        dir_file_path = os.path.join(file_path, dir_or_file)
        # 保留文件,去除文件夹
        if not os.path.isdir(dir_file_path):
            if os.path.splitext(dir_file_path)[-1] == ext:
                file_list.append(dir_file_path)
    return file_list


def img_rename(imgfile):
    fname= os.path.basename(imgfile)
    fname_new = re.sub('^((?!(\*|//)).)+[\u4e00-\u9fa5]','',fname)
    newfile = os.path.join(Newpath,fname_new)
    # 如果存在则删除原文件
    if os.path.exists(newfile):
        os.remove(newfile)
    os.rename(imgfile,newfile)


if __name__ == '__main__':
    Oldpath = './old_img'
    Newpath = './imgfile'
    img_files = get_files(Oldpath)
    for img_file in img_files:
        img_rename(img_file)
