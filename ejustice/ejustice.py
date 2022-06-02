import os

import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

proxy_username = os.environ.get("packetstream_username")
proxy_password = os.environ.get("packetstream_password")

class ejustice(scrapy.Spider):
    name = 'ejustice'
    custom_settings = {'CONCURRENT_REQUESTS': 1,
                       'FEED_FORMAT': 'jsonlines',
                       'FEED_URI': 'scraped_data/' + datetime.now().strftime('%Y_%m_%d__%H_%M') + 'ta_5stars.jl',
                       'DOWNLOADER_MIDDLEWARES': {
                           'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
                           'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
                       }
                       }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'TS01e238cf=010e20986166c44512e9e466d696ef3d148505c276b52635f754d159a007c6257ac3fd0a5bf143e0c14dadcaec444211d997dbac73',
        'Pragma': 'no-cache',
        'Referer': 'https://www.ejustice.just.fgov.be/loi/loi.htm',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    languages = ['fr', 'nl']

    PROXY = f'http://{proxy_username}:{proxy_password}@proxy.packetstream.io:31112'

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.ejustice.just.fgov.be/loi/loi2.htm',
            headers=self.headers,
            meta={
                'proxy': self.PROXY,
            },
            callback=self.parse
        )

    def parse(self, response):
        option_1 = [i.strip() for i in response.xpath('//select[@tabindex="2"]//option//text()').getall() if
                    i.strip() != '']
        option_2 = [i.strip() for i in response.xpath('//select[@tabindex="16"]//option//text()').getall() if
                    i.strip() != '']
        option_3 = [i.strip() for i in response.xpath('//select[@tabindex="24"]//option//text()').getall() if
                    i.strip() != '']

        for i in option_1:
            for j in option_2:
                for k in option_3:
                    option_i = '&+'.join(["'" + substr.replace("'", '"') + "'" for substr in i.upper().split(' ')])
                    option_j = '+'.join([substr.replace("'", '"') for substr in i.upper().split(' ')])
                    option_j = f"'{option_j}'"
                    option_k = '+'.join([substr.replace("'", '"') for substr in i.upper().split(' ')])
                    option_k = f"'{option_k}'"
                    # option_url = f"https://www.ejustice.just.fgov.be/cgi_loi/loi_l1.pl?language=fr&sql=dt+contains++'ACCORD'&+'DE'&+'COOPERATION'&+'(NATIONAL)'+and+so1+contains+'AFFAIRES+ECONOMIQUES'+and+cc+contains+'DROIT+PUBLIC'and+actif+=+'Y'&fromtab=loi_all&tri=dd+AS+RANK+&trier=promulgation&rech=2&caller=list&dt=ACCORD+DE+COOPERATION+(NATIONAL)&dtnum=&ddda=&dddm=&dddj=&ddfa=&ddfm=&ddfj=&pdda=&pddm=&pddj=&pdfa=&pdfm=&pdfj=&so=AFFAIRES+ECONOMIQUES&text1=&choix1=ET&text2=&choix2=ET&text3=&chercher=t&cc=DROIT+PUBLIC&fr=f&nl=&nm_ecran=&nmrc=&cn_y_ecran=&cn_m_ecran=&cn_d_ecran=&cn_num_ecran=&"
                    for lang in self.languages:
                        option_url = f"https://www.ejustice.just.fgov.be/cgi_loi/loi_l1.pl?language={lang}&sql=dt+contains++{option_i}+and+so1+contains+{option_j}+and+cc+contains+{option_k}and+actif+=+'Y'&fromtab=loi_all&tri=dd+AS+RANK+&trier=promulgation&rech=2&caller=list&dt=ACCORD+DE+COOPERATION+(NATIONAL)&dtnum=&ddda=&dddm=&dddj=&ddfa=&ddfm=&ddfj=&pdda=&pddm=&pddj=&pdfa=&pdfm=&pdfj=&so=AFFAIRES+ECONOMIQUES&text1=&choix1=ET&text2=&choix2=ET&text3=&chercher=t&cc=DROIT+PUBLIC&fr=f&nl=&nm_ecran=&nmrc=&cn_y_ecran=&cn_m_ecran=&cn_d_ecran=&cn_num_ecran=&"
                        head_item = {
                            "Nature juridique": i,
                            "Département": j,
                            "Domaine juridique": k,
                            "language": lang,

                        }
                        yield scrapy.Request(
                            url=option_url,
                            headers=self.headers,
                            meta={
                                'proxy': self.PROXY,
                                'head_item': head_item,

                            },
                            callback=self.parse_loi
                        )

    def parse_loi(self, response):

        details = response.xpath('//input[@name="DETAIL"]')
        head_item = response.meta['head_item']
        for detail in details:
            if head_item['language'] == 'nl':
                publication_date = detail.xpath(
                    './ancestor::tr//b[contains(text(),"Gepubliceerd op")]/font/text()').get('').strip()
                source = detail.xpath('./ancestor::tr//b[contains(text(),"Bron")]/font/text()').get('').strip()
            else:
                publication_date = detail.xpath('./ancestor::tr//b[contains(text(),"Published")]/font/text()').get(
                    '').strip()
                source = detail.xpath('./ancestor::tr//b[contains(text(),"Source")]/font/text()').get('').strip()
            detail_value = detail.xpath('./@value').get()

            title = detail.xpath('./ancestor::tr/td/font//text()').get('').strip()

            url = f"https://www.ejustice.just.fgov.be/cgi_loi/loi_a1.pl?DETAIL={detail}&caller=list&cn={detail_value.split('/')[0]}&language={head_item['language']}&fromtab=loi_all"

            mid_item = {
                "Publication date": publication_date,
                "Source": source,
                "Title": title,
            }
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                meta={
                    'proxy': self.PROXY,
                    'head_item': response.meta['head_item'],
                    'mid_item': mid_item,
                },
                callback=self.parse_loi_detail
            )

    def parse_loi_detail(self, response):
        head_item = response.meta['head_item']
        text = ' '.join(response.xpath(
            '//th/font[contains(text()," Texte ")]/ancestor::tr/following-sibling::tr//text()').getall()).strip().replace(
            '\xa0\xa0', '\n')
        if head_item['language'] == 'fr':
            numero = response.xpath('//font[contains(text(),"numéro : ")]/following-sibling::text()').get('').strip()
            text = ' '.join(response.xpath(
                '//th/font[contains(text()," Texte ")]/ancestor::tr/following-sibling::tr//text()').getall()).strip().replace(
                '\xa0\xa0', '\n')
        else:
            numero = response.xpath('//font[contains(text(),"nummer : ")]/following-sibling::text()').get('').strip()
            text = ' '.join(response.xpath(
                '//th/font[contains(text()," Tekst ")]/ancestor::tr/following-sibling::tr//text()').getall()).strip().replace(
                '\xa0\xa0', '\n')

        final_item = {
            **response.meta['head_item'],
            **response.meta['mid_item'],
            "Text": text,
            "Country": "Belgium",
            "Number": numero,
            # "Language" : "fr",
        }

        yield final_item


if __name__ == '__main__':
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ejustice)
    process.start()
