from selenium import webdriver
from time import sleep
from conf import CHROMEDRIVER_PATH


browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
url = 'https://google.com'
browser.get(url)

element = browser.find_element_by_name("q")
sleep(1)
element.send_keys('selenium-python')

submit_element = browser.find_element_by_css_selector("input[type='submit']")
# print(submit_element.get_attribute('name'))
sleep(1)
submit_element.click()
