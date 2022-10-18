# ‐*‐ coding: utf‐8 ‐*‐
"""
读取某文件夹内的txt文件
合并为excel
"""
import pandas as pd
import os
import xlsxwriter


# 获取某目录下的特定文件(含路径),ext为文件后缀(带点)
def get_files(file_path, ext):
	file_list = []
	dir_or_files = os.listdir(file_path)
	# dir_or_file不带路径
	for dir_or_file in dir_or_files:
		# 添加路径
		dir_file_path = os.path.join(file_path, dir_or_file)
		# 保留文件,去除文件夹
		if not os.path.isdir(dir_file_path):
			if os.path.splitext(dir_file_path)[-1] == ext:
				file_list.append(dir_file_path)
	return file_list


def main():
	txt_files = get_files(TxtPath,'.txt')
	df_all = pd.DataFrame()
	with pd.ExcelWriter('_txt合并.xlsx',engine='xlsxwriter',engine_kwargs={"options":{'strings_to_urls': False}}) as writer:
		for txt_file in txt_files:
			type_name = os.path.splitext(os.path.basename(txt_file))[0]
			df = pd.read_csv(txt_file,sep='\t',names=Columns)
			df['分类'] = type_name
			df_all = df_all.append(df)
		df_all.dropna().drop_duplicates().to_excel(writer,index=False)


if __name__ == "__main__":
	TxtPath = './url文件'
	# 表头
	Columns = ['title','url']
	main()
