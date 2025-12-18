# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class CuCrawlingPipeline:
    def process_item(self, item: dict[str, str], spider):
        address = item.get("address")
        
        if isinstance(address, str):
            prefix = "  —  "
            if address.startswith(prefix):
                item["address"] = address.replace(prefix, "")

        org_description = item.get("org_description")
        
        if isinstance(org_description, str):
            item["org_description"] = org_description.replace("\n", " ").strip()

        item["merchant_name"] = item["merchant_name"].strip()

        return item


class MongoPipeline:
    collection_name = 'collection' 

    def __init__(self):
        self.mongo_uri = "mongodb://admin:pass@localhost:27017/{self.mongo_db}?authSource=admin"
        self.mongo_db = "items"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            print(f"--> Saved to Mongo: {item.get('title', 'Unknown Title')} ---------------------------------------")

