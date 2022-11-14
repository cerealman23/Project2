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

def search_account(link):

  driver = webdriver.Chrome(ChromeDriverManager().install())
  #load the Amazon homepage
  driver.get(link)
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

  pagesToReview = 3

  while pagesToReview != 0:
    for i in range(len(profiles)):

      # Have to reset in order to not get a stale element reference
      item = driver.find_elements(By.CSS_SELECTOR, "div[data-hook=genome-widget] > a")[i]
      item.click()
      # gets the score from one reviewer and adds it to the data list
      data = driver.find_element(By.XPATH, "//span[@class='impact-text']")
      scores.append(data.text)

      driver.back()
      # so IP does not get blocked
      delay = random.randrange(1, 5)
      #driver.implicitly_wait(delay)
      time.sleep(delay)
    
    try:
      #click next page 
      item = driver.find_element(By.XPATH, '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
      item.click()
    except NoSuchElementException:
      pagesToReview = 0
    #except IndexError:
     # pagesToReview = False



  # time.sleep(10)

  print(scores)

  driver.quit()


  #Click the search button

search_account('https://www.amazon.com/Tile-Bluetooth-Battery-Water-Resistant-Compatible/dp/B09998MBFM/ref=pd_rhf_d_cr_s_pd_crcbs_sccl_1_4/144-4848069-3917667?pd_rd_w=74mOJ&content-id=amzn1.sym.31346ea4-6dbc-4ac4-b4f3-cbf5f8cab4b9&pf_rd_p=31346ea4-6dbc-4ac4-b4f3-cbf5f8cab4b9&pf_rd_r=MYJNY1DP9B6JWEJ04Z98&pd_rd_wg=3mMqY&pd_rd_r=5a2be869-d094-4602-83ed-0cb4467c0df9&pd_rd_i=B09998MBFM&psc=1')
