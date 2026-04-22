# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from search_engine import create_index, insert_document

class SearchPipeline:
    def __init__(self, index_name):
        self.index_name = index_name
    @classmethod
    def from_crawler(cls, crawler):
        index_name = crawler.settings.get("ES_INDEX", "news")
        return cls(index_name)
    def open_spider(self):
        create_index(self.index_name)
    def process_item(self, item):
        insert_document(item, self.index_name)
        return item

