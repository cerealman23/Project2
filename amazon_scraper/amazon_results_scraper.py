# sample project from https://medium.com/analytics-vidhya/scraping-amazon-results-with-selenium-and-python-547fc6be8bfa

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By #i added this bc selenium removed find_element_by_id and replaced with generic find_element
from selectorlib import Extractor
import requests
import json
import time
from bs4 import BeautifulSoup

#take the string for the item we want to search for on Amazon as an input
def search_amazon(item):
    #Using webdriver-manager we’ll install the correct version of the ChromeDriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #load the Amazon homepage
    driver.get('https://www.amazon.com')

    #Input the name of the item(s) we want to search for into the search bar
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox').send_keys(item)

    #Click the search button
    search_button = driver.find_element(By.ID, "nav-search-submit-text").click()

    #wait for the website to actually load the first page of results or else we will get errors 
    driver.implicitly_wait(5)

    # try:
    #     num_page = driver.find_element(By.XPATH, '//*[@class="a-pagination"]/li[6]')
    # except NoSuchElementException:
    #     num_page = driver.find_element(By.CLASS_NAME, 'a-last').click()

    #get num pages
    # try:
    #     num_page = driver.find_element(By.XPATH, '//*[@class="a-pagination"]/li[6]')
    #     num_page = driver.find_element(By.XPATH, '//*[@class="s-pagination"]/li[6]')#amazon changed their html so we cant go by list item anymore
    # except NoSuchElementException:
    #     num_page = driver.find_element(By.CLASS_NAME, 'a-last').click()
    #     num_page = driver.find_element(By.CLASS_NAME, 's-pagination-item s-pagination-diabled').click()#maybe we can hardcode 2 pages in for testing
    
    num_page = 2 #TESTCODE

    driver.implicitly_wait(3)

    #Iterate through every pages collecting url
    url_list = []

    #for i in range(int(num_page.text)):
    for i in range(num_page):
        page_ = i + 1
        url_list.append(driver.current_url)
        driver.implicitly_wait(4)
#        click_next = driver.find_element(By.CLASS_NAME, 'a-last').click()
        #click_next = driver.find_element(By.CLASS_NAME, 's-pagination-item').click()
        print("Page " + str(page_) + " grabbed")

    #after we get results
    driver.quit()

    #write urls to file
    with open('search_results_urls.txt', 'w') as filehandle:
        for result_page in url_list:
            filehandle.write('%s\n' % result_page)
    print("---DONE---")

#Navigate to the results page for the item(s)
def scrape(url):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

search_amazon('headphones') # <------ search query goes here.

# courtesy of https://github.com/scrapehero-code/amazon-scraper
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')

# product_data = []
with open("search_results_urls.txt",'r') as urllist, open('search_results_output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url)
        if data:
            for product in data['products']:
                product['search_url'] = url
                print("Saving Product: %s"%product['title'].encode('utf8'))
                json.dump(product,outfile)
                outfile.write("\n")
                # sleep(5)
