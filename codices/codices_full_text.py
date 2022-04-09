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


driver1 = webdriver.Chrome(options=options)
wait = WebDriverWait(driver1, 20)
driver1.maximize_window()


driver1.get('http://www.codices.coe.int/NXT/gateway.dll?f=templates&fn=default.htm')

time.sleep(10)
driver1.switch_to.frame(driver1.find_element_by_css_selector("iframe[title='Table of Contents']"))


wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.rootchildrennode li'))).click()
time.sleep(2)

driver1.find_element_by_id('CODICES/full').find_element_by_css_selector('a').click()

main_dictionary = {'Full texts':[]}

try:

    for ind , region in enumerate(driver1.find_element_by_id('CODICES/full_c').find_elements_by_xpath('/html/body/div/div[1]/div[2]/div[2]/div/ul/li/ul/li[7]/ul/li')):
        region_name = region.text
        region.find_element_by_css_selector('a.plusminus').click()
        time.sleep(1)
        main_dictionary['Full texts'].append({region_name:[]})

        for index ,states in enumerate(region.find_elements_by_xpath('ul/li')):
            state_name = states.text
            main_dictionary['Full texts'][ind][region_name].append({state_name:[]})
            states.find_element_by_css_selector('a.plusminus').click()
            time.sleep(0.5)

            for index2,county  in enumerate(states.find_elements_by_xpath('ul/li')):
                county_name = county.text
                main_dictionary['Full texts'][ind][region_name][index][state_name].append({county_name:[]})
                county.find_element_by_css_selector('a.plusminus').click()
                time.sleep(0.5)

                while True:
                    if county.find_elements_by_xpath('ul/li')[-1].find_element_by_css_selector('a img').get_attribute('alt') == 'Expand Node':
                        county.find_elements_by_xpath('ul/li')[-1].find_element_by_css_selector('a').click()
                        time.sleep(1)
                    else:
                        break

                for index3 , article in enumerate(county.find_elements_by_xpath('ul/li')):
                    article.find_element_by_css_selector('a.nodetext').click()
                    time.sleep(0.25)
                    """switch to default content """
                    driver1.switch_to.default_content()
                    # time.sleep(1)
                    """Click to second  iframe """
                    driver1.switch_to.frame(driver1.find_element_by_id('document-frameset'))
                    # time.sleep(1.5)
                    # time.sleep(1)
                    # data = driver.find_element_by_css_selector('div.WordSection1').text
                    main_dictionary['Full texts'][ind][region_name][index][state_name][index2][county_name].append(driver1.find_element_by_css_selector('body').text)

                    """switch to default content """
                    driver1.switch_to.default_content()

                    driver1.switch_to.frame(driver1.find_element_by_css_selector("iframe[title='Table of Contents']"))
                    time.sleep(0.5)



                county.find_element_by_css_selector('a.plusminus').click()
                time.sleep(2.5)
            states.find_element_by_css_selector('a.plusminus').click()
            time.sleep(2.5)
        region.find_element_by_css_selector('a.plusminus').click()
        time.sleep(2.5)

    driver1.close()
    with open("full_text_rest_europe.json", "w") as outfile:
        json.dump(main_dictionary, outfile)
except:
    pass

    # for state in region.find_elements_by_xpath('/ul')



