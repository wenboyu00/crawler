# -*- coding: utf-8 -*-
import re
from scrapy import Request
import json
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from wangyi.items import NewItem
from wangyi.spiders import SQL


class redis163(RedisCrawlSpider):
    name = "redis163"
    redis_key = 'redis163:start_urls'
    template = SQL.Sql.reach_Template("网易新闻")

    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        super(redis163, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 单个页面
        # url = 'http://news.163.com/photoview/00AP0001/2278034.html#p=D0BQBL2300AP0001NOS'
        # yield Request(url)

        # 要闻url
        # yw_url = 'http://temp.163.com/special/00804KVA/cm_yaowen.js'
        # yield Request(url=yw_url, callback=self.parse_index)
        yw_urls = 'http://temp.163.com/special/00804KVA/cm_yaowen_{}.js'
        for i in range(2, 5):
            n = str(i)
            s = n.zfill(2)
            yield Request(url=yw_urls.format(s), callback=self.parse_index)

            # # 社会url
            # sh_url = 'http://temp.163.com/special/00804KVA/cm_shehui.js'
            # yield Request(url=sh_url, callback=self.parse_index, dont_filter=False)
            # sh_urls = 'http://temp.163.com/special/00804KVA/cm_shehui_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)      # zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
            #     yield Request(url=sh_urls.format(s), callback=self.parse_index)
            #
            # # 国内url
            # gn_url = 'http://temp.163.com/special/00804KVA/cm_guonei.js'
            # yield Request(url=gn_url, callback=self.parse_index)
            # gn_urls = 'http://temp.163.com/special/00804KVA/cm_guonei_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=gn_urls.format(s), callback=self.parse_index)
            #
            # # 国际url
            # gj_url = 'http://temp.163.com/special/00804KVA/cm_guoji.js'
            # yield Request(url=gj_url, callback=self.parse_index)
            # gj_urls = 'http://temp.163.com/special/00804KVA/cm_guoji_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=gj_urls.format(s), callback=self.parse_index)
            #
            # # 军事url
            # war_url = 'http://temp.163.com/special/00804KVA/cm_war.js'
            # yield Request(url=war_url, callback=self.parse_index)
            # war_urls = 'http://temp.163.com/special/00804KVA/cm_war_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=war_urls.format(s), callback=self.parse_index)
            #
            # # 财经url
            # money_url = 'http://temp.163.com/special/00804KVA/cm_money.js'
            # yield Request(url=money_url, callback=self.parse_index, dont_filter=False)
            # money_urls = 'http://temp.163.com/special/00804KVA/cm_money_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=money_urls.format(s), callback=self.parse_index, dont_filter=False)
            # #
            # # 科技
            # tech_url = 'http://temp.163.com/special/00804KVA/cm_tech.js'
            # yield Request(url=tech_url, callback=self.parse_index, dont_filter=False)
            # tech_urls = 'http://temp.163.com/special/00804KVA/cm_tech_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=tech_urls.format(s), callback=self.parse_index, dont_filter=False)
            #
            # # 体育url
            # sport_url = 'http://temp.163.com/special/00804KVA/cm_sports.js'
            # yield Request(url=sport_url, callback=self.parse_index, dont_filter=False)
            # sport_urls = 'http://temp.163.com/special/00804KVA/cm_sports_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=sport_urls.format(s), callback=self.parse_index, dont_filter=False)
            #
            # # 娱乐url
            # ent_url = 'http://temp.163.com/special/00804KVA/cm_ent.js'
            # yield Request(url=ent_url, callback=self.parse_index, dont_filter=False)
            # ent_urls = 'http://temp.163.com/special/00804KVA/cm_ent_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=ent_urls.format(s), callback=self.parse_index, dont_filter=False)
            #
            # # 时尚url
            # lady_url = 'http://temp.163.com/special/00804KVA/cm_lady.js'
            # yield Request(url=lady_url, callback=self.parse_index, dont_filter=False)
            # lady_urls = 'http://temp.163.com/special/00804KVA/cm_lady_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=lady_urls.format(s), callback=self.parse_index, dont_filter=False)
            #
            # # 汽车url
            # auto_url = 'http://temp.163.com/special/00804KVA/cm_auto.js'
            # yield Request(url=auto_url, callback=self.parse_index, dont_filter=False)
            # auto_urls = 'http://temp.163.com/special/00804KVA/cm_auto_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=auto_urls.format(s), callback=self.parse_index, dont_filter=False)
            #
            # # 航空url
            # hk_url = 'http://temp.163.com/special/00804KVA/cm_hangkong.js'
            # yield Request(url=hk_url, callback=self.parse_index, dont_filter=False)
            # hk_urls = 'http://temp.163.com/special/00804KVA/cm_hangkong_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=hk_urls.format(s), callback=self.parse_index, dont_filter=False)
            #
            # # 健康url
            # jk_url = 'http://temp.163.com/special/00804KVA/cm_jiankang.js'
            # yield Request(url=jk_url, callback=self.parse_index, dont_filter=False)
            # jk_urls = 'http://temp.163.com/special/00804KVA/cm_jiankang_{}.js'
            # for i in range(2, 10):
            #     n = str(i)
            #     s = n.zfill(2)
            #     yield Request(url=jk_urls.format(s), callback=self.parse_index, dont_filter=False)

    def parse_index(self, response):
        # 对文本内容进行解码，并赋值给变量
        text = response.body.decode('gbk')
        # 取出掉多余内容，用json转成字典
        datas = json.loads(text.lstrip('data_callback(').rstrip(')').strip())
        for data in datas:
            item = NewItem()
            item['title'] = data['title']
            item['comment'] = data['tienum']
            # item['time'] = data['time']
            docurl = data['docurl']
            # 排除网页
            if 'dy.163.com' in docurl:
                continue
            if 'hongcai.163.com' in docurl:
                continue
            if 'nba.sports.163.com' in docurl:
                continue
            if 'cai.163.com' in docurl:
                continue
            if 'v.163.com' in docurl:
                continue
            if 'live.163.com/room' in docurl:
                continue
            if 'c.m.163.com/news/' in docurl:
                continue

            if 'photoview' in docurl:
                yield Request(url=docurl, meta={'key': item}, callback=self.parse_pic, dont_filter=False)
            else:
                yield Request(url=docurl, meta={'key': item}, callback=self.parse_doc, dont_filter=False)
                # commenturl = data['commenturl']

    def parse_doc(self, response):
        item = response.meta['key']

        # title = response.css('#epContentLeft h1::text').extract_first()

        item['time'] = response.css(self.template['Website_pubtime']).extract_first().strip()[:-13]
        item['source'] = response.css('#ne_article_source::text').extract_first()
        texts = response.css(self.template['Website_content']).extract()
        # 正文
        t = []
        contents = ''
        for text in texts:
            t.append(text.strip())
            contents = ''.join(t)
        item['contents'] = contents
        # 编辑人
        editor = response.css(self.template['Website_author']).extract_first().lstrip('责任编辑：')
        editors = re.findall('[\u4e00-\u9fa5]', editor)
        item['editor'] = ''.join(editors)
        yield item

    def parse_pic(self, response):
        item = response.meta['key']
        # 图片相配的文本内容
        res = response.css('body > div.gallery > textarea::text').extract_first()
        list1 = json.loads(res)  # 转成字典格式，提取内容
        list2 = []
        list3 = ''
        for li in list1['list']:
            if li['note'].strip() not in list2:  # 去重，如果不是list2中就添加
                list2.append(li['note'].strip())
                list3 = ''.join(list2)
        item['contents'] = list3
        # 编辑人信息
        editor = list1['info']['dutyeditor']
        editors = re.findall('[\u4e00-\u9fa5]', editor)
        item['editor'] = ''.join(editors)
        # 时间
        item['time'] = list1['info']['lmodify'][:-9]
        # 新闻源
        item['source'] = list1['info']['source']
        yield item
