## Import libraries
import json
import jsonlines
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Parameters initialization
PATH_CHROME = "C:\Program Files (x86)\Selenium\chromedriver.exe"
domain_name = 'https://www.retsinformation.dk'
lang = 'dk'
ID = 0


## Misc functions
def pages(number):
    url = 'https://www.retsinformation.dk/documents?dt=230&dt=240&dt=250&dt=260&dt=980&page='+str(number)+'&ps=100'
    return url

def date_iso_format(date):
    # dd/mm/yyyy  -->  yyyy-mm-dd
    tmp = date.split('/')
    y = tmp[2]
    m = tmp[1]
    d = tmp[0]
    return y + "-" + m + "-" + d

def create_article_JSON(article_soup, url, ID): 
    # HTML for decision's date
    tmp_html = article_soup.find('h5', {'class' : 'd-sm-inline m-0 mr-sm-2'})
    tmp = tmp_html.text
    tmp = tmp[len(tmp)-10:]
    date_decision = date_iso_format(tmp)

    # HTML for cleaned text
    text_html = article_soup.find(class_="restyling-html")
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
waitTime = 1
list_articles_html = []
for page_number in range(0,30):
    driver.get(pages(page_number))
    time.sleep(waitTime)
    pages_html = BeautifulSoup(driver.page_source, "html.parser")
    tmp_html = pages_html.find_all(class_="document-title")
    list_articles_html = list_articles_html + tmp_html[1:]

stat_elapsed_time = time.time_ns()
stat_number_articles = len(list_articles_html)
stat_articles_length = []
waitTime = 1
# Scrape articles and generate their corresponding JSON objects
for article_html in list_articles_html:
    tmp = BeautifulSoup(str(article_html), "html.parser")
    url = domain_name + tmp.find("a")["href"]
    driver.get(url)
    time.sleep(waitTime)
    tmp = BeautifulSoup(driver.page_source, "html.parser")
    try:
        ID = ID+1
        article_JSON = create_article_JSON(tmp, url, ID)
        articles_JSON.append(article_JSON)
        stat_articles_length.append(len(article_JSON['text']))
    except:
        ID = ID-1
    # Comment in/out for testing (to only consider 10 articles)
    # if (ID > 10):
    #    break

stat_elapsed_time = (time.time_ns() - stat_elapsed_time)*10**(-9)
stat_average_characters = sum(stat_articles_length)/stat_number_articles

## Release resources
driver.quit()

## Create and initialize a JSONL-Data
# fileName = "DBWebsite6.json"
# file = open(fileName, "w", encoding='utf8')
# json.dump(articles_JSON, file, ensure_ascii=False)
# file.close()
fileName = "DBWebsite6.jsonl"
writer = jsonlines.open(fileName, 'w')
for article in articles_JSON:
    writer.write(article)
writer.close()

## Statistics
print("Elapsed time: "+str(stat_elapsed_time))
print("Average elapsed time pro article: "+str(stat_elapsed_time/stat_number_articles))
print("Number of articles: "+str(stat_number_articles))
print("Average characters pro article: "+str(stat_average_characters))