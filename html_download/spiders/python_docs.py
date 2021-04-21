import scrapy


class PythonDocsSpider(scrapy.Spider):
    name = 'python_docs'
    allowed_domains = ['docs.scrapy.org/en/latest/']
    start_urls = ['http://docs.scrapy.org/en/latest/']

    def parse(self, response):
        # just first link in each section
        links = response.xpath("//div/ul/li[1]/a[contains(@class, 'reference internal')]")
        for index, link in enumerate(links):
            href_xpath = link.xpath('@href').get()
            title_xpath = link.xpath('text()').get()
            # download for each page
            next_url = response.url + href_xpath
            title = title_xpath + '.html'
            yield scrapy.Request(
                url=next_url,
                callback=self.save_html,
                meta={
                         'save_html': True,
                     },
            )

    def response_html_path(self, request):
        """
        Args:
            request (scrapy.http.request.Request): request that produced the
                response.
        """
        return 'html/last_response.html'