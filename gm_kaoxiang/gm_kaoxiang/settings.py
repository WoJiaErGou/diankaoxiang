# -*- coding: utf-8 -*-

# Scrapy settings for gm_kaoxiang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import time
BOT_NAME = 'gm_kaoxiang'

SPIDER_MODULES = ['gm_kaoxiang.spiders']
NEWSPIDER_MODULE = 'gm_kaoxiang.spiders'
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 6
AUTOTHROTTLE_ENABLED = True
RETRY_ENABLED=True
RETRY_TIMES=5
GM_user_agent=[
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
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
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]
#注意修改内容
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'gm_kaoxiang.middlewares.GM_user':400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware':True

}
MONGO_HOST = "172.28.171.13"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "DKX"  # 库名
MONGO_COLL = "dkx_gm"  # 文档(相当于关系型数据库的表名)
ITEM_PIPELINES = {
    'gm_kaoxiang.pipelines.CSVPipeline':200,
    'gm_kaoxiang.pipelines.MongoPipeline':190,
}
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
#存储文件
# Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# LOG_FILE='国美电饭煲日志_%s.log' % Time
# LOG_STDOUT=True