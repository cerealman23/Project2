#!/usr/bin/env python3

class Reviewer:

  def __init__(self, score, verified, long_review, image_profile):
    self.score = score
    # self.profile_picture = profile_picture
    self.verified = verified
    self.long_review = long_review
    self.image_profile = image_profile

# If they have a image they are credible
# If they have a high amazon score they are better off DONE
# Long reviews score better
# make sure they are a verified purchaser
# the more people who find it helpful the better

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
import random

def search_account(item):

  driver = webdriver.Chrome(ChromeDriverManager().install())
  #load the Amazon homepage
  driver.get('https://www.amazon.com/Disney-Friends-Leopard-Portrait-T-Shirt/dp/B082BXV2F3/ref=lp_21417004011_1_4')
  #Input the name of the item(s) we want to search for into the search bar

  driver.implicitly_wait(5)
  # search for headphones by clicking them.
  search_box = driver.find_element(By.ID, 'acrCustomerReviewText').click()

  reviewers = []

  #  This finds the butten that goes to the recview page
  profile = driver.find_element(By.XPATH, "//div[@id='reviews-medley-footer']/div[@class='a-row a-spacing-medium']/a").click()

  # all profiles on one page
  profiles = driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")
  reviews = driver.find_elements(By.XPATH,"//div[@class='a-section review aok-relative']")
  reviews_body = driver.find_elements(By.XPATH, "//div/span[@data-hook='review-body']")

  scores = []

  for i in range(len(profiles)):

    review = driver.find_elements(By.XPATH,"//div[@class='a-section review aok-relative']")[i]
    # verified = review.find_element(By.LINK_TEXT, 'Verified Purchase')
    body = review.find_elements(By.XPATH, "//div/span[@data-hook='review-body']")[i]

    body_size = len(body)

    # Have to reset in order to not get a stale element reference
    item = driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")[i]
    item.click()
    # gets the score from one reviewer and adds it to the data list
    data = driver.find_element(By.XPATH, "//span[@class='impact-text']")
    scores.append(data.text)

    profile_pic = driver.find_element(By.ID, "avatar-image")

    # if 'https://www.amazon.com/avatar/default/' in profile_pic.get_attribute("src"):
    #   avatar = False
    driver.back()
    # so IP does not get blocked
    delay = random.randrange(1, 5)
    driver.implicitly_wait(delay)
    # driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")


  # time.sleep(10)

  print(scores)

  driver.quit()


  #Click the search button

search_account("headphones")
