
# coding: utf-8

# In[77]:


# 导入库文件
from lxml import etree
import requests, time, pymongo


# In[78]:


# 初始化数据库
client = pymongo.MongoClient('localhost', 27017)
house_info_db = client['house_info_db']
house_info_table = house_info_db['house_info_table']


# In[79]:


# 请求信息的配置
headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Content-Length': '310',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'ROUTEID=.lb7; JSESSIONID=9A71A6FA3E654127C1F00E289A672CDF.lb7; Hm_lvt_70e93e4ca4be30a221d21f76bb9dbdfa=1555566018,1555566756; Hm_lpvt_70e93e4ca4be30a221d21f76bb9dbdfa=1555566756',
    'Host': 'jjhygl.hzfc.gov.cn',
    'Origin': 'http://jjhygl.hzfc.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://jjhygl.hzfc.gov.cn/webty/gpfy/gpfySelectlist.jsp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

post_data = {
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
    'page': '1',
    'xqid': '0',
    'signid': 'ff80808166484c980166486b4e0b0023',
    'threshold': 'ff80808166484c980166486b4e0b0021',
    'salt': 'ff80808166484c980166486b4e0b0022',
    'nonce': '0',
    'hash': '0448c9b2298cc81d7e0b7a2ab77fcd9261f956537b0939664985b08a1bc4ce20',
}

request_url = 'http://jjhygl.hzfc.gov.cn/webty/WebFyAction_getGpxxSelectList.jspx'


# 获取页码信息
def get_page_numbers():
    # 发起请求
    response_data = requests.post(request_url, headers=headers, data=post_data)
    # 房源和页面信息在返回的json格式数据中
    pageinfo_html = etree.HTML(response_data.json()['pageinfo'])
    # 通过xpath定位页面数目元素
    pagenum = pageinfo_html.xpath('.//font[@class="color-blue09"]/text()')

    return pagenum[0]

# 分析每一页的数据，并存入数据库中
def get_house_info():

    # 发起请求分析数据结构
    response_data = requests.post(request_url, headers=headers, data=post_data)
    # 请求成功，正确获得数据
    if response_data.status_code == 200:
        for house_info in response_data.json()['list']:
            # 查看数据库中是否已经有盖房屋信息
            check_house_info = [i['fwtybh'] for i in house_info_table.find({'fwtybh': house_info['fwtybh']})]
            if house_info['fwtybh'] in check_house_info:
                print('*'*10, '该房源信息已经存在，不会再次存入数据库!', '*'*10)
                print(house_info)
            else:
                house_info_table.insert_one(house_info)
                print('='*10,'新增房源信息一条'.format(house_info), '='*10,)
                print(house_info)
    else:
        print('数据请求失败，返回状态码为：{}'.format(response_data.status_code))

total_page_nums = get_page_numbers()

while int(post_data['page']) <= int(total_page_nums):
    time.sleep(3)
    print('#'*10, '正在请求第{}页数据，共{}页'.format(post_data['page'], total_page_nums), '#'*10)

    get_house_info()

    page_count = int(post_data['page']) + 1
    post_data['page'] = str(page_count)

    print('#'*10, '数据请求完毕', '#'*10, )