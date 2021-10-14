from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import username, password
import os
import time


APPLICATION_PATH = os.path.dirname(__file__)
driver = webdriver.Chrome(APPLICATION_PATH + '/chromedriver')

driver.get('http://149.7.16.11:8840/login')

username_field = driver.find_element_by_id("Username")
password_field = driver.find_element_by_id("Password")

username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)


time.sleep(3)
driver.quit()