## Import libraries
import json
import jsonlines
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Parameters initialization
PATH_CHROME = "C:\Program Files (x86)\Selenium\chromedriver.exe"
domain_name = 'http://www.bailii.org'
pages = 'http://www.bailii.org/ew/cases/EWCA/Civ/2019/'
lang = 'en'
ID = 0

## Misc functions
month_number={
        "january":"01",
        "february":"02",
        "march":"03",
        "april":"04",
        "may":"05",
        "june":"06",
        "july":"07",
        "august":"08",
        "september":"09",
        "october":"10",
        "november":"11",
        "december":"12"
}

def date_iso_format(date):
    # 8 May 2018 --> 2018-05-08
    # ["8","May","2018"]
    tmp = date.split(' ')
    if len(tmp)==3:
        y = tmp[2]
        m = month_number[tmp[1].lower()]
        d = tmp[0]
        return y + "-" + m + "-" + d
    # 08/05/2018 --> 2018-05-08
    # ["08","05","2018"]
    tmp = date.split('/')
    if len(tmp)==3:
        y = tmp[2]
        m = tmp[1]
        d = tmp[0]
        return y + "-" + m + "-" + d
    else:
        print("Date format: unknown ["+date+"]")

def create_article_JSON(article_soup, url, ID):
    # HTML for decision's date
    date_html = article_soup.find('date')
    if date_html is None:
        date_decision = ""
    else:
        date_decision = date_html.text 
        date_decision = date_iso_format(date_decision) 

    # HTML for cleaned text
    text_html = article_soup.find('ol')
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
waitTime = 0.1
options = Options()
options.headless = True
driver = webdriver.Chrome(PATH_CHROME, chrome_options=options)

## JSON Database
articles_JSON = []
# Build list of articles' URLs
driver.get(pages)
time.sleep(waitTime)
pages_html = BeautifulSoup(driver.page_source, "html.parser")
list_articles_html = pages_html.find_all("li")

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

## Create and initialize a JSONL-Data
# fileName = "DBWebsite4.json"
# file = open(fileName, "w", encoding='utf8')
# json.dump(articles_JSON, file, ensure_ascii=False)
# file.close()
fileName = "DBWebsite4.jsonl"
writer = jsonlines.open(fileName, 'w')
for article in articles_JSON:
    writer.write(article)
writer.close()

## Statistics
print("Elapsed time: "+str(stat_elapsed_time))
print("Average elapsed time pro article: "+str(stat_elapsed_time/stat_number_articles))
print("Number of articles: "+str(stat_number_articles))
print("Average characters pro article: "+str(stat_average_characters))