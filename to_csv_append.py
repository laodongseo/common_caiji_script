TodayCsvFile = f'{TodaySavePath}_1688_res_new.csv'
if IsHeader == 0:
	df_max_good.to_csv(TodayCsvFile,encoding='utf-8-sig',mode='w+',index=False)
	IsHeader = 1
else:
	df_max_good.to_csv(TodayCsvFile,encoding='utf-8-sig',mode='a+',index=False,header=False)
