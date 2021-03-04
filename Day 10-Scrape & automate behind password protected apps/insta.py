from decouple import config
from selenium import webdriver
from time import sleep
from conf import GECKODRIVER_PATH


browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
url = 'https://www.instagram.com'
browser.get(url)

sleep(0.4)
username = browser.find_element_by_name("username")
username.send_keys(config('INSTA_USERNAME'))

username = browser.find_element_by_name("password")
username.send_keys(config('INSTA_PASSWORD'))

sleep(0.4)
submit_element = browser.find_element_by_css_selector("button[type='submit']")
submit_element.click()

sleep(3.1)
# not_now_element1 = browser.find_element_by_class_name("cmbtv")
# not_now_button1 = not_now_element1.find_element_by_tag_name('button')
# not_now_button1.click()
# or
not_now_xpath1 = "//button[contains(text(), 'Not Now')]"
not_now_btn1 = browser.find_element_by_xpath(not_now_xpath1)
not_now_btn1.click()

sleep(1)
# not_now_element2 = browser.find_element_by_class_name("mt3GC")
# not_now_button2 = not_now_element2.find_element_by_css_selector(
#     "button[class='aOOlW   HoLwm ']")
# not_now_button2.click()
not_now_xpath2 = "//button[contains(text(), 'Not Now')]"
not_now_btn2 = browser.find_element_by_xpath(not_now_xpath2)
not_now_btn2.click()


# if we want to click everything having text 'not now':
# xpath = "//*[contains(text(), 'Not Now')]"
