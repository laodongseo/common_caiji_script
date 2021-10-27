def get_html(kwd,retry=1):
	try:
		r = requests.get(url=PostUrl,headers=headers,timeout=15)
	except Exception as e:
		print(f'{2-retry}error,{e},暂停60 s')
		time.sleep(60)
		if retry > 0:
			post_html(kwd,retry-1)
	else:
		page_source = r.text
		return page_source

 def post_html(kwd,retry=1):
	try:
		r = requests.get(url=PostUrl,headers=headers,data=dic_form,timeout=15)
	except Exception as e:
		print(f'{2-retry}error,{e},暂停60 s')
		time.sleep(60)
		if retry > 0:
			post_html(kwd,retry-1)
	else:
		page_source = r.text
		return page_source
