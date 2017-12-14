import scrapy
from scrapy import Selector
import requests
from requests import Session
import re
from sn_kaoxiang.items import SnKaoxiangItem
import json
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from sn_kaoxiang.settings import LIST_FAN
class Snkaox_spider(scrapy.Spider):
    name = 'sn_DKX'
    start_urls = ['https://list.suning.com/0-20336-0.html']
    def parse(self, response):
        '''
                信息条数为1000+
        '''
        max_page = response.xpath(".//div[@id='filter-results']/div[@id='bottom_pager']/span[@class='page-more']/text()").extract()[0]
        results = response.xpath(".//span[@class='total-result']/strong[@id='totalNum']/text()").extract()[0]
        max_number = re.findall('共(.*?)页', max_page)[0]
        print('苏宁电饭煲搜索结果页面为' + max_number + '页')
        print('电饭煲一共有' + results + '个')
        for i in range(0,int(max_number)):
            page_url='https://list.suning.com/0-20336-%d.html' % i
            print(page_url)
            yield scrapy.Request(url=page_url,callback=self.page_detail,dont_filter=True)
            # break
    def page_detail(self,response):
        # print(len(response.text))
        if len(response.text)<100000:
            yield scrapy.Request(url=response.request.url,callback=self.page_detail,dont_filter=True)
            print('网页内容不完整！')
            return None
        for number in response.xpath(".//div[@class='wrap']"):
            product_urlm=number.xpath(".//div[@class='res-info']/p[@class='sell-point']/a/@href").extract()[0]
            # print(product_urlm)
            # 商品的url提取
            product_url = "https:" + product_urlm[:]
            # 商品名称与之前不同，以列表得到，转化为字符串
            may_name_list = number.xpath(".//p[@class='sell-point']/a/text()").extract()
            p_Name = ''
            for each in may_name_list:
                p_Name = p_Name[:] + each
                if each != p_Name[-1]:
                    p_Name = p_Name[:] + ' '
            p_Name = re.sub(r'\n', '', p_Name)
            if '' == p_Name[-1]:
                p_Name = p_Name[:-2]
            print(p_Name)
            # 店铺名称
            shop_name = number.xpath(".//p[4]/@salesname").extract()[0]
            print(shop_name)
            # 产品ID
            ProductID = product_urlm.split('/')[-1].split('.')[0]
            # 对应商品详情页的请求ID
            urlID = product_urlm.split('/')[-2]
            # 实例化item
            # url='https://www.google.com.hk/'
            item = SnKaoxiangItem(ProductID=ProductID, urlID=urlID, p_Name=p_Name, shop_name=shop_name,product_url=product_url)
            request = scrapy.Request(url=product_url, callback=self.product_detail, meta={'item': item},dont_filter=True)
            yield request
    def product_detail(self,response):
        item = response.meta['item']
        ProductID = item['ProductID']
        urlID = item['urlID']
        product_url=item['product_url']
        # print(len(response.text))
        if len(response.text)<90000:
            yield scrapy.Request(url=product_url,callback=self.product_detail,meta=response.meta,dont_filter=True)
            return None
        response_text=response.text
        for key,value in LIST_FAN.items():
            response_text=re.sub(key,value,response_text)
        # 品牌
        try:
            brand = Selector(response).re('"brandName":"(.*?)"')[0]
        except:
            try:
                brand = Selector(response).re('品牌</span>.*?target="_blank">美的(Midea)</a>')[0]
            except:
                try:
                    brand = re.findall('"brandName":"(.*?)"', response_text)[0]
                except:
                    brand = None
        # 去掉品牌括号内容
        if brand:
            if re.findall(r'（.*?）', brand):
                re_com = re.compile('（.*?）')
                brand = brand[:0] + re.sub(re_com, '', brand)
        if brand:
            if re.findall(r'\(.*?\)', brand):
                re_cn = re.compile('\(.*?\)')
                brand = brand[:0] + re.sub(re_cn, '', brand)
        # 容量
        try:
            capacity = Selector(response).re('容量：(.*?)</li>')[0]
        except:
            try:
                capacity = Selector(response).re('容量</.*?val">(.*?)</td>')[0]
            except:
                try:
                    capacity = re.findall('容量：(.*?)</li>', response_text)[0]
                except:
                    try:
                        capacity=re.findall('容量</.*?val">(.*?)</td>',response_text)[0]
                    except:
                        capacity = None
        # 颜色
        try:
            color = Selector(response).re('颜色：(.*?)</li>')[0]
        except:
            try:
                color = Selector(response).re('颜色</span>.*?class="val">(.*?)</td>')[0]
            except:
                try:
                    color = re.findall('颜色：(.*?)</li>', response_text)[0]
                except:
                    color = None
        # 类型，商品型号
        try:
            X_name = Selector(response).re('型号</span> </div> </td> <td class="val">(.*?)</td>')[0]
        except:
            try:
                X_name = re.findall('型号</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                if X_name == None:
                    X_name = re.findall('型号</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
            except:
                X_name = None
        if X_name:
            if brand:
                if brand in X_name:
                    X_name=re.sub(brand,'',X_name)
                else:
                    pass
        if X_name:
            if re.findall(r'（.*?）', X_name):
                re_com = re.compile('（.*?）')
                X_name = X_name[:0] + re.sub(re_com, '', X_name)
        if X_name:
            if re.findall(r'\(.*?\)', X_name):
                re_cn = re.compile('\(.*?\)')
                X_name = X_name[:0] + re.sub(re_cn, '', X_name)
        # 控制方式
        try:
            control = Selector(response).re('控制方式：(.*?)</li>')[0]
        except:
            try:
                control = Selector(response).re('控制方式</.*?val">(.*?)</td>')[0]
            except:
                try:
                    control = re.findall('控制方式：(.*?)</li>', response_text)[0]
                except:
                    try:
                        control=re.findall('控制方式</.*?val">(.*?)</td>',response_text)[0]
                    except:
                        try:
                            control=re.findall('控制方法：(.*?)</li>', response_text)[0]
                        except:
                            try:
                                control=re.findall('控制方法</.*?val">(.*?)</td>',response_text)[0]
                            except:
                                control = None
        # 外观样式
        try:
            X_type = Selector(response).re('外观式样：(.*?)</li>')[0]
        except:
            try:
                X_type = Selector(response).re('外观式样</.*?val">(.*?)</td>')[0]
            except:
                try:
                    X_type = re.findall('外观式样：(.*?)</li>', response_text)[0]
                except:
                    try:
                        X_type = re.findall('外观式样</.*?val">(.*?)</td>', response_text)[0]
                    except:
                        X_type = None
        # 温度控制方式(普通加热，上下独立控温，热风循环，旋转烧烤，旋转烤叉)
        #普通加热
        try:
            pt = re.findall('普通加热：(.*?)</li>', response_text)[0]
        except:
            try:
                pt = re.findall('普通加热</.*?val">(.*?)</td>', response_text)[0]
            except:
                pt = None
        if pt:
            pt='普通加热:'+pt[:]
        #上下独立控温
        try:
            sxdl = Selector(response).re('上下独立控温：(.*?)</li>')[0]
        except:
            try:
                sxdl = Selector(response).re('上下独立控温</.*?val">(.*?)</td>')[0]
            except:
                try:
                    sxdl = re.findall('上下独立控温：(.*?)</li>', response_text)[0]
                except:
                    try:
                        sxdl = re.findall('上下独立控温</.*?val">(.*?)</td>', response_text)[0]
                    except:
                        sxdl = None
        if sxdl:
            sxdl='上下独立控温:'+sxdl
        #热风循环
        try:
            rfxh = Selector(response).re('热风.*?循环：(.*?)</li>')[0]
        except:
            try:
                rfxh = Selector(response).re('热风.*?循环</.*?val">(.*?)</td>')[0]
            except:
                try:
                    rfxh = re.findall('热风.*?循环：(.*?)</li>', response_text)[0]
                except:
                    try:
                        rfxh = re.findall('热风.*?循环</.*?val">(.*?)</td>', response_text)[0]
                    except:
                        rfxh = None
        if rfxh:
            rfxh='热风循环:'+rfxh
        #旋转烧烤
        try:
            xzsk = Selector(response).re('旋转烧烤：(.*?)</li>')[0]
        except:
            try:
                xzsk = Selector(response).re('旋转烧烤</.*?val">(.*?)</td>')[0]
            except:
                try:
                    xzsk = re.findall('旋转烧烤：(.*?)</li>', response_text)[0]
                except:
                    try:
                        xzsk = re.findall('旋转烧烤</.*?val">(.*?)</td>', response_text)[0]
                    except:
                        xzsk = None
        if xzsk:
            xzsk='旋转烧烤:'+xzsk
        #旋转烤叉
        try:
            xzkc = Selector(response).re('旋转烤叉：(.*?)</li>')[0]
        except:
            try:
                xzkc = Selector(response).re('旋转烤叉</.*?val">(.*?)</td>')[0]
            except:
                try:
                    xzkc = re.findall('旋转烤叉：(.*?)</li>', response_text)[0]
                except:
                    try:
                        xzkc = re.findall('旋转烤叉</.*?val">(.*?)</td>', response_text)[0]
                    except:
                        xzkc = None
        if xzkc:
            xzkc='旋转烤叉:'+xzkc
        temp_con = '"'
        if pt or sxdl or rfxh or xzsk or xzkc:
            if pt:
                temp_con=temp_con[:]+pt
            if sxdl:
                temp_con=temp_con[:]+' '+sxdl
            if rfxh:
                temp_con=temp_con[:]+' '+rfxh
            if xzsk:
                temp_con=temp_con[:]+' '+xzsk
            if xzkc:
                temp_con=temp_con[:]+' '+xzkc
        if len(temp_con)<2:
            temp_con=None
        print(temp_con)
        # 特色功能
        #背部热风
        try:
            bbrf = Selector(response).re('背部热风</.*?val">(.*?)</td>')[0]
        except:
            try:
                bbrf = re.findall('背部热风</.*?val">(.*?)</td>', response_text)[0]
            except:
                bbrf = None
        if bbrf:
            bbrf='背部热风:'+bbrf
        #童锁功能
        try:
            tsgn = Selector(response).re('童锁功能</.*?val">(.*?)</td>')[0]
        except:
            try:
                tsgn = re.findall('童锁功能</.*?val">(.*?)</td>', response_text)[0]
            except:
                tsgn = None
        if tsgn:
            tsgn='童锁功能:'+tsgn
        function='"'
        if bbrf or tsgn:
            if bbrf:
                function=function[:]+bbrf
            if tsgn:
                function=function[:]+' '+tsgn
        if len(function)<2:
            function=None
        #尺寸大小
        try:
            size = Selector(response).re('产品尺寸.*?</.*?val">(.*?)</td>')[0]
        except:
            try:
                size = re.findall('产品尺寸.*?</.*?val">(.*?)</td>', response_text)[0]
            except:
                size = None
        #开门方式
        try:
            open_type = Selector(response).re('开门方式</.*?val">(.*?)</td>')[0]
        except:
            try:
                open_type = re.findall('开门方式.*?</.*?val">(.*?)</td>', response_text)[0]
            except:
                open_type = None
        #核心参数
        type = '"'
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            ul = soup.find('ul', attrs={'class': 'cnt clearfix'})
            li = ul.find_all('li')
            for i in range(len(li)):
                type = type[:] + li[i].text
                if i < len(li) - 1:
                    type = type[:] + ' '
                if i == len(li) - 1:
                    type = type[:] + '"'
        except:
            try:  # 部分核心参数格式更改
                div = soup.find('div', class_='prod-detail-container')
                ul = div.find('ul', attrs={'class': 'clearfix'})
                li = ul.find_all('li')
                for each in li:
                    li_li = each.find_all('li')
                    for i in range(len(li_li)):
                        type = type[:] + li_li[i].text
                        if i < len(li_li) - 1:
                            type = type[:] + ' '
                        if i == len(li_li) - 1:
                            type = type[:] + '"'
            except:
                type = None
        if type:
            if len(type)<2:
                type=None
        if type == None:
            try:
                parameter_id = Selector(response).re('"mainPartNumber":"(.*?)"')[0]
            except:
                try:
                    parameter_id = re.findall('"mainPartNumber":"(.*?)"', response_text)[0]
                except:
                    parameter_id = None
                    type = None
            if parameter_id:
                try:
                    parameter_id = Selector(response).re('"mainPartNumber":"(.*?)"')[0]
                    parameter_url = 'https://product.suning.com/pds-web/ajax/itemParameter_%s_R0105002_10051.html' % parameter_id
                    para_response = requests.get(parameter_url).text
                    time.sleep(1)
                    for key, value in LIST_FAN.items():
                        para_response = re.sub(key, value, para_response)
                    eles = re.findall('"snparameterdesc":"(.*?)"', para_response)
                    souls = re.findall('"snparameterVal":"(.*?)"', para_response)
                    try:
                        type = '"'
                        for i in range(len(eles)):
                            type = type[:] + eles[i] + ':' + souls[i]
                            if i < len(eles) - 1:
                                type = type[:] + ' '
                            if i == len(eles) - 1:
                                type = type[:] + '"'
                            if len(type)<2:
                                type=None
                    except:
                        type = None
                    if brand == None:
                        try:
                            brand = re.findall('"snparameterdesc":"品牌","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            brand = None
                    if capacity==None:
                        try:
                            capacity = re.findall('"snparameterdesc":"容量","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            capacity = None
                    #型号
                    if X_name==None:
                        try:
                            X_name = re.findall('"snparameterdesc":"型号","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            X_name = None
                        if X_name:
                            if brand:
                                if brand in X_name:
                                    X_name=re.sub(brand,'',X_name)
                                else:
                                    X_name = brand + X_name[:]
                        if X_name:
                            if re.findall(r'（.*?）', X_name):
                                re_com = re.compile('（.*?）')
                                X_name = X_name[:0] + re.sub(re_com, '', X_name)
                        if X_name:
                            if re.findall(r'\(.*?\)', X_name):
                                re_cn = re.compile('\(.*?\)')
                                X_name = X_name[:0] + re.sub(re_cn, '', X_name)
                        # print(X_name)
                    #控温方式
                    if temp_con==None:
                        try:
                            pt = re.findall('"snparameterdesc":"普通加热","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            pt = None
                        try:
                            sxdl = re.findall('"snparameterdesc":"上下独立控温","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            sxdl = None
                        try:
                            rfxh = re.findall('"snparameterdesc":"热风.*?循环","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            rfxh = None
                        try:
                            xzsk = re.findall('"snparameterdesc":"旋转烧烤","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            xzsk = None
                        try:
                            xzkc = re.findall('"snparameterdesc":"旋转烤叉","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            xzkc = None
                        temp_con = '"'
                        if pt or sxdl or rfxh or xzsk or xzkc:
                            if pt:
                                temp_con = temp_con[:] + pt
                            if sxdl:
                                temp_con = temp_con[:] + ' ' + sxdl
                            if rfxh:
                                temp_con = temp_con[:] + ' ' + rfxh
                            if xzsk:
                                temp_con = temp_con[:] + ' ' + xzsk
                            if xzkc:
                                temp_con = temp_con[:] + ' ' + xzkc
                        if len(temp_con) < 2:
                            temp_con = None
                    if function==None:
                        try:
                            bbrf = re.findall('"snparameterdesc":"背部热风","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            bbrf = None
                        try:
                            tsgn = re.findall('"snparameterdesc":"童锁功能","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            tsgn = None
                        function = '"'
                        if bbrf or tsgn:
                            if bbrf:
                                function = function[:] + bbrf
                            if tsgn:
                                function = function[:] + ' ' + tsgn
                        if len(function) < 2:
                            function = None
                    if color==None:
                        try:
                            color = re.findall('"snparameterdesc":"颜色","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            color = None
                    if size==None:
                        try:
                            size = re.findall('"snparameterdesc":"产品尺寸.*?","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            size = None
                    if open_type==None:
                        try:
                            open_type = re.findall('"snparameterdesc":"开门方式","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            open_type = None
                except:
                    pass
        # 获取相关请求url
        keyword_url = 'https://review.suning.com/ajax/getreview_labels/general-000000000' + ProductID + '-' + urlID + '-----commodityrLabels.htm'
        comment_url = 'https://review.suning.com/ajax/review_satisfy/general-000000000' + ProductID + '-' + urlID + '-----satisfy.htm'
        price_url = 'https://pas.suning.com/nspcsale_0_000000000' + ProductID + '_000000000' + ProductID + '_' + urlID + '_10_010_0100101_20268_1000000_9017_10106_Z001.html'
        # 获取印象关键字
        try:
            keyword_response = requests.get(keyword_url).text
            keyword_text = json.loads(re.findall(r'\((.*?)\)', keyword_response)[0])
            keyword_list = keyword_text.get('commodityLabelCountList')
            key_str = '"'
            keyword = []
            for i in range(len(keyword_list)):
                key_str = key_str[:] + keyword_list[i].get('labelName')
                if i < len(keyword_list) - 1:
                    key_str = key_str[:] + ' '
                if i == len(keyword_list) - 1:
                    key_str = key_str[:] + '"'
            keyword.append(key_str)
        except:
            keyword = None
        # 获取评价信息
        try:
            comment_response = requests.get(comment_url).text
            comment_text = json.loads(re.findall(r'\((.*?)\)', comment_response)[0])
            comment_list = comment_text.get('reviewCounts')[0]
            # 差评
            PoorCount = comment_list.get('oneStarCount')
            twoStarCount = comment_list.get('twoStarCount')
            threeStarCount = comment_list.get('threeStarCount')
            fourStarCount = comment_list.get('fourStarCount')
            fiveStarCount = comment_list.get('fiveStarCount')
            # 评论数量
            CommentCount = comment_list.get('totalCount')
            # 好评
            GoodCount = fourStarCount + fiveStarCount
            # 中评
            GeneralCount = twoStarCount + threeStarCount
            # 好评度
            # 得到百分比取整函数
            if CommentCount != 0:
                goodpercent = round(GoodCount / CommentCount * 100)
                generalpercent = round(GeneralCount / CommentCount * 100)
                poorpercent = round(PoorCount / CommentCount * 100)
                commentlist = [GoodCount, GeneralCount, PoorCount]
                percent_list = [goodpercent, generalpercent, poorpercent]
                # 对不满百分之一的判定
                for i in range(len(percent_list)):
                    if percent_list[i] == 0 and commentlist[i] != 0 and CommentCount != 0:
                        percent_list[i] = 1
                nomaxpercent = 0  # 定义为累计不是最大百分比数值
                # 好评度计算url='http://res.suning.cn/project/review/js/reviewAll.js?v=20170823001'
                if CommentCount != 0:
                    maxpercent = max(goodpercent, generalpercent, poorpercent)
                    for each in percent_list:
                        if maxpercent != each:
                            nomaxpercent += each
                    GoodRateShow = 100 - nomaxpercent
                else:
                    GoodRateShow = 100
            else:
                PoorCount = 0
                CommentCount = 0
                GoodCount = 0
                GeneralCount = 0
                GoodRateShow = 100
        except:
            PoorCount = 0
            CommentCount = 0
            GoodCount = 0
            GeneralCount = 0
            GoodRateShow = 100
        # 有关价格
        try:
            price_response = requests.get(price_url).text
        except requests.RequestException as e:
            # print(e)
            time.sleep(2)
            s = requests.session()
            s.keep_alive = False
            s.mount('https://', HTTPAdapter(max_retries=5))
            price_response = s.get(price_url).text
        if len(price_response) > 900:
            try:
                price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                if len(price) < 1:
                    price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                if price:
                    if float(price) < float(PreferentialPrice):
                        tt = price
                        price = PreferentialPrice
                        PreferentialPrice = tt
            except:
                price = None
                PreferentialPrice = None
        else:
            time.sleep(3)
            price_response = requests.get(price_url).text
            if len(price_response) > 900:
                try:
                    price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                    PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                    if len(price) < 1:
                        price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                    if price:
                        if float(price) < float(PreferentialPrice):
                            tt = price
                            price = PreferentialPrice
                            PreferentialPrice = tt
                except:
                    price = None
                    PreferentialPrice = None
            else:
                # 作出失败判断并将url归入重试
                price_response = self.retry_price(price_url)
                if len(price_response) > 500:
                    try:
                        price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                        PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                        if len(price) < 1:
                            price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                        if price:
                            if float(price) < float(PreferentialPrice):
                                tt = price
                                price = PreferentialPrice
                                PreferentialPrice = tt
                    except:
                        price = None
                        PreferentialPrice = None
                else:
                    PreferentialPrice = None
                    price = None
        # 防止出现多个字段出现为空
        if capacity==None and control==None and type==None:
            yield None
        else:
            source = '苏宁'
            people=None
            item['X_name'] = X_name
            item['type'] = type
            item['X_type'] = X_type
            item['price'] = price
            item['PreferentialPrice'] = PreferentialPrice
            item['brand'] = brand
            item['keyword'] = keyword
            item['PoorCount'] = PoorCount
            item['CommentCount'] = CommentCount
            item['GoodCount'] = GoodCount
            item['GeneralCount'] = GeneralCount
            item['GoodRateShow'] = GoodRateShow
            item['capacity'] = capacity
            item['color'] = color
            item['source'] = source
            item['control']=control
            item['people'] = people
            item['temp_con'] = temp_con
            item['function'] = function
            item['size'] = size
            item['open_type'] = open_type
            yield item
    def retry_price(self,price_url):
        price_response_may = requests.get(price_url)
        time.sleep(5)
        price_response=price_response_may.text
        return price_response