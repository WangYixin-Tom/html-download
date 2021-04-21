# https://docs.scrapy.org/en/latest/topics/practices.html

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from spiders.python_docs import PythonDocsSpider

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(PythonDocsSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished