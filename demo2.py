
# import libraries
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver

###########################
# Loop of all the pages
###########################

#Loop to go over all pages
pages = np.arange(1, 3, 1)
data=[]

for page in pages:
page= "https://www.legifrance.gouv.fr/juri/id/JURITEXT000044245391?init=true&page=1&query=&searchField=ALL&tab_selection=juri"
driver = webdriver.Chrome()
    driver.get(page)  
    sleep(randint(2,10))

soup = BeautifulSoup(driver.page_source, 'html.parser')
    my_table = soup.find_all(class_=['description', 'price-label body-3','price title-5',\
                                    'score orange big'])

    for tag in my_table:
        data.append(tag.get_text())