wb = Workbook()
title = ['问题ID','用户名','问题标题','问题描述','创建时间','总回答数','排序权重','问题状态','操作']
for filename in os.listdir(r'./'):
    name,ext = os.path.splitext(filename)
    if '.txt' == ext:
        city = name.split('-')[1]
        print(city)
        sheet = wb.create_sheet(city)
        sheet.append(title)
        for line in open(filename,'r',encoding='utf-8'):
            line = line.strip()
            line = line.split('\t')
            try:
                element = '=VALUE(INDIRECT("RC[-4]", FALSE))'
                line.append(element)
            except Exception as e:
                print(e)
            finally:
                sheet.append(line)
wb.save('all_question.xlsx')
