import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FivesuperSpider(CrawlSpider):
    name = 'FiveSuper'
    allowed_domains = ['khamsat.com']
    start_urls = ['https://khamsat.com/search?q=scraping&siv=false&sr=4&no_keyword=false']


    le_khedma = LinkExtractor(restrict_css='div.service-card__title>h3>a')

    rule_khedma = Rule(le_khedma, callback='parse_item', follow=False)

    rules = (
        rule_khedma,
    )

    def parse_item(self, response):
        
        service =  response.css('h1::text').get()
        provider = response.css('a.sidebar_user::text').get()
        service_detail = response.css('div.c-card__body>article::text').getall()
        no_buyers = response.css('div.c-card__section>div#sidebar>div.o-layout__item.u-6\@large.u-6\@medium.u-6\@small.u-6\@tiny:nth-of-type(6)>span::text').get()
        avr_reply = response.css('div.c-card__section>div#sidebar>div.o-layout__item.u-6\@large.u-6\@medium.u-6\@small.u-6\@tiny:nth-of-type(4)>span::text').get()
        delivery = response.css('div.c-card__section>div#sidebar>div.o-layout__item.u-6\@large.u-6\@medium.u-6\@small.u-6\@tiny:nth-of-type(12)>span::text').get()
        seller_tags = response.css('ul.c-list.c-list--tags a::text').extract()
        avatar = response.css('img.u-circle.img-thumbnail.img--medium::attr(src)').get()
        last_review = response.css('div.discussion-message article::text').get().strip()

        extras = response.css('td.checkable.details-td')
        for row in extras:
            extra = row.css('h3.details-head::text').get().strip()
            price_extra = row.css('div.details-hint>p::text').get().strip()

            yield {
                
                'service_name':service,
                'service_description':service_detail,
                'provider_name':provider,
                'seller_tags': seller_tags,
                'avg_speed_reply':avr_reply,
                'delivery_period':delivery,
                'number_of_buyers': no_buyers,
                'extra_service':extra,
                'extra_service_fee': price_extra,
                'last_buyer_review': last_review,
                'service_Link':response.url,
                'seller_picture_link':avatar,
            }
