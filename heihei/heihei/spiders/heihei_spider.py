import scrapy


class StackOverflowSpider(scrapy.Spider):
    name = 'heihei'
    start_urls = ['http://www.fanhome.org/lei/']


    def parse(self, response):
        for href in response.css('.genreitem a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_main)
    def parse_main(self, response):
        # now_href = response.css('.pagination li[class=active] a::attr(href)')
        # now_full_url = response.urljoin(now_href.extract())
        # yield scrapy.Request(response.url, callback=self.parse_page)
        # href = response.css('.pagination li[class=active]+li a::attr(href)')
        # if href is not None:
        #     full_url = response.urljoin(href.extract())
        #     yield scrapy.Request(full_url, callback=self.parse_main)
        for i in range(1,151):
            ex_url= response.url+'/'+str(i)+".htm"
            full_url = ex_url
            yield scrapy.Request(full_url, callback=self.parse_page)
    def parse_page(self, response):
        for href in response.css('.td2 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('.col-sm-9 .page-header a::text').extract()[0],
            'id': response.css('.col-xs-12 .info p span::text').extract()[1],
            'date': response.css('.col-xs-12 .info p::text').extract()[1],
            'length': response.css('.col-xs-12 .info p::text').extract()[2],
            'director': response.css('.col-xs-12 .info p::text').extract()[3],
            'producter': response.css('.col-xs-12 .info p::text').extract()[5],
            'publisher': response.css('.col-xs-12 .info p::text').extract()[7],
            'actor': response.xpath('/html/body/div/div/div[1]/div[2]/div/h4/a/text()'),
            'tags': response.css('.genre a::text').extract(),
            'link': response.url,
        }

