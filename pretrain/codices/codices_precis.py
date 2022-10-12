from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import scrapy
import json
import unidecode

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-infobars")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
driver.maximize_window()

driver.get('http://www.codices.coe.int/NXT/gateway.dll?f=templates&fn=default.htm')

time.sleep(5)
driver.switch_to.frame(driver.find_element_by_css_selector("iframe[title='Table of Contents']"))

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.rootchildrennode li'))).click()
time.sleep(2)

driver.find_element_by_css_selector('span[title="Précis / Décisions abrégées"]').click()

driver.switch_to.default_content()

driver.switch_to.frame(driver.find_element_by_id('document-frameset'))

stop_state = driver.find_element_by_css_selector('div.A div').text

first = 1

while stop_state != 'Systematic thesaurus - Thésaurus systématique - Thesaurus sistemático':
    try:
        level1 = driver.find_element_by_css_selector('div.A div').text
        one = level1
    except:
        level1 = ""
    try:
        level2 = driver.find_element_by_css_selector('div.B div').text
        two = level2
    except:
        level2 = ""

    try:
        level3 = driver.find_element_by_css_selector('div.C div').text
        three = level3
    except:
        level3 = ""
    try:
        level4 = driver.find_element_by_css_selector('div.D div').text
        four = level4
    except:
        level4 = ""
    try:
        level5 = driver.find_element_by_css_selector('div.E').text
        five = level5
    except:
        level5 = ""

    if first == 1:
        data_dictionary = {level1: {level2: {level3: {str(level4): [level5]}}}}
        first += 1

    else:
        if level1 == "" and level2 == "" and level3 == "" and level4 == "":
            data_dictionary[one][two][three][four].append(level5)

        elif level1 == "" and level2 == "" and level3 == "":
            if level4 not in data_dictionary[one][two][three].keys():
                data_dictionary[one][two][three][str(level4)] = [level5]
        elif level1 == "" and level2 == "":
            data_dictionary[one][two][level3] = {str(level4): [level5]}

        elif level1 == "":
            data_dictionary[one][level2] = {level3: {str(level4): [level5]}}

    driver.switch_to.default_content()
    driver.find_element_by_css_selector('img[alt="Next Doc"]').click()
    time.sleep(4)
    driver.switch_to.frame(driver.find_element_by_id('document-frameset'))
    try:
        stop_state = driver.find_element_by_css_selector('div.A div').text
    except:
        pass

driver.close()
with open("Data.json", "w") as outfile:
    json.dump(data_dictionary, outfile)
