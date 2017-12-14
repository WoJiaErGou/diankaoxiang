import scrapy
from scrapy import Selector
import requests
from requests import Session
import re
from gm_kaoxiang.items import GmKaoxiangItem
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
class SN_DKXspider(scrapy.Spider):
    name = 'gm_DKX'
    start_urls=['http://list.gome.com.cn/cat10000208.html?intcmp=sy-1000053150_1']
    #数量400+，页面9
    def parse(self, response):
        try:
            numbers=re.findall('TotalNumber">(\d+)</em> 个商品</span>',response.text)[0]
            print('一共有%s个商品！' % numbers)
        except:
            pass
        pages=re.findall('totalPage.+:(\d+),',response.text)[0]
        print('一共有%s页！' % pages)
        for i in range(1,int(pages)+1):
            page_url='http://list.gome.com.cn/cat10000208-00-0-48-1-0-0-0-1-0-0-0-0-0-0-0-0-0.html?&page=%d' % i
            yield scrapy.Request(url=page_url,callback=self.page_detail,dont_filter=True)
    def page_detail(self,response):
        # print(len(response.text))
        if len(response.text)<80000:
            time.sleep(2)
            yield scrapy.Request(url=response.request.url,callback=self.page_detail,dont_filter=True)
            return None
        for each in response.xpath(".//div[@class='item-tab-warp']"):
            # print(each)
            product_urlm=each.xpath(".//p[@class='item-name']/a/@href").extract()[0]
            product_url='http:'+product_urlm
            print(product_url)
            item=GmKaoxiangItem(product_url=product_url)
            yield item