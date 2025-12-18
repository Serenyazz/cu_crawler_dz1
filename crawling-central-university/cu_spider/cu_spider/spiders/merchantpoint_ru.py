import scrapy


class MerchantpointRuSpider(scrapy.spiders.SitemapSpider):
    name = "merchantpoint_ru"
    allowed_domains = ["merchantpoint.ru"]

    sitemap_urls = ("https://merchantpoint.ru/sitemap/brands.xml", )
    sitemap_rules = [('/brand', 'parse')]

    # start_urls = ["https://merchantpoint.ru/brand/4390"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "cu_spider.pipelines.CuCrawlingPipeline": 300,
        },
        "CLOSESPIDER_ITEMCOUNT": 30
    }

    def parse(self, response):
        raw_org_description = response.xpath("//div[contains(@class, 'description_brand')]//text()").getall()
        org_description = ' '.join(raw_org_description)
        merchant_urls = response.xpath("//table[@class='finance-table']//a/@href").getall()
        
        yield from response.follow_all(urls=merchant_urls, 
                                        cb_kwargs={"org_description": org_description}, 
                                        callback=self.parse_merchant)

    def parse_merchant(self, response, org_description):
        return {
            "merchant_name": response.xpath("//h1[contains(@class, 'text-3xl md:text-4xl')]/text()").get(), 
            "mcc": response.xpath("//p[contains(., 'MCC')]/a/text()").get(), 
            "address": response.xpath("//div//p[contains(., 'Адрес')]/text()").get(), 
            "geo_coordinates": response.xpath("//div//p[contains(., 'Геокоординаты:')]/text()").get(), 
            "org_name": response.xpath("//div//p/a[contains(@href, '/brand/')]/text()").get(), 
            "org_description": org_description,
            "source_url": response.url
        }
