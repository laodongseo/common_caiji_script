# ‐*‐coding:utf‐8‐*‐
import os
"""
利用os.listdir递归获取所有的目录路径和文件路径
"""
def get_file_path(root_path, file_list, dir_list):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            # 递归获取所有文件和目录的路径
            get_file_path(dir_file_path, file_list, dir_list)
        else:
            file_list.append(dir_file_path)

            
 # 每个filename 不含路径    
def file_name(file_dir):
    File_Name=[]
    for files in os.listdir(file_dir):
        if os.path.splitext(files)[1] == '.txt':
            File_Name.append(files)
    return File_Name
txt_file_name=file_name(".")


if not os.path.isdir(path):  # 无文件夹时创建
#             os.makedirs(path)
#         if not os.path.isfile(filename):  # 无文件时创建
#             fd = open(filename, mode="w", encoding="utf-8")


