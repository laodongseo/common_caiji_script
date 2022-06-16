# ‐*‐coding:utf‐8‐*‐
import os

# 获取纯文件名|不含后缀
basename = os.path.basename(excel_file)
fname = os.path.splitext(basename)[0]


os.path.abspath(path)：获取目标位置的绝对路径
os.path.exists(path)：判断目标是否存在
os.path.isdir(path)：判断目标是否是目录
os.path.isfile(path)：判断目标是目录还是文件
os.walk(path)：遍历指定目录下的所有子文件夹和子文件夹中的所有文件
os.listdir()：返回指定路径下所有的文件和文件夹列表,但是子目录下文件不遍历


os.path.join()：将分离的部分合成一个整体
filename=os.path.join('/home/ubuntu/python_code','split_func') ：输出为：/home/ubuntu/python_code/split_func

os.path.basename(file)  返回文件名(去除路径 包含后缀)
os.path.splitext() 分割文件的路径(带有文件名) 和扩展名
fname,fename=os.path.splitext('/home/ubuntu/python_code/split_func/split_function.py')
#输出为：/home/ubuntu/python_code/split_func/split_function   .py

os.path.split（）分割文件的路径 和文件名(带后缀)
dirname,filename=os.path.split('/home/ubuntu/python_code/split_func/split_function.py')
# /home/ubuntu/python_code/split_func     split_function.py

# shutil库
shutil.move(src, dst)：把文件移动到指定位置


# os.listdir递归获取所有的目录和文件(含路径)
def get_file_path(root_path, file_list, dir_list):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 添加目录或者文件的路径
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
        # 给目录或者文件添加路径
        dir_file_path = os.path.join(file_path, dir_or_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            pass
        else:
            if os.path.splitext(dir_file_path)[-1] == ext:
                file_list.append(dir_file_path)
    return file_list

            
# 结果里每个filename不含路径含后缀  
def get_file_namess(file_path,ext):
    file_names=[]
    for files in os.listdir(file_path):
        if os.path.splitext(files)[1] == ext:
            file_names.append(files)
    return file_names
file_names=get_file_namess("./",'.txt')


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


