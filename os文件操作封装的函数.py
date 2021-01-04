# ‐*‐coding:utf‐8‐*‐
import os

# 利用os.listdir递归获取所有的目录路径和文件路径
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
            
            
# 获取某个目录下的特定文件(含路径,非递归),ext为文件后缀(带点)
def get_files(file_path,ext):
    file_list = []
    dir_or_files = os.listdir(file_path)
    # dir_or_file纯文件名+后缀,不带路径
    for dir_or_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(file_path, dir_or_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            pass
        else:
            if os.path.splitext(dir_file_path)[-1] == ext:
                file_list.append(dir_file_path)
    return file_list

            
 # 结果里每个filename 是不含路径的    
def file_name(file_dir):
    File_Name=[]
    for files in os.listdir(file_dir):
        if os.path.splitext(files)[1] == '.txt':
            File_Name.append(files)
    return File_Name
txt_file_name=file_name(".")


# 清空文件夹
def clear_path(filepath):
    if os.path.exists(filepath):
        for i in os.listdir(filepath):
            path_file = os.path.join(filepath, i)
            if os.path.isfile(path_file):
                os.remove(path_file)
            elif os.path.isdir(path_file):
                shutil.rmtree(path_file)
            else:
                pass
            
            
if not os.path.isdir(path):  # 无文件夹时创建
#             os.makedirs(path)
#         if not os.path.isfile(filename):  # 无文件时创建
#             fd = open(filename, mode="w", encoding="utf-8")


