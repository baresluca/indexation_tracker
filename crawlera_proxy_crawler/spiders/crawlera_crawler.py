import scrapy
import csv
from ..items import CrawleraProxyCrawlerItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class CrawleraSpider(scrapy.Spider):
    name = "crawlera_crawler"
    
    def start_requests(self):
        with open('indexation-list.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            start_urls = list(csv_reader)
        
        for row in start_urls:
            url = row[0]
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)

    def parse(self, response):
        items = CrawleraProxyCrawlerItem()

        status_code = response.status        
        scraped_url = response.request.url
        error_code = response.request.meta
        links = response.css('div.g div.rc div.r a::attr(href)').getall()
        no_match = response.css('div.med div.mnr-c div.med.card-section p::text').getall()


        items['scraped_url'] = scraped_url
        items['links'] = links
        items['no_match'] = no_match
        items['status_code'] = status_code
        items['error_code'] = error_code

        yield items

    def errback_httpbin(self, failure):       
        # log all failures
        self.logger.error(repr(failure))


        # in case you want to do something special for some errors,
        # you may need the failure's type:
        with open('errors.csv', mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=',')

            if failure.check(HttpError):
                # these exceptions come from HttpError spider middleware
                # you can get the non-200 response
                response = failure.value.response
                err_status = response.status
                err_url = response.url
                self.logger.error('HTTP Error %s and %s', err_url, err_status)
                writer.writerow([err_url, err_status])
                

            elif failure.check(DNSLookupError):
                # this is the original request
                request = failure.request
                self.logger.error('DNS Lookup Error %s', response.url)
                writer.writerow([err_url, err_status])

            elif failure.check(TimeoutError, TCPTimedOutError):
                request = failure.request
                self.logger.error('TIMEOUT on %s', response.url)
                writer.writerow([err_url, err_status])


