# -*- coding: utf-8 -*-
import sys
reload(sys)
import scrapy
import urllib
import re
import urlparse
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from companysearch.items import CompanysearchItem

sys.setdefaultencoding('utf-8')
class CompanySpider(scrapy.Spider):
    name = "companysearch"
    download_delay = 1
    allowed_domains = ["jobui.com"]
    start_urls = []

    def start_requests(self):
        #keywords = u'美光'.encode('utf-8')
        #additonkeyword = keywords+ '+'+ u"西安".encode('utf-8')
        #requesturl = "http://www.jobui.com/cmp?area=%E5%85%A8%E5%9B%BD&keyword={0}".format(urllib.quote(additonkeyword))
        file_object = open('company_name.txt','r')
        try:
              url_head = "http://www.jobui.com/cmp?area=%E5%85%A8%E5%9B%BD&keyword={0}+%E8%A5%BF%E5%AE%89"
              for line in file_object:
                  self.start_urls.append(url_head.format(urllib.quote(line)))
              for url in self.start_urls:
                  yield self.make_requests_from_url(url)
        finally:
              file_object.close()

    def parse(self, response):
        # '解析跳转到公司链接'
        #company_url = response.css('ul[class=companyList] li[class=atn-li] div[class=atn-content] h2[class=titTxt] span[class=fl] a :: attr(href)').extract_first(default='not-found')
        company_url = response.xpath('//ul[@class="companyList"]/li[@class="atn-li"]/div[@class="atn-content"]/h2/span[@class="fl"]/a/@href').extract_first(default='not-found')
        #html = response.xpath('/html/body/div').extract()
        #print(html)
        print(company_url)
        if (company_url != 'not-found') :
            yield scrapy.Request(urlparse.urljoin("http://www.jobui.com",company_url), meta={'dont_obey_robotstxt': True}, callback=self.parse_item)

    # 解析内容函数
    def parse_item(self, response):
        # '解析公司名称，公司信息，公司行业，公司介绍'
        companyname = response.xpath('//*[@id="companyH1"]/a/text()').extract()
        #print(companyname)
        #print("Company Name:" + companyname)
        info = response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[1]/text()').extract()
        #print("Company Info:" + info)
        industry = response.xpath('//*[@id="cmp-intro"]/div/div[2]/dl/dd[2]/a/text()').extract()
        #print("Company Industry:" + industry)
        introduction = response.xpath('//*[@id="textShowMore"]/text()').extract()
        #print("Company Introduction" + introduction)
        yield CompanysearchItem({
            'companyname': companyname,
            'info': info,
            'industry': industry,
            'introduction': introduction
        })