# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from wangyi.spiders import SQL


class WangyiPipeline(object):
    def process_item(self, item, spider):
        if spider.name == '163':
            time = item['time']

            if len(time) > 6:
                item['time'] = time[0:4] + time[5:7] + time[-2:]

            data = dict(item)
            SQL.Sql.inserdata(data, 'wangyi_all')
        return item

class Wangyi_editor(object):
    def process_item(self, item, spider):
        if spider.name == '163':
            data = {}
            data['id'] = None
            data['Editor'] = item['editor']
            data['Source'] = item['source']
            data['Times'] = item['time']
            data['Comments'] = item['comment']
            SQL.Sql.inser_editor(data, 'wangyi_editor')
        return item


class Wangyi_source(object):
    def process_item(self, item, spider):
        if spider.name == '163':
            data = {}
            data['id'] = None
            data['Source'] = item['source']
            data['Times'] = item['time']
            data['Comments'] = item['comment']
            SQL.Sql.inser_source(data, 'wangyi_source')
        return item

class sina_source(object):
    def process_item(self, item, spider):
        if spider.name == 'sina':
            time = item['time']

            if len(time) == len('2017年10月01日'):
                item['time'] = time[0:4] + time[5:7] + time[8:10]

            data = dict(item)
            SQL.Sql.inserdata(data, 'Sina_all')

            data = {}
            data['id'] = None
            data['Source'] = item['source']
            data['Times'] = item['time']
            data['Comments'] = item['comment']
            SQL.Sql.inser_source(data, 'Sina_source')

            data = {}
            data['id'] = None
            data['Editor'] = item['editor']
            data['Source'] = item['source']
            data['Times'] = item['time']
            data['Comments'] = item['comment']
            SQL.Sql.inser_editor(data, 'Sina_editor')

        return item

class Acfun_insert(object):
    def process_item(self, item, spider):
        if spider.name == 'acfun':
            time = item['time']
            if len(time) == len('2017年10月01日'):
                item['time'] = time[0:4] + time[5:7] + time[8:10]
            if len(time) == len('2017年10月1日'):
                item['time'] = time[0:4] + time[5:7] + time[8:9]
            data = dict(item)
            SQL.Sql.inserdata(data, 'Acfun_all')

            data = {}
            data['id'] = None
            data['Source'] = item['UP']
            data['Times'] = item['time']
            data['Comments'] = item['comments']
            SQL.Sql.inser_source(data, 'Acfun_source')

            data = {}
            data['id'] = None
            data['Editor'] = item['UP']
            data['Source'] = item['UP']
            data['Times'] = item['time']
            data['Comments'] = item['comments']
            SQL.Sql.inser_editor(data, 'Acfun_editor')

        return item