import os
import requests
from decouple import config
from selenium import webdriver
from time import sleep
from conf import GECKODRIVER_PATH


browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
# url = 'https://www.instagram.com'
# browser.get(url)


def insta_login(browser):
    sleep(0.4)
    username = browser.find_element_by_name("username")
    username.send_keys(config('INSTA_USERNAME'))

    username = browser.find_element_by_name("password")
    username.send_keys(config('INSTA_PASSWORD'))

    sleep(0.4)
    login = browser.find_element_by_css_selector("button[type='submit']")
    login.click()

    sleep(3.1)
    # not_now_element1 = browser.find_element_by_class_name("cmbtv")
    # not_now_button1 = not_now_element1.find_element_by_tag_name('button')
    # not_now_button1.click()
    # or
    try:
        not_now_xpath1 = "//button[contains(text(), 'Not Now')]"
        not_now_btn1 = browser.find_element_by_xpath(not_now_xpath1)
        not_now_btn1.click()
    except Exception:
        pass

    sleep(1)
    # not_now_element2 = browser.find_element_by_class_name("mt3GC")
    # not_now_button2 = not_now_element2.find_element_by_css_selector(
    #     "button[class='aOOlW   HoLwm ']")
    # not_now_button2.click()
    try:
        not_now_xpath2 = "//button[contains(text(), 'Not Now')]"
        not_now_btn2 = browser.find_element_by_xpath(not_now_xpath2)
        not_now_btn2.click()
    except Exception:
        pass


# if we want to click everything having text 'not now':
# xpath = "//*[contains(text(), 'Not Now')]"

body_element = browser.find_element_by_css_selector('body')
html_txt = body_element.get_attribute('innerHTML')
# print(html_txt)


def automate_follow(browser):
    # it will click the first follow btn of page
    follow_btn_xpath = ("//button[contains(text(), 'Follow')]")
    # "[not(contains(text(), 'Following')]")
    follow_btn = browser.find_element_by_xpath(follow_btn_xpath)
    sleep(2)
    try:
        follow_btn.click()
        insta_login(browser)
        follow_btn = browser.find_element_by_xpath(follow_btn_xpath)
        sleep(2)
        follow_btn.click()
    except Exception:
        pass

    # it will click all the follow buttons on the page
    # my_follow_btn = ("//button[contains(text(), 'Follow')]"
    #                  "[not(contains(text(), 'Following')]")
    # follow_btn_elements = browser.find_elements_by_xpath(my_follow_btn)

    # for btn in follow_btn_elements:
    #     sleep(2)  # to avoid overloading
    #     try:
    #         btn.click()
    #     except Exception:
    #         pass


new_user_url = "https://www.instagram.com/therock/"
browser.get(new_user_url)
automate_follow(browser)


# post_url_pattern = "https://www.instagram.com/ted/p/<post_slug_id>"
post_xpath_str = "//a[contains(@href, '/p/')]"
post_links = browser.find_elements_by_xpath(post_xpath_str)

post_link_element = None
if len(post_links) > 0:
    post_link_element = post_links[0]

if post_link_element is not None:
    post_href = post_link_element.get_attribute('href')
    browser.get(post_href)

# scrapping video and image elements of top element
# video_element = browser.find_element_by_xpath("//video")
# img_element = browser.find_element_by_xpath("//img")


# scrapping all the videos and images elements
video_elements = browser.find_elements_by_xpath("//video")
img_elements = browser.find_elements_by_xpath("//img")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMG_DIR = os.path.join(DATA_DIR, 'images')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

for img in img_elements:
    url = img.get_attribute('src')
    filename = os.path.basename(url)
    filepath = os.path.join(IMG_DIR, f'{filename}.jpg')

    with requests.get(url, stream=True) as r:
        try:
            r.raise_for_status()
        except Exception:
            continue

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content():
                if chunk:
                    f.write(chunk)
