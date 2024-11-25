import requests
from lxml import etree

# 只能搜索左边的队伍
key = '伊普斯维奇'

url = f'https://www.zhibo8.com/schedule/finish_more.htm'
myheader = {'user-agent': 'Chrome'}
response = requests.get(url, headers=myheader)
response.encoding = 'utf-8'
html = response.content
element = etree.HTML(html)

# 搜索定位（取第一个）
span_elements = element.xpath('//li/span[@class="_teams"]')
for span in span_elements:
    team = span.text
    # print(team)
    if key in team:
        break

a_elements = span.xpath('../a')
for a in a_elements:
    url_jijin = a.get('href')
    url_luxiang = 'https://www.zhibo8.com' + \
        url_jijin.replace('jijin', 'luxiang')
    print(url_jijin)
    print(url_luxiang)

# https://www.zhibo8.com/zuqiu/2024/1030-match1448348v-luxiang.htm
