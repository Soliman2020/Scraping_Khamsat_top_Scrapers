import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from time import strftime,gmtime

class FivesuperSpider(CrawlSpider):
    name = 'FiveSuper'
    # use this settings here instead of using in settings.py
    custom_settings = {
        'ROBOTSTXT_OBEY' : False,   # Inforce website to accept running our spider for the web scrapping   
        'FEED_FORMAT': 'csv',
        'FEED_URI': f'KHAMSAT_{strftime("%Y-%m-%d_%H_%M", gmtime())}GMT.csv' # file name refer to the date and time.
    }
    
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
            
# run file from internal terminal is not avaliable
# because of website blocked the scraping by default
# So I can't apply the following code

# from scrapy.crawler import CrawlerProcess  # To run the process without switching to the terminal in case it is possible!
# process = CrawlerProcess ()
# process.crawl(FivesuperSpider)
# process.start()
