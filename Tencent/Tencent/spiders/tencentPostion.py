# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentpostionSpider(scrapy.Spider):
    name = 'tencentPostion'
    allowed_domains = ['tencent.com']
    base_url = 'http://hr.tencent.com/position.php?&start='
    offset = 0

    #起始url
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for each in node_list:
			#初始化模型
            item = TencentItem()

            item['positionName'] = each.xpath("./td[1]/a/text()").extract()[0]

            item['positionLink'] = each.xpath("./td[1]/a/@href").extract()[0]

            if len(each.xpath("./td[2]/text()")) != 0:
                item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            else :
                item['positionType'] = ""

            item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]

            item['workLoction'] = each.xpath("./td[4]/text()").extract()[0]

            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]

            yield item

            # if self.offset < 3830:
            #     self.offset += 10
            #     url = self.base_url + str(self.offset)
        #
        if len(response.xpath("//a[@id='next' and calss='noactive']")) == 0:
            next_url = self.base_url + str(response.xpath("//a[@id='next']/@href"))
            yield scrapy.Request(next_url,callback = self.parse)