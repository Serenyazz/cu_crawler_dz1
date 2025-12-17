# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

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

