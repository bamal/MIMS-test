import numpy as np
import scrapy
from scrapymims.items import JsonLinesItemExporter

# To execute the spider only
# scrapy crawl images -a urls="https://scrapy.org/community/, https://scrapy.org/"

class ImagesSpider(scrapy.Spider):

    name = "images"

    def __init__(self, urls ='', *args, **kwargs):

        self.start_urls = urls.split(",")

        self.logger.info(self.start_urls)

        self.urls_child = []

        self.jobId = kwargs.get('_job')

        self.file = open('data/'+self.jobId+'.pickle', 'w+b')

        self.exporter = JsonLinesItemExporter(self.file)

        self.exporter.start_exporting()

        super(ImagesSpider, self).__init__(*args, **kwargs)


    def start_requests(self):

        for url in self.start_urls:
            # Send the request to parse the urls, in the case of duplicated urls to parse, it is filtered
            yield scrapy.Request(url=url, callback=self.parse, dont_filter = False)


    def parse(self, response, dont_filter=False):
        """
        Parse a url and its descendents urls to extract their images urls

        :param response: Object
            An HTTP response

        :param dont_filter: Bool
            Indicates whether this request should not be filtered by the scheduler or not.
            This is used when you want to perform an identical request multiple times
            to ignore the duplicates.
        :return: List of Item object
            Each item represents the url of the page and its images urls
        """

        # first layer crawling
        yield self.parse_deeper(response)

        # second layer crawling
        self.urls_child = response.css('a[href*=http]::attr(href)').getall()

        for url in self.urls_child:
            # Send the request to parse the first later children urls, in the case of
            # duplicated urls to parse, it is filtered
            yield scrapy.Request(url=url, callback=self.parse_deeper, dont_filter = False)


    def parse_deeper(self, response):
        """
        Parse the url to extract images urls
        :param response: Object
            An HTTP response
        :return: Item
            An image item has two fields
            url: string
                the url of the page
            images_url: list of string
                the list of urls of all images within the page
        """
        url = response.url

        imgs = np.asarray(response.css('img').xpath('@src').getall())

        imgs_filtered = self._extract_clean_imgs(imgs)

        if self._extract_clean_imgs(imgs) is not None:

            self.exporter.export_item({url:imgs_filtered})

            return {
                url: imgs_filtered
            }


    def _extract_clean_imgs(self, imgs):
        """
        Extract images urls without duplicates and with only three
         extentions (i.e., GIF, PNG, JPEG)

        :param response: Object
            An HTTP response
        :return:
        """
        try:

            # filter images according to their extension using vectorized
            # fast operations
            mask = [(".gif" in img or ".png" in img or ".jpeg" in img) and "http" in img
                    for img in imgs]

            mask = np.asarray(mask)

            imgs = np.unique(imgs[mask])

            if len(imgs) > 1:

                return imgs.tolist()

        except:

            return None

        return None



