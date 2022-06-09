import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

proxy_username = ""
proxy_password = ""


class ejustice(scrapy.Spider):
    name = 'ejustice'
    custom_settings = {'CONCURRENT_REQUESTS': 25,
                       'FEED_FORMAT': 'jsonlines',
                       'FEED_URI': 'scraped_data/' + datetime.now().strftime('%Y_%m_%d__%H_%M') + 'ejustice.jl',
                       'DOWNLOADER_MIDDLEWARES': {
                           'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
                           'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
                       },
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

    PROXY = f'http://{proxy_username}:{proxy_password}@proxy.packetstream.io:31112' if proxy_username else ""

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
                    option_j = '+'.join([substr.replace("'", '"') for substr in j.upper().split(' ')])
                    option_j = f"'{option_j}'"
                    option_k = '+'.join([substr.replace("'", '"') for substr in k.upper().split(' ')])
                    option_k = f"'{option_k}'"
                    option_url = f"https://www.ejustice.just.fgov.be/cgi_loi/loi_l1.pl?row_id=1&language=fr&sql=dt+contains++{option_i}+and+so1+contains+{option_j}+and+cc+contains+{option_k}and+actif+=+'Y'&fromtab=loi_all&tri=dd+AS+RANK+&trier=promulgation&rech=2&caller=list&dt=ACCORD+DE+COOPERATION+(NATIONAL)&dtnum=&ddda=&dddm=&dddj=&ddfa=&ddfm=&ddfj=&pdda=&pddm=&pddj=&pdfa=&pdfm=&pdfj=&so=AFFAIRES+ECONOMIQUES&text1=&choix1=ET&text2=&choix2=ET&text3=&chercher=t&cc=DROIT+PUBLIC&fr=f&nl=&nm_ecran=&nmrc=&cn_y_ecran=&cn_m_ecran=&cn_d_ecran=&cn_num_ecran=&"

                    head_item = {
                        "Nature juridique": i,
                        "Département": j,
                        "Domaine juridique": k,

                    }
                    yield scrapy.Request(
                        url=option_url,
                        headers=self.headers,
                        meta={
                            'proxy': self.PROXY,
                            'head_item': head_item,
                            'option_url': option_url,

                        },
                        callback=self.parse_loi
                    )

    def parse_loi(self, response):
        details = response.xpath('//input[@name="DETAIL"]')
        head_item = response.meta['head_item']
        for detail in details:
            detail_value = detail.xpath('./@value').get()

            caller = detail.xpath('./parent::form//input[@name="caller"]/@value').get('')
            row_id = detail.xpath('./parent::form//input[@name="row_id"]/@value').get('')
            numero = detail.xpath('./parent::form//input[@name="numero"]/@value').get('')
            rech = detail.xpath('./parent::form//input[@name="rech"]/@value').get('')
            cn = detail.xpath('./parent::form//input[@name="cn"]/@value').get('')
            table_name = detail.xpath('./parent::form//input[@name="table_name"]/@value').get('')
            nm = detail.xpath('./parent::form//input[@name="nm"]/@value').get('')
            la = detail.xpath('./parent::form//input[@name="la"]/@value').get('')
            chercher = detail.xpath('./parent::form//input[@name="chercher"]/@value').get('')
            dt = detail.xpath('./parent::form//input[@name="dt"]/@value').get('')
            language = detail.xpath('./parent::form//input[@name="language"]/@value').get('')
            fr = detail.xpath('./parent::form//input[@name="fr"]/@value').get('')
            choix1 = detail.xpath('./parent::form//input[@name="choix1"]/@value').get('')
            choix2 = detail.xpath('./parent::form//input[@name="choix2"]/@value').get('')
            fromtab = detail.xpath('./parent::form//input[@name="fromtab"]/@value').get('')
            cc = detail.xpath('./parent::form//input[@name="cc"]/@value').get('')
            sql = detail.xpath('./parent::form//input[@name="sql"]/@value').get('')
            tri = detail.xpath('./parent::form//input[@name="tri"]/@value').get('')
            trier = detail.xpath('./parent::form//input[@name="trier"]/@value').get('')
            NATIONALandso1containsAFFA = detail.xpath(
                './parent::form//input[@name="NATIONALandso1containsAFFA"]/@value').get('')
            so = detail.xpath('./parent::form//input[@name="so"]/@value').get('')
            form_action = detail.xpath('./parent::form/@action').get('')
            data = {
                'DETAIL': detail_value,
                'caller': caller,
                'row_id': row_id,
                'numero': numero,
                'rech': rech,
                'cn': cn,
                'table_name': table_name,
                'nm': nm,
                'la': la,
                'chercher': chercher,
                'dt': dt,
                'language': language,
                'fr': fr,
                'choix1': choix1,
                'choix2': choix2,
                'fromtab': fromtab,
                'cc': cc,
                'sql': sql,
                'tri': tri,
                'trier': trier,
                'NATIONALandso1containsAFFA': NATIONALandso1containsAFFA,
                'so': so,
            }

            yield scrapy.FormRequest(
                url=response.urljoin(form_action),
                method='POST',
                formdata=data,
                callback=self.parse_loi_2,
                meta={'head_item': head_item}
            )
        next_row_id = response.xpath('//input[@name="next_row_id"]/@value').get('')

        if next_row_id:
            option_url = response.meta['option_url']

            next_option_url = option_url.split('row_id=')[0] + f"row_id={next_row_id}" + "&language" + \
                              option_url.split('&language')[-1]
            yield scrapy.Request(
                url=next_option_url,
                headers=self.headers,
                meta={
                    'proxy': self.PROXY,
                    'head_item': head_item,
                    'option_url': next_option_url,
                }
                , callback=self.parse_loi
            )

    def parse_loi_2(self, response):
        link_url = response.urljoin(response.xpath('//@src').get(''))
        yield scrapy.Request(
            url=link_url,
            callback=self.parse_loi_detail,
            meta={'head_item': response.meta['head_item']}
        )

    def parse_loi_detail(self, response):
        head_item = response.meta['head_item']
        all_text = ' '.join([i.strip() for i in response.xpath(
            '//font[contains(text()," Titre ")]/ancestor::tr/following-sibling::tr//th//text()').getall() if i.strip()])
        text_title = all_text.split('Source :')[0].strip()
        source = all_text.split('Source :')[1].split('Publication :')[0].strip()
        publication = all_text.split('Publication :')[1].split('numéro :')[0].strip()

        numero = response.xpath('//font[contains(text(),"numéro : ")]/following-sibling::text()').get('').strip()
        text = ' '.join(response.xpath(
            '//th/font[contains(text()," Texte ")]/ancestor::tr/following-sibling::tr//text()').getall()).strip().replace(
            '\xa0\xa0', '\n')

        final_item = {
            **head_item,
            "Publication date": publication,
            "Source": source,
            "Title": text_title,
            "Text": text,
            "Country": "Belgium",
            "Number": numero,
            "URL": response.url,
            "Language": "fr",
        }

        yield final_item

        dutch_version_url = response.xpath('//b[contains(text(),"Version néerlandaise")]/ancestor::a/@href').get('')

        if dutch_version_url:
            yield scrapy.Request(
                url=response.urljoin(dutch_version_url),
                headers=self.headers,
                meta={
                    'proxy': self.PROXY,
                    'head_item': head_item,
                },
                callback=self.parse_loi_detail_dutch
            )

    def parse_loi_detail_dutch(self, response):
        link_url = response.urljoin(response.xpath('//@src').get(''))
        yield scrapy.Request(
            url=link_url,
            callback=self.parse_loi_detail_dutch_detail,
            meta={'head_item': response.meta['head_item']}
        )

    def parse_loi_detail_dutch_detail(self, response):
        head_item = response.meta['head_item']
        all_text = ' '.join([i.strip() for i in response.xpath(
            '//font[contains(text()," Titel ")]/ancestor::tr/following-sibling::tr//th//text()').getall() if i.strip()])
        text_title = all_text.split('Bron :')[0].strip()
        source = all_text.split('Bron :')[1].split('Publicatie :')[0].strip()
        publication = all_text.split('Publicatie :')[1].split('nummer :')[0].strip()

        numero = response.xpath('//font[contains(text(),"nummer : ")]/following-sibling::text()').get('').strip()
        text = ' '.join(response.xpath(
            '//th/font[contains(text()," Tekst ")]/ancestor::tr/following-sibling::tr//text()').getall()).strip().replace(
            '\xa0\xa0', '\n')

        final_item = {
            **head_item,
            "Publication date": publication,
            "Source": source,
            "Title": text_title,
            "Text": text,
            "Country": "Belgium",
            "Number": numero,
            "URL": response.url,
            "Language": "nl",
        }

        yield final_item


if __name__ == '__main__':
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ejustice)
    process.start()
