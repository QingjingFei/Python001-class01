# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
from scrapy.selector import Selector


class MaoyanmovieSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'maoyanmovie'
    allowed_domains = ['maoyan.com']
    # 起始URL列表
    start_urls = ['https://maoyan.com/films?showType=3']

    # 注释默认的parse函数
    # def parse(self, response):
    #     pass

    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        url = f'https://maoyan.com/films?showType=3'
        cookies = {
            'uuid': 'A5E2A980B84911EA80F64D80EBA969F77731BC6D4B3E4657B7A855BA15BAA616'
        }
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse, dont_filter=False)

    # 解析函数
    def parse(self, response):
        # 打印网页的url
        print(f'url: {response.url}')
        # # 打印网页的内容
        # print('------------------------------------------')
        # print(response.text)
        movies = Selector(response=response).xpath('.//div[@class="channel-detail movie-item-title"]')
        i = 0
        # 获取前十的电影link
        for movie in movies:
            if i < 10:
                # 在items.py定义
                item = SpidersItem()
                link = 'https://maoyan.com' + movie.xpath('./a/@href').extract_first()
                title = movie.xpath('./a/text()').extract_first()
                print('---------------------------')
                print(f'详情页: {link}')
                item['title'] = title
                print(f'电影名称: {title}')

                i += 1
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    # 解析具体页面
    def parse2(self, response):
        item = response.meta['item']
        infos = Selector(response=response).xpath('.//div[@class="movie-brief-container"]/ul')
        genres = infos.xpath('./li[1]/a')
        genre = '/'.join(
            genre.xpath('./text()').extract_first().strip() for genre in genres
            )
        date = infos.xpath('./li[3]/text()').extract_first()[0:10]

        print(f'电影类型: {genre}')
        print(f'上映日期: {date}')
        item['genre'] = genre
        item['date'] = date

        yield item

