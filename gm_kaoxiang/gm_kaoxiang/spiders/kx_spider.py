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
        if len(response.text)<80000:
            yield scrapy.Request(url=response.request.url,callback=self.page_detail,dont_filter=True)
            time.sleep(2)
            print('网页加载不完整！')
            return None
        for each in response.xpath(".//div[@class='item-tab-warp']"):
            # print(each)
            product_urlm=each.xpath(".//p[@class='item-name']/a/@href").extract()[0]
            product_url='http:'+product_urlm
            print(product_url)
            item=GmKaoxiangItem(product_url=product_url)
            yield scrapy.Request(url=product_url,meta={'item':item},callback=self.product_detail,dont_filter=True)
    def product_detail(self,response):
        item=response.meta['item']
        product_url=item['product_url']
        if len(response.text)<65000:
            yield scrapy.Request(url=product_url,callback=self.product_detail,dont_filter=True,meta=response.meta)
            return None
        #商品名称
        # 商品集合页查询商品名称，店铺名称，商品详情页url
        try:
            p_Name = re.findall("prdName:'(.*?)'", response.text)[0]
        except:
            try:
                p_Name = re.findall('title="(.*?)"', response.text)[0]
            except:
                try:
                    p_Name = re.findall(' <h1>(.*?)</h1>', response.text)[0]
                except:
                    try:
                        p_Name = re.findall('商品名称：(.*?)</div>', response.text)[0]
                    except:
                        p_Name = None
        # print(p_Name)
        #店铺名称
        try:
            shop_name=response.xpath(".//div[@class='zy-stores shops-name']/a[@class='name']/text()").extract()[0]
        except:
            try:
                shop_name=response.xpath(".//h2[@id='store_live800_wrap']/a[@class='name']/text()").extract()[0]
            except:
                try:
                    shop_name=response.xpath(".//div[@class='zy-stores shops-name']/span[@class='identify']/text()").extract()[0]
                except:
                    shop_name=None
        # print(shop_name)
        #ProductID商品ID
        try:
            ProductID = Selector(response).re('prdId:"(.*?)"')[0]
        except:
            try:
                ProductID = re.findall('prdId:"(.*?)"', response.text)[0]
            except:
                try:
                    ProductID = re.findall('prdId:"(.*?)"', response.text)[0]
                except:
                    ProductID = response.url.split('/')[-1].split('-')[0]
        # print(ProductID)
        # 价格类代码重写
        try:
            Price = re.findall('price:"(.*?)"', response.text)
            gomeprice = re.findall('gomePrice:"(.*?)"', response.text)
            groupprice = re.findall('groupPrice:"(.*?)"', response.text)
            oldprice = re.findall('<span id="listPrice">(.*?)</span>', response.text)
            if Price:
                if Price[0] == '0':
                    price = gomeprice[0]
                    PreferentialPrice = gomeprice[0]
                else:
                    if float(Price[0]) < float(gomeprice[0]):
                        price = gomeprice[0]
                        PreferentialPrice = Price[0]
                    else:
                        price = Price[0]
                        PreferentialPrice = gomeprice[0]
            else:
                if float(oldprice[0]) < float(groupprice[0]):
                    price = groupprice[0]
                    PreferentialPrice = oldprice[0]
                else:
                    price = oldprice[0]
                    PreferentialPrice = groupprice[0]
            if float(price) < float(PreferentialPrice):
                print('错误！！！')
        except:
            price = None
            PreferentialPrice = None
        # print(price)
        # print(PreferentialPrice)
        # 品牌
        try:
            brand = Selector(response).re('品牌：(.*?)</div>')[0]
        except:
            try:
                brand = re.findall('品牌：(.*?)</div>', response.text)[0]
            except:
                brand = None
        if brand:
            if re.findall(r'（.*?）', brand):
                re_com = re.compile('（.*?）')
                brand = brand[:0] + re.sub(re_com, '', brand)
        if brand:
            if re.findall(r'(.*?)', brand):
                re_cn = re.compile('\(.*?\)')
                brand = brand[:0] + re.sub(re_cn, '', brand)
        # print(brand)
        # 品牌型号
        try:
            X_name = Selector(response).re('型号：(.*?)</div>')[0]
        except:
            try:
                X_name = re.findall('型号：(.*?)</div>', response.text)[0]
            except:
                try:
                    X_name = Selector(response).re('型号</span><span>(.*?)</span>')[0]
                except:
                    try:
                        X_name = re.findall('型号</span><span>(.*?)</span>', response.text)[0]
                    except:
                        X_name = None
        if X_name:
            if brand:
                if brand in X_name:
                    X_name=re.sub(brand,'',X_name)
                else:
                    pass
        # print(X_name)
        # 颜色
        try:
            color = Selector(response).re('颜色</span><span>(.*?)</span>')[0]
        except:
            try:
                color = re.findall('颜色</span><span>(.*?)</span>', response.text)[0]
            except:
                color = None
        # print(color)
        #控制方式
        try:
            control=Selector(response).re('控制方式：(.*?)</div>')[0]
        except:
            try:
                control=Selector(response).re('控制方式</span><span>(.*?)</span>')[0]
            except:
                try:
                    control=re.findall('控制方式：(.*?)</div>',response.text)[0]
                except:
                    try:
                        control=re.findall('控制方式</span><span>(.*?)</span>',response.text)[0]
                    except:
                        control=None
        # print(control)
        #外观样式
        try:
            X_type=Selector(response).re('外观样式：(.*?)</div>')[0]
        except:
            try:
                X_type=Selector(response).re('外观样式</span><span>(.*?)</span>')[0]
            except:
                try:
                    X_type=re.findall('外观样式：(.*?)</div>',response.text)[0]
                except:
                    try:
                        X_type=re.findall('外观样式</span><span>(.*?)</span>',response.text)[0]
                    except:
                        X_type=None
        # print(X_type)
        #容量
        try:
            capacity=Selector(response).re('实际容量：(.*?)</div>')[0]
        except:
            try:
                capacity=Selector(response).re('实际容量</span><span>(.*?)</span>')[0]
            except:
                try:
                    capacity=re.findall('实际容量：(.*?)</div>',response.text)[0]
                except:
                    try:
                        capacity=re.findall('实际容量</span><span>(.*?)</span>',response.text)[0]
                    except:
                        capacity=None
        # print(capacity)
        #温控方式
        try:
            temp_con=Selector(response).re('加热方式：(.*?)</div>')[0]
        except:
            try:
                temp_con=Selector(response).re('加热方式</span><span>(.*?)</span>')[0]
            except:
                try:
                    temp_con=re.findall('加热方式：(.*?)</div>',response.text)[0]
                except:
                    try:
                        temp_con=re.findall('加热方式</span><span>(.*?)</span>',response.text)[0]
                    except:
                        temp_con=None
        # print(temp_con)
        #特色功能
        try:
            function=Selector(response).re('定时功能：(.*?)</div>')[0]
        except:
            try:
                function=Selector(response).re('定时功能</span><span>(.*?)</span>')[0]
            except:
                try:
                    function=re.findall('定时功能：(.*?)</div>',response.text)[0]
                except:
                    try:
                        function=re.findall('定时功能</span><span>(.*?)</span>',response.text)[0]
                    except:
                        function=None
        if function:
            if '定时功能' in function:
                pass
            else:
                function='定时功能:'+function[:]
        # print(function)
        try:
            size=Selector(response).re('产品尺寸.*?</span><span>(.*?)</span></li>')[0]
        except:
            try:
                size=re.findall('产品尺寸.*?</span><span>(.*?)</span></li>',response.text)[0]
            except:
                try:
                    size=Selector(response).re('产品.*?尺寸</span><span>(.*?)</span></li>')[0]
                except:
                    try:
                        size=re.findall('产品.*?尺寸</span><span>(.*?)</span></li>',response.text)[0]
                    except:
                        size=None
        # print(size)
        #开门方式
        try:
            open_type=Selector(response).re('开门方式：(.*?)</div>')[0]
        except:
            try:
                open_type=Selector(response).re('开门方式</span><span>(.*?)</span>')[0]
            except:
                try:
                    open_type=re.findall('开门方式：(.*?)</div>',response.text)[0]
                except:
                    try:
                        open_type=re.findall('开门方式</span><span>(.*?)</span>',response.text)[0]
                    except:
                        open_type=None
        # print(open_type)
        # 好评，差评等信息采集
        comment_url = 'http://ss.gome.com.cn/item/v1/prdevajsonp/appraiseNew/%s/1/all/0/10/flag/appraise' % ProductID
        mark_url = 'http://ss.gome.com.cn/item/v1/prdevajsonp/productEvaComm/%s/flag/appraise/totleMarks?callback=totleMarks' % ProductID
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        with Session() as gome:
            # 建立会话对象
            gome.mount('http://', request_retry)
            gome.mount('https://', request_retry)
            gome.headers = headers
            comment_text = gome.get(url=comment_url).text
            time.sleep(0.3)
            mark_text = gome.get(url=mark_url).text
        # 访问comment_url
        try:
            # 好评
            GoodCount = re.findall('"good":(.*?),', comment_text)[0]
        except:
            GoodCount = None
            # 中评
        try:
            GeneralCount = re.findall('"mid":(.*?),', comment_text)[0]
        except:
            GeneralCount = None
            # 差评
        try:
            PoorCount = re.findall('"bad":(.*?),', comment_text)[0]
        except:
            PoorCount = None
            # 总评
        try:
            CommentCount = re.findall('"totalCount":(.*?),', comment_text)[0]
        except:
            CommentCount = None
        # 访问评论关键字
        # 好评度
        try:
            GoodRateShow = re.findall(r'"goodCommentPercent":(\d+)', mark_text)[0]
        except:
            try:
                GoodRateShow = re.findall(r'"good":(\d+),', mark_text)[0]
            except:
                GoodRateShow = None
        try:
            keyword = '"'
            word_list = re.findall('"recocontent":"(.*?)"', mark_text)
            for each in word_list:
                if '?' in each:
                    word_list.remove(each)
            if word_list:
                for every in word_list:
                    keyword = keyword[:] + every
                    if every != word_list[-1]:
                        keyword = keyword[:] + ' '
                    if every == word_list[-1]:
                        keyword = keyword[:] + '"'
            if len(keyword) <= 1:
                print(1 / 0)
        except:
            keyword = None
        #核心参数，如若获取不到
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            parameter = []
            div_item = soup.find_all('div', class_='param-item')
            for each in div_item:
                li_list = each.find_all('li')
                for each in li_list:
                    li_text = re.sub(r'\n', '', each.text)
                    parameter.append(li_text)
            if len(parameter) < 1:
                print(1 / 0)
        except:
            try:
                parameter = []
                div_item = soup.find('div', class_='guigecanshu_wrap')
                div_canshu = div_item.find_all('div', class_='guigecanshu')
                for each in div_canshu:
                    parameter.append(each.text)
                if len(parameter) < 1:
                    print(1 / 0)
            except:  # 针对真划算页面的type参数分析
                try:
                    parameter = []
                    table = soup.find('table', attrs={'class': 'grd-specbox'})
                    tr_list = table.find_all('tr')
                    for each in tr_list:
                        if each.find('td'):
                            td = each.find_all('td')
                            if td:
                                td1 = re.sub(r'\n', '', td[0].text)
                                td2 = re.sub(r'\n', '', td[1].text)
                                parameter.append(td1 + ':' + td2)
                                # print(td1 + ':' + td2)
                    print(parameter)
                    if len(parameter) < 1:
                        print(1 / 0)
                except:
                    parameter = None
        # 将核心参数转化为字符串形式
        try:
            if parameter == None:
                type = None
            else:
                type = '"'
                for i in range(len(parameter)):
                    type = type[:] + parameter[i]
                    if i < len(parameter) - 1:
                        type = type[:] + ' '
                    if i == len(parameter) - 1:
                        type = type[:] + '"'
        except:
            type = None
        print(type)
        if type:
            if brand==None:
                try:
                    brand=re.findall('品牌:(.*?) ',type)[0]
                except:
                    brand=None
            if brand:
                if re.findall(r'（.*?）', brand):
                    re_com = re.compile('（.*?）')
                    brand = brand[:0] + re.sub(re_com, '', brand)
            if brand:
                if re.findall(r'(.*?)', brand):
                    re_cn = re.compile('\(.*?\)')
                    brand = brand[:0] + re.sub(re_cn, '', brand)
            if X_name==None:
                try:
                    X_name=re.findall('型号:(.*?) ',type)[0]
                except:
                    X_name=None
            if X_name:
                if brand:
                    if brand in X_name:
                        X_name = re.sub(brand, '', X_name)
                    else:
                        pass
            if color==None:
                try:
                    color=re.findall('颜色:(.*?) ',type)[0]
                except:
                    color=None
            if control==None:
                try:
                    control=re.findall('控制方式:(.*?) ',type)[0]
                except:
                    control=None
            if X_type==None:
                try:
                    X_type=re.findall('外观样式:(.*?) ',type)[0]
                except:
                    X_type=None
            if capacity==None:
                try:
                    capacity=re.findall('容量:(.*?) ',type)[0]
                except:
                    capacity=None
            if temp_con==None:
                try:
                    temp_con=re.findall('加热方式:(.*?) ',type)[0]
                except:
                    temp_con=None
            if function==None:
                try:
                    function=re.findall('定时功能:(.*?) ',type)[0]
                except:
                    function=None
            if function:
                function='定时功能:'+function[:]
            if size==None:
                try:
                    size=re.findall('产品尺寸.*?:(.*?) ',type)[0]
                except:
                    try:
                        size=re.findall('产品.*?尺寸:(.*?)',type)[0]
                    except:
                        size=None
            if open_type==None:
                try:
                    open_type=re.findall('开门方式:(.*?) ',type)[0]
                except:
                    open_type=None
        people=None
        source='国美'
        item['p_Name']=p_Name
        item['shop_name'] = shop_name
        item['ProductID'] = ProductID
        item['price'] = price
        item['PreferentialPrice'] = PreferentialPrice
        item['CommentCount'] = CommentCount
        item['GoodRateShow'] = GoodRateShow
        item['GoodCount'] = GoodCount
        item['GeneralCount'] = GeneralCount
        item['PoorCount'] = PoorCount
        item['keyword'] = keyword
        item['type'] = type
        item['brand'] = brand
        item['X_name'] = X_name
        item['control'] = control
        item['X_type'] = X_type
        item['capacity'] = capacity
        item['temp_con'] = temp_con
        item['people'] = people
        item['function'] = function
        item['color'] = color
        item['size'] = size
        item['open_type'] = open_type
        item['source'] = source
        yield item