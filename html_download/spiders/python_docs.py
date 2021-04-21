import scrapy


class PythonDocsSpider(scrapy.Spider):
    name = 'python_docs'
    allowed_domains = ['docs.scrapy.org/en/latest/']
    start_urls = ['http://docs.scrapy.org/en/latest//']

    def parse(self, response):
        pass
