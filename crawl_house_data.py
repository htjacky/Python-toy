# craw house data from LianJia/AnJuKe/FangTianXia
# LianJia https://blog.csdn.net/haohaixingyun/article/details/51839956
#         https://www.linchun.com.cn/technic/634.html
# FangTianXia https://blog.csdn.net/yiranhwj/article/details/52680536
#             https://zhuanlan.zhihu.com/p/25713752
# AnJuKe https://segmentfault.com/a/1190000013932818

#class house_spider(object):
#    def

from bs4 import BeautifulSoup

import re
import urllib
import urllib.request
import math
import codecs
import pandas as pd
import numpy as np

import view_house

lj_domain='http://sh.lianjia.com/'
lj_house_url = lj_domain + 'ershoufang/pudong/'
se_file='se.xls'
num_per_page = 30.0
down_price = 100
up_price = 600

def get_all_community_list():
    df = pd.read_excel(se_file, 'Sheet1', usecols=[6])
    df = df.drop_duplicates()
    np_data = np.array(df)
    all_commu_list = np_data.tolist()
    print(all_commu_list)
    return all_commu_list


def getHouseInfo(house_soup, h_list, comm_name):
    for tag in  house_soup.find('ul',class_='sellListContent').find_all('div', class_="info"):
        href        = tag.find('a').get('href')
        title       = tag.find('a').string
        addr_commu  = tag.find('div',class_="houseInfo").a.string
        addr_info   = tag.find('div',class_="houseInfo").a.next_sibling
        floor       = tag.find('div',class_="flood").find('div',class_="positionInfo").span.next_sibling
        area        = tag.find('div',class_="flood").find('div',class_="positionInfo").a.string
        total_price = tag.find('div',class_="totalPrice").span.string + \
                tag.find('div',class_="totalPrice").span.next_sibling
        unit_price  = tag.find('div',class_="unitPrice").span.string
        house_info  = [href, title, addr_commu, addr_info, total_price, unit_price]
        #if addr_commu == comm_name:
        if addr_commu.find(comm_name) != -1:
            print('%s is %s, Add:\n%s\n' %(addr_commu, comm_name, house_info))
            h_list.append(house_info)
        else:
            print('%s is not %s, just skip:\n%s\n' %(addr_commu, comm_name, house_info))


def getHouseInfoForOneCommu(community, house_list):
    #house_list=[]
    house_num = 0
    #comm_url=r'http://sh.lianjia.com/ershoufang/lc2lc1bp200ep400rs潍坊二村/'
    comm_str = str(community).strip('[]')
    comm_str = comm_str.strip('\'')
    comm_url = lj_house_url + 'lc2lc1bp' + str(down_price) + 'ep' + str(up_price) + 'rs' \
        + urllib.parse.quote(comm_str)
    print(comm_url)
    #comm_url = comm_url.encode('utf-8')
    try:
        xiao_html_doc = urllib.request.urlopen(comm_url).read()
        xiaoqu_soup = BeautifulSoup(xiao_html_doc, 'html.parser')
        house_num=int(xiaoqu_soup.find("h2",class_="total fl").find('span').string)
    except:
        print("search %s failed!\n" %comm_str)
        return house_list

    print(house_num)

    if house_num == 0:
        print('no house found')
        return house_list

    if house_num > 100:
        print('100+ house in %s found, maybe the address is wrong!!!\n' %comm_str)
        return house_list
    
    #house_list.append(getHouseInfo(xiaoqu_soup))
    view_house.show_house_info(comm_str, house_num)
    getHouseInfo(xiaoqu_soup,house_list,comm_str)

    total_page = math.ceil(house_num / num_per_page)
    for page_index in range(2, int(total_page)+1):
        #page_url= '%s%d' % ('http://bj.lianjia.com/ershoufang/changying/p',page_index)
        page_url = lj_house_url + 'pg' + str(page_index) + 'lc2lc1bp' + str(down_price) \
            + 'ep' + str(up_price) + 'rs' + urllib.parse.quote(comm_str)
        page_html_doc= urllib.request.urlopen(page_url).read()
        page_soup = BeautifulSoup(page_html_doc, 'html.parser')
        #print page_url
        #house_list.append(getHouseInfo(page_soup))
        getHouseInfo(page_soup,house_list,comm_str)
    return house_list

community_list = get_all_community_list()
all_house_data = []
for community in community_list:
    getHouseInfoForOneCommu(community, all_house_data)

house_df = pd.DataFrame(all_house_data)
house_df.to_excel('lianjia_house_info.xls')
