'''
url = 'http://jjhygl.hzfc.gov.cn/webty/gpfy/gpfySelectlist.jsp'
api = 'http://jjhygl.hzfc.gov.cn/webty/WebFyAction_getGpxxSelectList.jspx'
'''

import requests, os, time
from bs4 import BeautifulSoup

# 杭州挂牌二手房api
api = 'http://jjhygl.hzfc.gov.cn/webty/WebFyAction_getGpxxSelectList.jspx'

# POST请求头信息和参数
headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Length': '310',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'ROUTEID=.lb3; Hm_lvt_70e93e4ca4be30a221d21f76bb9dbdfa=1540182828,1540294887; JSESSIONID=CB8381AB14EECCAC158B8575FC5FB711.lb3; Hm_lpvt_70e93e4ca4be30a221d21f76bb9dbdfa=1540433758',
    'Host': 'jjhygl.hzfc.gov.cn',
    'Origin': 'http://jjhygl.hzfc.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://jjhygl.hzfc.gov.cn/webty/gpfy/gpfySelectlist.jsp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
form_data = {
    'gply': '',
    'wtcsjg': '',
    'jzmj': '',
    'ordertype': '',
    'fwyt': '',
    'hxs': '',
    'havepic': '',
    'xzqh': '',
    'secondxzqh': '',
    'starttime': '',
    'endtime': '',
    'keywords': '',
    'page': '',
    'xqid': '0',
    'signid': 'ff80808166484c980166486b4e0b0023',
    'threshold': 'ff80808166484c980166486b4e0b0021',
    'salt': 'ff80808166484c980166486b4e0b0022',
    'nonce': '0',
    'hash': '0448c9b2298cc81d7e0b7a2ab77fcd9261f956537b0939664985b08a1bc4ce20',
}

# 获取当前页二手房信息
def get_currentpage_house_data(api, pages):
    index = 0
    while index < int(pages):
        time.sleep(10)
        from_data['page'] = str(index)
        dir_name = './page_' + form_data['page']
        os.mkdir(dir_name)
        print(dir_name+'creating dir successful.')

        # 获取当前页json响应数据
        r = requests.post(api, headers=headers, data=form_data)

        # 获取当前页面所有房源信息，并将每个房源信息生成独立文件保存
        house_data_list = r.json()['list']
        # 计数器
        count = 0
        for i in house_data_list:
            # 构建每个房源信息文件
            filename = dir_name + '/house_info_'+str(count)+'.txt'
            with open(filename, 'w') as f:
                # 遍历字典，写入数据到文件
                for key in i:
                    f.write(key + ':')
                    f.write(str(i[key])+'\n')
            print('fileNO: ' + str(count))
            count = count + 1
        index = index + 1

# 获取全部页码数和房源数
def get_total_pages_counts(api):
    # 获取当前页json响应数据
    r = requests.post(api, headers=headers, data=form_data)
    print(r.json()['pageinfo'])

    # 获取页码和总共房源数目信息
    total_info_html = r.json()['pageinfo']

    # 用BeautifulSoup解析html内容
    soup = BeautifulSoup(total_info_html, 'lxml')
    pages = soup.font.string
    # print(pages, soup.text)
    # print(soup.text.split(' '))
    # print(soup.text.split(' ')[-1].)
    return pages



pages = get_total_pages_counts(api)
# get_currentpage_house_data(api, pages)