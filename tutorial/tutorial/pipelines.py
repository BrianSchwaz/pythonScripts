# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import XmlItemExporter

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class durantPipeline(object):
    vat_factor = 1.15

    def open_spider(self,spider):
        self.stats_to_exporter = {}
        self.files_to_close = {}

    def close_spider(self,spider):
        for exporter in self.stats_to_exporter.values():
            exporter.finish_exporting()
        for file in self.files_to_close.values():
        	file.close()
            

    def _exporter_for_item(self, item):
        stat = type(item).__name__
        if stat not in self.stats_to_exporter:
            f = open('{}.csv'.format(stat),'w+b')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.files_to_close[stat] = f
            self.stats_to_exporter[stat] = exporter
        return self.stats_to_exporter[stat]

    def process_item(self,item,spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        #print(item)
        return item