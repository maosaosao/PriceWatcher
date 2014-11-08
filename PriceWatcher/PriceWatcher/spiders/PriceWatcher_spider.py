import scrapy
import smtplib
import json
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
            with open('items.json', 'r') as data_file:
                s = data_file.read()
                existIds = json.loads(s)
                for eid in existIds:
                    IDS_SEEN.add(eid)
            itemID = str(item['id'])[-16:-2]
            if itemID in IDS_SEEN:
                continue
            else:
                print('Newly added Item!')
                IDS_SEEN.add(itemID)
                with open('items.json', 'w') as data_file:
                    s = json.dumps(list(IDS_SEEN))
                    data_file.write(s)
                self.send_email_notification(item)
            yield item

    def send_email_notification(self, newly_added_bagItem):
        bagName = str(newly_added_bagItem['name'][0])
        bagDesigner = str(newly_added_bagItem['designer'][0])
        #bagPrice = str(newly_added_bagItem['price'][0])
        bagLink = str(newly_added_bagItem['link'][0]).encode("ascii")

        text = bagDesigner + " " + bagName+ \
               " is on Sale "  + "\n" + "\n" + \
               " Click the following link :" + "\n" + "\n" + \
               bagLink


        msg = MIMEText(text)
        msg['Subject'] = "Barneys added " + bagName + " in its Bag Sale "
        msg['From'] = FROM_EMAIL
        msg['To'] = ','.join(TO_EMAILS)

        s=smtplib.SMTP('smtp.gmail.com:587')
        try:
            s.starttls()
            s.login(LOG_IN, PASS_WORD)
            s.sendmail(FROM_EMAIL, TO_EMAILS, msg.as_string())
        finally:
            s.quit()
