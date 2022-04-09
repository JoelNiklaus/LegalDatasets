# https://www.fiverr.com/prakriteekhanal

# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from urllib.parse import urlparse

import pandas as pd

import json
import logging
import os
import pathlib
import shutil
from datetime import datetime

import requests
import scrapy
# pdfminer.six
from pdfminer.high_level import extract_text

logging.basicConfig()
logging.getLogger("pdfminer").setLevel(logging.WARNING)
from fake_headers import Headers

proxy_username = os.environ.get("packetstream_username")
proxy_password = os.environ.get("packetstream_password")


class ItalgiureGiustizia(scrapy.Spider):
    name = 'italgiure_giustizia'
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,

        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'scraped_data/' + datetime.now().strftime('%Y_%m_%d__%H_%M') + 'italgiure_giustizia.jl',

        # 'DOWNLOAD_DELAY': .5,
        'RETRY_TIMES': 30,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'PROXY': f'http://{proxy_username}:{proxy_password}@proxy.packetstream.io:31112',
        # http://user:pass@proxy.packetstream.io:31112
    }
    #

    headers = {
        'authority': 'www.italgiure.giustizia.it',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.italgiure.giustizia.it/',
        'accept-language': 'en-US,en;q=0.9',

    }
    headers_facet = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-GPC': '1',
        'Origin': 'http://www.italgiure.giustizia.it',
        'Referer': 'http://www.italgiure.giustizia.it/sncass/',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def start_requests(self):
        self.proxies = False
        if self.settings.get('PROXY'):
            self.proxies = {
                'http': self.settings.get('PROXY'),
                'https': self.settings.get('PROXY'),
            }
            self.logger.info(f'Proxy detected, Using proxies')

        url = 'http://www.italgiure.giustizia.it/sncass/'
        if self.settings.get('PROXY'):
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers=self.headers,
                meta={
                    'proxy': settings.get('PROXY'),
                })
        else:
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers=self.headers,
                meta={

                })

    def parse(self, response):
        boxes = response.xpath('//*[@data-role="keylist"]')
        for box in boxes:
            arg = box.xpath('./@data-arg').get('')
            # if 'tipoprov' not in arg:
            #     continue
            name = box.xpath('./@data-label').get('')
            self.logger.info(f'Working on {name} ==> {arg}')

            data = f'facet.method=enum&facet.mincount=1&wt=json&indent=off&q=(kind:%22snciv%22%20OR%20kind:%22snpen%22)&fl=name&facet=true&facet.limit=257&facet.sort=false&facet.prefix=&facet.field={arg}'
            request_url = 'http://www.italgiure.giustizia.it/sncass/isapi/hc.dll/sn.solr/sn-collection/select?app.facet'
            # resp = requests.post(request_url, headers=self.headers_facet, data=data, verify=False)
            resp = self.load_post_request(url=request_url, data=data, headers=self.headers_facet, proxies=self.proxies)
            facet_fields = json.loads(resp)['facet_counts']['facet_fields'][arg]
            for i in range(1, len(facet_fields), 2):
                facet_name = facet_fields[i - 1]

                facet_count = facet_fields[i]
                self.logger.info(f'Working on {facet_name} ==> {facet_count}')
                listing_url = 'http://www.italgiure.giustizia.it/sncass/isapi/hc.dll/sn.solr/sn-collection/select?app.query'

                for i in range(0, int(facet_count), 1000):
                    start = i
                    end = i + 1000
                    self.logger.info(f'Working on {facet_name} ==> Page {start} - {end}')
                    payload = f'start={start}&rows={end}&q=((kind%3A%22snciv%22%20OR%20kind%3A%22snpen%22))%20AND%20{arg}%3A%22{facet_name}%22&wt=json&indent=off&sort=pd desc,numdec desc&fl=id%2Cfilename%2Cszdec%2Ckind%2Cssz%2Ctipoprov%2Cnumcard%2Cnumdec%2Cnumdep%2Cdatdep%2Cecli%2Canno%2Cdatdec%2Cpresidente%2Crelatore%2Ctestoocr%2Cocr&hl=true&hl.snippets=4&hl.fragsize=100&hl.fl=ocr&hl.q=nomatch%20AND%20{arg}%3A%22{facet_name}%22&hl.maxAnalyzedChars=1000000&hl.simple.pre=%3Cem%20class%3D%22hit%22%3E&hl.simple.post=%3C%2Fem%3E'
                    try:
                        resp = self.load_post_request(url=listing_url, data=payload, headers=self.headers_facet,
                                                      verify=False, proxies=self.proxies)
                        items = json.loads(resp)['response']['docs']
                        for ii, item in enumerate(items):
                            self.logger.info(f'Working on {facet_name} ==> Item Num {item["numdec"]} {ii}/{len(items)}')
                            # {"language": "it", "section": "prima penale", "country": "Italy", "type": "decreto", "text": "long legal text example"}
                            pdf_url = f'http://www.italgiure.giustizia.it/xway/application/nif/clean/hc.dll?verbo=attach&db=snciv&id={item["filename"][0]}'.replace(
                                '.pdf', '.clean.pdf')
                            if 'in fase di oscuramento' in item['ocr']:
                                pdf_url = ''
                            try:
                                date = item['datdep'][0]
                                # 20220324
                                date = datetime.strptime(date, '%Y%m%d').strftime('%d/%m/%Y')
                            except:
                                date = ''

                            result = {
                                'language': 'it',
                                'country': 'Italy',
                                'category': name,
                                'subcategory': facet_name,
                                'count': facet_count,
                                'type': item['kind'],
                                'numdec': item['numdec'],
                                'date': date,
                                'pdf_url': pdf_url,
                                'text': item['ocr'],
                            }

                            result = self.handle_pdf(result)
                            yield result;
                            self.logger.info(f'ok Saving')
                    except Exception as e:
                        self.logger.error(e)

    def handle_pdf(self, result):

        if not result['pdf_url']:
            result['text'] = ''
            return result

        # '20220324/snciv@s61@a2022@n09689@tO.clean.pdf'
        filename = result["pdf_url"].split('./')[-1].replace('/', ' ').replace('@', ' ')
        filename = f'./pdf/{filename}'

        # download pdf
        self.download_pdf(url=result['pdf_url'], filename=filename)

        # extract text from pdf
        logging.getLogger("pdfminer").setLevel(logging.WARNING)

        try:
            text = extract_text(filename)
        except Exception as e:
            self.logger.error(f'error when extracting pdf ==> {e}')
            text = ''
        result['text'] = text
        return result

    def download_pdf(self, url, filename):
        self.headers = Headers(browser="chrome", os="win", headers=True).generate()
        completed = False
        retry_times = 5
        while not completed:
            try:
                if os.path.isfile(filename) == False:
                    folder_path = '/'.join(filename.split('/')[:-1])
                    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
                    filename_final_path = filename
                    if self.proxies:
                        response = requests.get(url, stream=True, headers=self.headers, proxies=self.proxies)
                    else:
                        response = requests.get(url, stream=True, headers=self.headers)
                    if response.status_code == 200:
                        with open(filename_final_path, 'wb') as f:
                            response.raw.decode_content = True
                            shutil.copyfileobj(response.raw, f)
                        response.raw.decode_content = False
                        self.logger.info(f' PDF Download complete:{filename_final_path}')

                    if os.path.getsize(filename) / 1024.0 < 10 and retry_times > 0:
                        os.remove(filename)
                        self.logger.warn(f'Captcha detected, Trying again.')
                        completed = False
                    else:
                        completed = True



                else:
                    self.logger.warn(f' PDF already downloaded:{filename}')
            except Exception as e:
                self.logger.error(f'Couldnot download the pdf: {e}')
            retry_times -= 1

    def load_post_request(self, **kwargs):
        '''
        retry_times: optional, default 3
        url: required
        data: required
        headers: required
        verify: optional, default True
        proxies: optional, default False
        '''
        kwargs['headers']['User-Agent'] = Headers(browser="chrome", os="win", headers=True).generate()['User-Agent']
        retry_times = kwargs.get('retry_times', 5)
        while retry_times > 0:
            try:
                if kwargs.get('proxies', False):
                    proxies = kwargs.get('proxies')
                    resp = requests.post(kwargs['url'], headers=kwargs['headers'], data=kwargs['data'],
                                         verify=kwargs.get('verify', True), proxies=proxies)
                else:
                    resp = requests.post(kwargs['url'], headers=kwargs['headers'], data=kwargs['data'],
                                         verify=kwargs.get('verify', True))
                if resp.status_code == 200:
                    return resp.text
            except Exception as e:
                print('Error when loading the post request', e)
            retry_times -= 1
        return ''


if __name__ == "__main__":  # if the script is ran directly
    # IMPORTANT Disclaimer: For us this script did not work well enough, that's why we don't include this data
    settings = get_project_settings()

    process = CrawlerProcess(settings)
    process.crawl(ItalgiureGiustizia)  # start scraper
    process.start()
