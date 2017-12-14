# -*- coding: utf-8 -*-

# Scrapy settings for sn_kaoxiang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import time
BOT_NAME = 'sn_kaoxiang'

SPIDER_MODULES = ['sn_kaoxiang.spiders']
NEWSPIDER_MODULE = 'sn_kaoxiang.spiders'
LIST_FAN = {'機':'机','獨':'独','唔':'不','轉':'转','燒':'烧','熱':'热','風':'风','環':'环','範':'范','圍':'围','時':'时','雙':'双','膽':'胆','質':'质','產':'产',
            '開':'开','門':'门','觀':'观','樣':'样'}

ROBOTSTXT_OBEY = False
suning_user_agent=[
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
FIELDS_TO_EXPORT = [
    'p_Name',
    'shop_name',
    'ProductID',
    'price',
    'PreferentialPrice',
    'CommentCount',
    'GoodRateShow',
    'GoodCount',
    'GeneralCount',
    'PoorCount',
    'keyword',
    'type',         #核心参数
    'brand',        #品牌
    'X_name',       #型号
    'control',      #控制方式
    'X_type',       #外观样式
    'capacity',     #容量
    'temp_con',     #温控方式
    'people',       #适用人数
    'function',     #特色功能
    'color',        #颜色
    'size',         #产品尺寸
    'open_type',    #开门方式
    'product_url',
    'source'
]
MONGO_HOST = "172.28.171.13"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "DKX"  # 库名
MONGO_COLL = "dkx_sn"  # 文档(相当于关系型数据库的表名)
DOWNLOAD_DELAY = 4
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'sn_kaoxiang.middlewares.SuningUseragentMiddleware':400,
    'sn_kaoxiang.middlewares.Exceptions':300,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware':True

}
RETRY_ENABLED=True
RETRY_TIMES=3
DOWNLOAD_TIMEOUT = 10
ITEM_PIPELINES = {
    'sn_kaoxiang.pipelines.CSVPipeline':200,
    'sn_kaoxiang.pipelines.MongoPipeline':190,

}
AUTOTHROTTLE_ENABLED = True
Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# LOG_FILE='苏宁电烤箱日志_%s.log' % Time
# LOG_STDOUT=True
