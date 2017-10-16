# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
import re

from wangyi.items import NewItem


class SinaSpider(Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://sina.com/']

    def start_requests(self):
        url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1505353908881'
        for i in range(1, 30):  # 抓取多个列表的页面
            yield Request(url=url.format(i), callback=self.parse_links)

    def parse_links(self, response):
        res = response.text.lstrip('  newsloadercallback(').rstrip(');')
        jd = json.loads(res)
        for x in (jd['result']['data']):
            print(x['url'])  # 从字典中得到url
            yield Request(url=x['url'], callback=self.parse_new)

    def parse(self, response):
        pass

    def parse_new(self, response):
        item = NewItem()  # 定义储存item
        title = response.css('#artibodyTitle::text').extract_first()  # 标题
        if title == None:
            yield Request(response.url, callback=self.parse_othernews, dont_filter=True)
        else:
            # 正文
            texts = []
            text = ''
            for p in response.css('#artibody p::text').extract()[:-1]:
                texts.append(p.strip())
                text = ''.join(texts)

            # 新闻源
            try:
                source = response.css('.time-source span a::text').extract_first()
            except:
                print('Source ERROR,Source parser changed')
                source = response.css('.time-source span:text').extract_first()

            # 编辑人
            editor = response.css('.article-editor::text').extract_first().lstrip('责任编辑： ').strip()
            # 时间
            time = response.css('.time-source::text').extract_first().strip()

            # 评论url
            # 用正则表达式从正文连接中得到信息，m.group取出id
            m = re.search('doc-i(.*).shtml', response.url)
            id = m.group(1)
            commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
            item['title'] = title
            item['contents'] = text
            item['source'] = source
            item['editor'] = editor
            item['time'] = time[0:11]
            # 评论
            yield Request(url=commenturl.format(id), meta={'key': item}, callback=self.parse_comment, dont_filter=True)

    def parse_comment(self, response):
        item = response.meta['key']
        # 得到内容为取出多余字符，带入到js中。
        jd = json.loads(response.text.strip('var data='))
        try:
            item['comment'] = jd['result']['count']['total']
        except:
            item['comment'] = None
        yield item

    def parse_othernews(self, response):
        item = NewItem()
        # 标题
        item['title'] = response.xpath('//*[@id="main_title"]/text()').extract_first()
        # 正文
        texts = []
        text = ''

        for p in response.xpath('//div[@id="artibody"]/p/text()').extract():
            texts.append(p.strip())
            text = ''.join(texts)
        item['contents'] = text

        # 新闻源
        source = response.xpath('//*[@id="page-tools"]/span/span[2]/text()').extract_first()
        if source == None:
            item['source'] = response.xpath('//div[@id="page-tools"]/span/span[2]/a/text()').extract_first()
        else:
            item['source'] = source

        # 时间
        time = response.xpath('//*[@id="page-tools"]/span/span[1]/text()').extract_first()
        item['time'] = time[0:11]
        # 评论
        m = re.search('doc-i(.*).shtml', response.url)
        id = m.group(1)
        commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=jc&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
        yield Request(url=commenturl.format(id), meta={'key': item}, callback=self.parse_comment, dont_filter=True)