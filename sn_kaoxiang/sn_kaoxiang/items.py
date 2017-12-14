# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnKaoxiangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_Name = scrapy.Field()
    shop_name = scrapy.Field()
    ProductID = scrapy.Field()
    price = scrapy.Field()
    PreferentialPrice = scrapy.Field()
    CommentCount = scrapy.Field()
    GoodRateShow = scrapy.Field()
    GoodCount = scrapy.Field()
    GeneralCount = scrapy.Field()
    PoorCount = scrapy.Field()
    keyword = scrapy.Field()
    # 核心参数
    type = scrapy.Field()
    # 品牌
    brand = scrapy.Field()
    # 型号
    X_name = scrapy.Field()
    # 控制方式
    control = scrapy.Field()
    # 外观样式
    X_type = scrapy.Field()
    # 容量
    capacity = scrapy.Field()
    # 温控方式
    temp_con = scrapy.Field()
    # 适用人数
    people = scrapy.Field()
    # 特色功能
    function = scrapy.Field()
    # 颜色
    color = scrapy.Field()
    # 产品尺寸
    size = scrapy.Field()
    # 开门方式
    open_type = scrapy.Field()
    source = scrapy.Field()
    ##不用存储的字段
    urlID = scrapy.Field()
    product_url = scrapy.Field()
