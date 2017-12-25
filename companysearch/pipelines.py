# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import csv

class CompanysearchPipeline(object):
    def __init__(self):
        # self.file = codecs.open('data.json', mode='wb', encoding='utf-8')#数据存储到data.json
        self.csvwriter = csv.writer(open('data.csv', 'wb'), delimiter=',')#数据存储到data.csv
        self.csvwriter.writerow(['companyname','info','industry','introduction']) #添加head
    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line.decode("unicode_escape"))
        # return item
        rows = zip(item['companyname'],item['info'],item['industry'],item['introduction'])
        for row in rows:
            self.csvwriter.writerow(row)
        return item
