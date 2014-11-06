import scrapy
import smtplib
from scrapy.exceptions import CloseSpider
from PriceWatcher.items import PriceWatcherItem
from PriceWatcher.SitesAndURLs import *
from email.mime.text import MIMEText

class PriceWatcherSpider(scrapy.spider.Spider):
    name = "PriceWatcher"
    allowed_domain = URL_BARNEYS

    start_urls = URL_SALE_BAG_BARNEYS

    def parse(self, response):
        divs = response.xpath('//div[@class="product producttile"] | //div[@class="product producttile last"]')
        for div in divs :
            item = PriceWatcherItem()
            item['id'] = div.xpath('@id').extract()
            item['name'] = div.xpath('.//div[@class="name"]/a/span[@class="displayname"]/text()').extract()
            item['designer'] = div.xpath('.//div[@class="name"]/a/span[@class="designername"]/text()').extract()
            item['price'] = div.xpath('.//div[@class="price"]//div[@class="salesprice"]/em/text()').extract()
            item['originalPrice'] = div.xpath('.//div[@class="price"]//div[@class="standardprice"]/text()').extract()
            item['link'] = div.xpath('.//p[@class="productimage"]/a/@href').extract()
            if str(item['id']) in IDS_SEEN:
                continue
            else:
                IDS_SEEN.add(str(item['id']))
                self.send_email_notification(item)
            yield item

    def send_email_notification(self, newly_added_bagItem):
        text = str(newly_added_bagItem['name'][0])+ \
               " is on Sale. Click the following link :" + "\n" + "\n" + \
               str(newly_added_bagItem['link'][0]).encode("ascii")

        msg = MIMEText(text)
        msg['Subject'] = "Barneys added new items in its Bag Sale"
        msg['From'] = FROM_EMAIL
        msg['To'] = ','.join(TO_EMAILS)

        s=smtplib.SMTP('smtp.gmail.com:587')
        try:
            s.starttls()
            s.login(LOG_IN, PASS_WORD)
            s.sendmail(FROM_EMAIL, TO_EMAILS, msg.as_string())
        finally:
            s.quit()

    def stop(self):
        raise CloseSpider("Stopping spider")

    #if __name__ == '__main__':
