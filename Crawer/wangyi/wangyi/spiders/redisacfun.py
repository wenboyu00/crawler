# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from wangyi.items import AcfunItem
from wangyi.spiders import SQL


class redisacfun(RedisCrawlSpider):
    name = "redisacfun"
    redis_key = 'redisacfun:start_urls'
    allowed_domains = ['www.acfun.cn']
    template = SQL.Sql.reach_Template("AcFun")
    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        super(redisacfun, self).__init__(*args, **kwargs)

    def parse(self, response):
        res = response.css('#block-content-article .mainer .item')
        for re in res:
            urlpart = re.css('.hint-comm-article::attr(href)').extract_first()
            yield Request(url='http://www.acfun.cn' + urlpart, callback=self.parse_page)

        url = 'http://www.acfun.cn/v/list110/index_{}.htm'
        # maxindex = 22166
        for i in range(1, 2):
            yield Request(url.format(i), callback=self.parse_index)

    def parse_index(self, response):
        res = response.css('#block-content-article .mainer .item')
        for re in res:
            urlpart = re.css('.hint-comm-article::attr(href)').extract_first()
            yield Request(url='http://www.acfun.cn' + urlpart, callback=self.parse_page)

    def parse_page(self, response):
        item = AcfunItem()
        item['title'] = response.css(self.template['Website_title']).extract_first()
        item['time'] = response.css(self.template['Website_pubtime']).extract_first().lstrip('发布于 ')[:-6].replace(' ', '')

        res = response.css(self.template['Website_content'])
        # acfun文章页有很多空格需要去掉，因为通过选择器得到有多个空格组成的list，所以先把通过把
        # list变成str，然后用str.replace()去重，就得到比较少空格的多个字符串组成list
        # 最后再把list转为str
        content = []
        for re in res:
            text = re.css('::text').extract()
            texts = ' '.join(text)
            content.append(texts.replace(' ', '').replace('\xa0', ''))
        item['contents'] = ''.join(content)

        item['UP'] = response.css(self.template['Website_author']).extract_first()

        comment_url = 'http://www.acfun.cn/content_view.aspx?contentId={}&channelId=110'
        yield Request(url=comment_url.format(response.url[-7:]), meta={'key': item}, callback=self.parse_comment)

    def parse_comment(self, response):
        item = response.meta['key']
        jd = json.loads(response.text)
        item['onlook'] = jd[0]
        item['comments'] = jd[1]
        yield item