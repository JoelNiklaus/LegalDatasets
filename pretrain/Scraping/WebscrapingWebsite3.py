## Import libraries
import json
import jsonlines
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Parameters initialization:
PATH_CHROME = "C:\Program Files (x86)\Selenium\chromedriver.exe"
domain_name = 'https://www.ris.bka.gv.at'
lang = 'de'
ID = 0

## Misc functions
def pages(number):
    # The next page is 100 articles away (1->1, 2->101, 3->201, ...)
    step = 100*(number-1) + 1
    url= 'https://www.ris.bka.gv.at/Ergebnis.wxe?Abfrage=Dok&EntscheidendeBehoerde=&SucheNachRechtssatz=True&SucheNachText=True&GZ=&VonDatum=01.01.2000&BisDatum=09.12.2021&Norm=&ImRisSeitVonDatum=&ImRisSeitBisDatum=&ImRisSeit=Undefined&ResultPageSize=100&Suchworte=&Position='+str(step)
    return url

def date_iso_format(date):
    # dd.mm.yyyy  -->  yyyy-mm-dd
    return date[6:10]+"-"+date[3:5]+"-"+date[0:2]

def create_article_JSON(article_soup, url, ID):
    # HTML for decision's date
    date_html = article_soup.find_all(class_=['contentBlock'])[1]
    date_decision = date_html.p.text
    date_decision = date_iso_format(date_decision)

    # HTML for cleaned text
    text_html = article_soup.find(class_=['paperw nextpage'])
    tmp = BeautifulSoup(str(text_html), "html.parser")
    text = tmp.get_text()

    # Create and intialize article's JSON object
    article_JSON = {
        "ID" : ID,
        "URL": url,
        "language": lang,
        "date_decision": date_decision,
        "text": str(text), 
    }

    return article_JSON


## Webdriver initialization
waitTime = 0.1
options = Options()
options.headless = True
driver = webdriver.Chrome(PATH_CHROME, chrome_options=options)

## JSON Database
articles_JSON = []
# Build list of articles' URLs
list_articles_html = []
for page_number in range(1,40):
    driver.get(pages(page_number))
    time.sleep(waitTime)
    pages_html = BeautifulSoup(driver.page_source, "html.parser")
    list_articles_html = list_articles_html + pages_html.find_all(class_="nativeDocumentLinkCell")

stat_elapsed_time = time.time_ns()
stat_number_articles = len(list_articles_html)
stat_articles_length = []
# Scrape articles and generate their corresponding JSON objects
for article_html in list_articles_html:
    tmp = BeautifulSoup(str(article_html), "html.parser")
    url = domain_name + tmp.find("a")["href"]
    driver.get(url)
    time.sleep(waitTime)
    tmp = BeautifulSoup(driver.page_source, "html.parser")
    ID = ID+1
    article_JSON = create_article_JSON(tmp, url, ID)
    articles_JSON.append(article_JSON)
    stat_articles_length.append(len(article_JSON['text']))
    # Comment in/out for testing (to only consider 10 articles)
    #if (ID > 10):
        #break

stat_elapsed_time = (time.time_ns() - stat_elapsed_time)*10**(-9)
stat_average_characters = sum(stat_articles_length)/stat_number_articles

## Release resources
driver.quit()

## Create and intitialize a JSONL-Data
#fileName = "DBWebsite3.json"
#file = open(fileName, "w", encoding='utf8')
#json.dump(articles_JSON, file, ensure_ascii=False)
#file.close()
fileName = "DBWebsite3.jsonl"
writer = jsonlines.open(fileName, 'w')
for article in articles_JSON:
    writer.write(article)
writer.close()

## Statistics
print("Elapsed time: "+str(stat_elapsed_time))
print("Average elapsed time pro article: "+str(stat_elapsed_time/stat_number_articles))
print("Number of articles: "+str(stat_number_articles))
print("Average characters pro article: "+str(stat_average_characters))