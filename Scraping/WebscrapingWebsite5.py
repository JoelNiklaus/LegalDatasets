## Import libraries
import json
import jsonlines
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Parameters initialization:
PATH_CHROME = "C:\Program Files (x86)\Selenium\chromedriver.exe"
domain_name = 'http://www.sentenze.ti.ch'
lang = 'it'
ID = 0

## Misc functions
def pages(number):
    url = 'http://www.sentenze.ti.ch/cgi-bin/nph-omniscgi?OmnisPlatform=WINDOWS&WebServerUrl=www.sentenze.ti.ch&WebServerScript=/cgi-bin/nph-omniscgi&OmnisLibrary=JURISWEB&OmnisClass=rtFindinfoWebHtmlService&OmnisServer=JURISWEB,193.246.182.54:6000&Parametername=WWWTI&Schema=TI_WEB&Source=&Aufruf=validate&Template=results%2Fresultpage_ita.fiw&cSprache=ITA&nX40_KEY=3058757&nAnzahlTrefferProSeite=5&nSeite='+str(number)
    return url

def date_iso_format(date):
    # dd.mm.yyyy  -->  yyyy-mm-dd
    tmp = date.split('.')
    y = tmp[2]
    m = tmp[1]
    d = tmp[0]
    return y + "-" + m + "-" + d

def create_article_JSON(article_soup, url, ID): 
    # HTML for decision's date
    tmp_html = article_soup.find_all("tbody")
    date_soup = BeautifulSoup(str(tmp_html[3]), "html.parser")
    date_html = date_soup.find_all("td")[3]
    date_decision = date_html.text[:10]
    date_decision = date_iso_format(date_decision)

    # HTML for cleaned text
    text_html = article_soup.find("table",{"width":"680"})
    tmp = BeautifulSoup(str(text_html), "html.parser")
    text = tmp.get_text()

    # Create and initialize article's JSON object
    article_JSON = {
        "ID" : ID,
        "URL": url,
        "language": lang,
        "date_decision": date_decision,
        "text": str(text), 
    }

    return article_JSON


## Webdriver initialization
options = Options()
options.headless = True
driver = webdriver.Chrome(PATH_CHROME, chrome_options=options)

## JSON Database
articles_JSON = []
# Build list of articles' URLs
waitTime = 0.8
list_articles_html = []
for page_number in range(1,1000):
    driver.get(pages(page_number))
    time.sleep(waitTime)
    pages_html = BeautifulSoup(driver.page_source, "html.parser")
    tmp_html = pages_html.find_all("table", {"cellpadding":"0", "cellspacing":"0","width":"100%"})
    list_articles_html = list_articles_html + tmp_html[1:]

stat_elapsed_time = time.time_ns()
stat_number_articles = len(list_articles_html)
stat_articles_length = []
waitTime = 0.1
# Scrape articles and generate their corresponding JSON objects
for article_html in list_articles_html:
    tmp = BeautifulSoup(str(article_html), "html.parser")
    url = tmp.find("a")["href"]
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

## Create and initialize a JSONL-Data
# fileName = "DBWebsite5.json"
# file = open(fileName, "w", encoding='utf8')
# json.dump(articles_JSON, file, ensure_ascii=False)
# file.close()
fileName = "DBWebsite5.jsonl"
writer = jsonlines.open(fileName, 'w')
for article in articles_JSON:
    writer.write(article)
writer.close()

## Statistics
print("Elapsed time: "+str(stat_elapsed_time))
print("Average elapsed time pro article: "+str(stat_elapsed_time/stat_number_articles))
print("Number of articles: "+str(stat_number_articles))
print("Average characters pro article: "+str(stat_average_characters))