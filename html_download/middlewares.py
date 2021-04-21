# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import utils.filesys as fs

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class HtmlStorageMiddleware(object):
    """Scrapy downloader middleware that stores HTML files to local file system.
    """

    def __init__(self, settings):
        """
        Args:
            settings (scrapy.settings.Settings)
        """
        self.settings = settings.get('HTML_STORAGE', {})
        self.save_html_on_codes = self.settings.get('save_html_on_codes', [])

    @classmethod
    def from_crawler(cls, crawler):
        """Contruct middleware with scrapy settings.

        Args:
            settings (scrapy.settings.Settings)

        Returns:
            HtmlStorageMiddleware:
        """
        return cls(crawler.settings)

    @classmethod
    def from_settings(self, settings):
        """Contruct middleware with scrapy settings.

        Args:
            settings (scrapy.settings.Settings)

        Returns:
            HtmlStorageMiddleware:
        """
        return HtmlStorageMiddleware(settings)


    def process_response(self, request, response, spider):
        """Stores response HTML body to file.

        Args:
            request (scrapy.http.request.Request): request which triggered
                this response.
            response (scrapy.http.Response)
            spider: (scrapy.Spider): spider that triggered the request.
                Spiders must set 'started_crawling' field to Unix timestamp.

        Returns:
            scrapy.http.response.Response: unmodified response object.
        """
        if self._should_save_html(request, response):
            fs.write_to_file(spider.response_html_path(request), response.text)

        return response


    def _should_save_html(self, request, response):
        """
        Args:
            request (scrapy.http.request.Request)
            response (scrapy.http.response.Response)

        Returns:
            bool: True if this request should be stored to disk, False otherwise.
        """
        return 'save_html' in request.meta and \
            should_save_html_according_response_code(
                response.status,
                self.save_html_on_codes
            )


def should_save_html_according_response_code(code, allowed_code_list):
    """
    Args:
        code (int): response status code
        allowed_code_list (list): list of response status codes allowed to save html

    Returns:
        bool: True if allowed_code_list is empty (save all responses), or response
              code in allowed list.
    """
    return not allowed_code_list or code in allowed_code_list


class HtmlDownloadSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HtmlDownloadDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
