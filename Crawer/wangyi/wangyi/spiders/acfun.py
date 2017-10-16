# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request

from wangyi.items import AcfunItem


class AcfunSpider(Spider):
    name = "acfun"
    allowed_domains = ["acfun.cn"]
    start_urls = ['http://acfun.cn/']

    def start_requests(self):
        # 单个页面
        # url = 'http://www.acfun.cn/a/ac4026411'
        # yield Request(url, callback=self.parse)

        url = 'http://www.acfun.cn/v/list110/index_{}.htm'
        # maxindex = 22166
        for i in range(1, 50):
            yield Request(url.format(i), callback=self.parse_index)

    def parse(self, response):
        pass

    def parse_index(self, response):
        res = response.css('#block-content-article .mainer .item')
        for re in res:
            urlpart = re.css('.hint-comm-article::attr(href)').extract_first()
            yield Request(url='http://www.acfun.cn' + urlpart, callback=self.parse_page)

    def parse_page(self, response):
        item = AcfunItem()
        item['title'] = response.css('.txt-title-view_1::text').extract_first()
        item['time'] = response.css('#txt-info-title_1 .time::text').extract_first().lstrip('发布于 ')[:-6].replace(' ', '')

        res = response.css('#area-player p')
        # acfun文章页有很多空格需要去掉，因为通过选择器得到有多个空格组成的list，所以先把通过把
        # list变成str，然后用str.replace()去重，就得到比较少空格的多个字符串组成list
        # 最后再把list转为str
        content = []
        for re in res:
            text = re.css('::text').extract()
            texts = ' '.join(text)
            content.append(texts.replace(' ', '').replace('\xa0', ''))
        item['contents'] = ''.join(content)

        item['UP'] = response.css(
            '#block-info-bottom > div.block-info-bottom-r.l > div > span:nth-child(1) > a > nobr::text').extract_first()

        comment_url = 'http://www.acfun.cn/content_view.aspx?contentId={}&channelId=110'
        yield Request(url=comment_url.format(response.url[-7:]), meta={'key': item}, callback=self.parse_comment)

    def parse_comment(self, response):
        item = response.meta['key']
        jd = json.loads(response.text)
        item['onlook'] = jd[0]
        item['comments'] = jd[1]
        yield item