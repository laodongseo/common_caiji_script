# --*--coding: utf-8 --*--
"""
指定起始页self.url
单线程翻页采集直到结束
"""
import requests
import re
from pyquery import PyQuery as pq
import time


class Tieba(object):

    def __init__(self,id,cookie):
        self.url = 'http://cms.5i5j.com/aax/index?1=1&city_id=1&status_id={0}&start_time=&end_time='.format(id)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Cookie':cookie
        }


    def get_data(self,url,retry=1):
        try:
            r = requests.get(url=url,headers=self.headers, timeout=5)
        except Exception as e:
            print('获取源码失败', url, e)
            if retry > 0:
                time.sleep(30)
                self.get_data(url, retry - 1)
        else:
            status = r.status_code
            if status == 200:
                html = r.text
                return html


    def parse_data(self,html):
        texts = []
        next_page = None
        if html and 'AdminLTE' in html:
            try:
                doc = pq(html)
                tr_list = doc('tbody tr').items()
            except Exception as e:
                print('未提取到信息', e)
            else:
                for tr in tr_list:
                    hang = []
                    tds = tr('td').items()
                    for td in tds:
                        text = td.text()
                        hang.append(text)
                    texts.append(hang)
            if '下一页' in html:
                page_a = doc('.pageSty a').eq(0)
                next_page = page_a.attr('href')
        return texts,next_page



    def save_data(self,texts):
        for hang in texts:
            str_text = '\t'.join(hang)
            f.write('{0}\n'.format(str_text))
            f.flush()


    def run(self):
        data = self.get_data(self.url)
        texts,next_link = self.parse_data(data)
        self.save_data(texts)
        while 1:
            if next_link:
                next_link = 'http://cms.5i5j.com' + next_link
                print(next_link)
                data = self.get_data(next_link)
                tie_links,next_link = self.parse_data(data)
                self.save_data(tie_links)
                time.sleep(3)
            else:
                break

if __name__ == '__main__':
    f = open('zhuanye-wenda.txt','w',encoding='utf-8')
    cookie_str = 'smidV2=20190801154444f4237e3acfad9b8108a4ba6def791e0e001248760ce2cb9e0; _ga=GA1.2.1797629563.1569735268; yfx_c_g_u_id_10000001=_ck19092913342814331937372675747; OUTFOX_SEARCH_USER_ID_NCOO=848036200.464548; yfx_c_g_u_id_10000124=_ck19102110590319054575787455158; yfx_c_g_u_id_10000079=_ck19103113490917929935504514178; yfx_f_l_v_t_10000124=f_t_1571626743841__r_t_1573180060453__v_t_1573197199966__r_c_4; _Jo0OQK=442063914DC1F542BFA181919E6677B919288738375A4A8634E287018665DDB8F99DD7532D721C13A1673339D1E5CE3F25140962C4C31C7691EFDB51BF485A6953280A0C92C42EF75FBD222BA71AF7573AAD222BA71AF7573AAA684330A52EF69D1GJ1Z1KA==; c=cyrVR4v6-1577932018444-eea7fc3b5406d-1754182029; _xid=kMksCRlH3rO1PQ9REZOv0oLAS%2B5ZllNADW%2Bx148cQU4FACTtQtJrOczRBYBEYCLgNCJpNwxk%2FY3mV6xWkmSpLw%3D%3D; _fmdata=O793Fy5IKiRViqccOICV5tKy%2BSVZg9UMyFiAHP08e8SUkHXoPnL3ozCp64QyLCANQ9PxUzYw7PWVIaW1AJsP7HYoCLLJx9OS7q0u5YFXE48%3D; gr_user_id=079673f0-99de-404d-9da2-7e0034b945e7; grwng_uid=1ff47588-1823-4595-83c3-65363000c8d2; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%221711b24aa13d5-025343fdbb19fc-3a365305-1296000-1711b24aa148cd%22%2C%22distinct_id%22%3A%224c2381cb-6cd5-4ba8-bc0b-fb1d5cf56b16%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22http%3A%2F%2Foa.bacic5i5j.com%2Fsys%2Fportal%2Fpage.jsp%22%7D%2C%22first_id%22%3A%221741e8afa953f3-04d2e9162d01a9-393e5809-1296000-1741e8afa969f1%22%7D; yfx_mr_n_10000001=baidu%3A%3Amarket_type_ocpc%3A%3A%3A%3Abaidu_ppc%3A%3A%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E4%25BF%25A1%25E6%2581%25AF58%25E5%2590%258C%25E5%259F%258E%25E7%25BD%2591%3A%3Awww.baidu.com%3A%3A123886290726%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25AB%259E%25E5%2593%2581%25E8%25AF%258D%3A%3A58-%25E4%25BF%25A1%25E6%2581%25AF%3A%3A36%3A%3Apmf_from_adv%3A%3Abj.5i5j.com%2F; yfx_mr_f_n_10000001=baidu%3A%3Amarket_type_ocpc%3A%3A%3A%3Abaidu_ppc%3A%3A%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E4%25BF%25A1%25E6%2581%25AF58%25E5%2590%258C%25E5%259F%258E%25E7%25BD%2591%3A%3Awww.baidu.com%3A%3A123886290726%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25AB%259E%25E5%2593%2581%25E8%25AF%258D%3A%3A58-%25E4%25BF%25A1%25E6%2581%25AF%3A%3A36%3A%3Apmf_from_adv%3A%3Abj.5i5j.com%2F; yfx_key_10000001=; ershoufang_BROWSES=500664698%2C501044001; qqmail_alias=dongzhiheng@5i5j.com; xiaoqu_BROWSES=13041%2C165526%2C59565%2C9041%2C2763%2C345556%2C8434%2C8544%2C338977%2C10363%2C13407%2C338869%2C6161%2C9006%2C347155%2C347158%2C351785%2C11881%2C9371%2C376054%2C439821%2C470415%2C98020%2C243200%2C424230%2C395456%2C401971%2C432177%2C387390%2C38%2C439289%2C348752%2C164794%2C338642%2C100000000005209%2C338940%2C11596%2C100000000005214%2C338855%2C402414%2C440703%2C1022002115223%2C473038%2C254446%2C100000000006107%2C1759%2C66220%2C9079%2C338981%2C100000000000176%2C100000000000452%2C100000000005289%2C467999%2C53361%2C359958%2C171200%2C468286%2C351729%2C311386%2C40977%2C13661%2C100000000004504%2C338698%2C100000000005236%2C100000000004300%2C100000000003151%2C2230%2C53287%2C239641%2C338829%2C12146%2C338770%2C321366%2C49060%2C290720%2C285521%2C164783%2C5603%2C338866%2C1024002109472%2C347733%2C100000000012519%2C100000000014339%2C100000000011277%2C100000000005484%2C100000000004100%2C50634%2C405770%2C354852%2C28643%2C406550%2C432297%2C338732%2C348219%2C1024002108900%2C102400247154%2C102400248553%2C1024002109488%2C348218%2C1024002109489%2C1024002109424%2C359512%2C12651%2C244120%2C338738%2C304606%2C291733%2C2603%2C1024002109491%2C63034%2C1024002109490%2C1024002109492%2C1024002109486%2C1024002109478; question_BROWSES=171076%2C171075%2C171081%2C901164%2C171085%2C171079%2C171086%2C894117; __TD_deviceId=50VPEJI0OI9SSF53; PHPSESSID=jeh6bhufqnhsq8vplpfril4g18; _gid=GA1.2.1403560004.1603331496; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1602814308,1603073323,1603243236,1603331497; yfx_f_l_v_t_10000001=f_t_1569735268428__r_t_1603331496078__v_t_1603333990167__r_c_224; yfx_f_l_v_t_10000079=f_t_1572500949793__r_t_1603333992579__v_t_1603333992579__r_c_74; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1603333993; _csrf-backend=51bb19f73e43a879961cf35fc4a160e42af89edb5e9fa88288e505227eecf54ca%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_csrf-backend%22%3Bi%3A1%3Bs%3A32%3A%22HHm4j13N3mo2hpeENC47DCZnrRR2afu9%22%3B%7D; PHPSESSID1=ST-478394-IuqLfceNafxvNP0NA5d0-sso1'
    tieba = Tieba(1,cookie_str)
    tieba.run()
    f.flush()
    f.close()
