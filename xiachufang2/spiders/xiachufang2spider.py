# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from xiachufang2.items import Xiachufang2Item
import hashlib
from scrapy.utils.python import to_bytes
from time import localtime


class Xiachufang2spider(CrawlSpider):
    name = 'xiachufang2spider'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/recipe/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item=Xiachufang2Item()

        s = response.xpath('//div[@class="steps"]/ol')[0]
        imgurl=s.xpath('//img/@src').extract()
        steps=response.xpath('//div[@class="steps"]/ol')[0].extract()
        item['image_urls']=imgurl

        for i in imgurl:
            steps=steps.replace(i,'{% static "pic/'+str(localtime().tm_year) + str(localtime().tm_mon)+'/'+hashlib.sha1(to_bytes(i)).hexdigest()+'.jpg" %}')
        item['steps']=steps

        item['tip']=response.xpath('//div[@class="tip"]/text()')[0].extract().replace('\n','').strip()
        item['description']=response.xpath('//div[@itemprop="description"]/text()')[0].extract().replace('\n','').strip()
        item['title']=response.xpath('//h1/text()')[0].extract().replace('\n','').strip()

        materials=response.xpath('//div[@class="ings"]/table/tr[@itemprop="recipeIngredient"]')
        m={}
        for i in materials:
            x=i.xpath('td[@class="name"]')[0].extract()
            y=i.xpath('td[@class="unit"]')[0].extract()
            x=rhtml(x).replace('\n','').strip()
            y=rhtml(y).replace('\n','').strip()
            m[x]=y
        item['stuff']=m

        if len(item['stuff'])<=0 or len(item['title'])<=0 or len(item['steps'])<=0:
            yield None
        else:
            yield item

def rhtml(string):
    t = string
    s=get(t,'<','>',cycle=1,include=1)
    if len(s)>0:
        for i in s:
            t=t.replace(i,'')
    return t

def get(string, begin, last, cycle=0, include=0):
    if type(string) == type(''):
        if cycle == 0:
            startpoint = string.find(begin)
            endpoint = startpoint + len(begin) + string[startpoint + len(begin):].find(last)
            if startpoint < 0 or endpoint < 0:  # 找不到开头或者结尾,直接返回
                print(u'首尾字符串找不到')
                return [string]
            if include == 0:
                return [string[startpoint + len(begin):endpoint]]
            else:
                return [begin + string[startpoint + len(begin):endpoint] + last]
        elif cycle == 1:
            records = []
            x = string
            while x.find(begin) >= 0:
                startpoint = x.find(begin)
                endpoint = startpoint + len(begin) + x[startpoint + len(begin):].find(last)
                if startpoint < 0 or endpoint < 0:  # 找不到开头或者结尾,直接返回
                    print(u'首尾字符串找不到')
                    return [string]
                if include == 0:
                    records.append(x[startpoint + len(begin):endpoint])
                else:
                    records.append(begin + x[startpoint + len(begin):endpoint] + last)
                x = x[endpoint + len(last):]
            return records
    else:
        return ['error:not string type']