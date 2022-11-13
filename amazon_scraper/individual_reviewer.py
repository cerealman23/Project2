#!/usr/bin/env python3

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By #i added this bc selenium removed find_element_by_id and replaced with generic find_element
from selenium.webdriver.common.keys import Keys
from selectorlib import Extractor
import requests
import json
import time
from bs4 import BeautifulSoup

def search_account(item):

  driver = webdriver.Chrome(ChromeDriverManager().install())
  #load the Amazon homepage
  driver.get('https://www.amazon.com/jbl-230nc-wireless-cancelling-headphones/dp/B09FM6PDHP/ref=sr_1_12?crid=NNNHTRCN0930&keywords=headphones&qid=1668290376&sprefix=%2Caps%2C57&sr=8-12&th=1')
  #Input the name of the item(s) we want to search for into the search bar

  driver.implicitly_wait(5)
  # try:
  search_box = driver.find_element(By.ID, 'acrCustomerReviewText').click()
  # except NoSuchElementException:
  #   search_box = driver.find_element(By.ID, 'acrCustomerReviewLink').click()


  reviewers = []


  profile = driver.find_element(By.XPATH, "//div[@id='reviews-medley-footer']/div[@class='a-row a-spacing-medium']/a").click()

  # profiles = driver.find_element(By.XPATH, "//div[@class='a-fixed-right-grid-col a-col-left']/div[@data-hook='gneome-widget']/a")
  profiles = driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")
  # profiles = driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")


  scores = []


  for i in range(len(profiles)):
    item = driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")[i]
    item.click()
    data = driver.find_element(By.XPATH, "//span[@class='impact-text']")
    scores.append(data.text)
    driver.back()
    driver.implicitly_wait(2)
    # driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")


  # time.sleep(10)

  print(scores)

  driver.quit()


  #Click the search button

search_account("headphones")
