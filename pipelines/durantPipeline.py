from scrapy.exporters import CsvItemExporter

class durantPipeline(object):
    vat_factor = 1.15

    def open_spider(self,spider):
        self.stats_to_exporter = {}

    def close_spider(self,spider):
        for exporter in self.stats_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_item(self, item):
        stat = item['stat']
        if stat not in self.stats_to_exporter:
            f = open('{}.csv'.format(stat),'wb')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.stats_to_exporter[stat] = exporter
        return self.stats_to_exporter[stat]

    def process_item(self,item,spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
