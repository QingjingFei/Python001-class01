# 使用requests爬取猫眼电影，使用BeautifulSoup解析网页

import requests
from bs4 import BeautifulSoup as bs


domain = 'https://maoyan.com'
myurl = domain + '/films?showType=3'

header = {}
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
header['user-agent'] = user_agent
cookies = dict(uuid='A5E2A980B84911EA80F64D80EBA969F77731BC6D4B3E4657B7A855BA15BAA616')

response = requests.get(myurl, headers=header, cookies=cookies)
print(f'返回码是: {response.status_code}')
# print(response.text)

# 使用BeautifulSoup解析网页
bs_info = bs(response.text, 'html.parser')
i = 0
urls = []
# 获取所有链接
for tag in bs_info.find_all('div', attrs={'class': 'channel-detail movie-item-title'}):
    # 获取前十的链接
    if i < 10:
        urls.append(domain+tag.find('a').get('href'))
        i += 1
print(urls)


# 请求电影详情页，提取电影信息
mylist = []
for url in urls:
    response = requests.get(url, headers=header, cookies=cookies)
    # print(response.text)
    bs_info = bs(response.text, 'html.parser')
    div = bs_info.find('div', attrs={'class': 'movie-brief-container'})
    # 电影名称
    film_name = div.find('h1', attrs={'class': 'name'}).text
    print(f'电影名称: {film_name}')
    # 电影类型
    types = [a.text for a in div.ul.find('li', attrs={'class': 'ellipsis'}).find_all('a')]
    film_type = '/'.join(t.strip() for t in types)
    print(f'电影类型: {film_type}')
    # 上映日期
    plan_date = div.find_all('li', attrs={'class': 'ellipsis'})[-1].text[0:10]
    print(f'上映日期: {plan_date}')

    movie = {}
    movie['电影名称'] = film_name
    movie['电影类型'] = film_type
    movie['上映日期'] = plan_date

    mylist.append(movie)
print(len(mylist))


# 序列化存储
import pandas as pd
movie1 = pd.DataFrame(data = mylist)
# windows需要使用gbk字符集
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)