## Import libraries
import jsonlines
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Parameters initialization
PATH_CHROME = "C:\Program Files (x86)\Selenium\chromedriver.exe"
domain_name = 'https://www.legifrance.gouv.fr'
lang = 'fr'
ID = 0

## Misc functions
def pages(number):
    url = 'https://www.legifrance.gouv.fr/search/juri?tab_selection=juri&searchField=ALL&query=*&searchType=ALL&typePagination=DEFAULT&sortValue=DATE_DESC&pageSize=100&page='+str(number)+'&tab_selection=juri#juri'
    return url

month_number={
        "janvier":"01",
        "février":"02",
        "mars":"03",
        "avril":"04",
        "mai":"05",
        "juin":"06",
        "juillet":"07",
        "août":"08",
        "septembre":"09",
        "octobre":"10",
        "novembre":"11",
        "décembre":"12"
}

def date_iso_format(date):
    # 18 avril 2019 --> 2019-04-18
    tmp = date.split(' ')
    y = tmp[2]
    m = month_number[tmp[1]]
    d = tmp[0]
    return y + "-" + m + "-" + d

def create_article_JSON(article_soup, url, ID):
    # HTML for decision's date
    date_html = article_soup.find(class_=['titreLecture'])
    tmp = date_html.span.text
    date_decision = date_html.span.text[tmp.index(", du ")+5:len(tmp)]
    date_decision = date_iso_format(date_decision)

    # HTML for cleaned text
    text_html = article_soup.find(class_=['content-page'])
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
list_articles_html = []
for page_number in range(1,100):
    driver.get(pages(page_number))
    time.sleep(waitTime)
    pages_html = BeautifulSoup(driver.page_source, "html.parser")
    list_articles_html = list_articles_html + pages_html.find_all(class_="title-result-item")

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
    try:
        ID = ID+1
        article_JSON = create_article_JSON(tmp, url, ID)
        articles_JSON.append(article_JSON)
        stat_articles_length.append(len(article_JSON['text']))
    except:
        ID = ID-1
    # Comment in/out for testing (to only consider 10 articles)
    #if ID > 10:
        #break

stat_elapsed_time = (time.time_ns() - stat_elapsed_time)*10**(-9)
stat_average_characters = sum(stat_articles_length)/stat_number_articles

## Release resources
driver.quit()

## 7. Create and initialize a JSONL-Data
# fileName = "DBWebsite1.json"
# file = open(fileName, "w", encoding='utf8')
# json.dump(articles_JSON, file, ensure_ascii=False)
# file.close()
fileName = "DBWebsite1.jsonl"
writer = jsonlines.open(fileName, 'w')
for article in articles_JSON:
    writer.write(article)
writer.close()

## Statistics
print("Elapsed time: "+str(stat_elapsed_time))
print("Average elapsed time pro article: "+str(stat_elapsed_time/stat_number_articles))
print("Number of articles: "+str(stat_number_articles))
print("Average characters pro article: "+str(stat_average_characters))