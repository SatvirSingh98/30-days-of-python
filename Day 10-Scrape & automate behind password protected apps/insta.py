import os
from time import sleep
from urllib.parse import urlparse

import requests
from decouple import config
from selenium import webdriver

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

    print('Logging in ...')

    sleep(0.4)
    login = browser.find_element_by_css_selector("button[type='submit']")
    login.click()

    sleep(3.1)
    # not_now_element1 = browser.find_element_by_class_name("cmbtv")
    # not_now_button1 = not_now_element1.find_element_by_tag_name('button')
    # not_now_button1.click()
    # or

    print('Logged in ...')

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


def automate_follow(browser, follow_user: str):
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

        print(f'Following: {follow_user}')

    except Exception:
        print(f'Already following: {follow_user}')

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


user = 'therock'
new_user_url = f"https://www.instagram.com/{user}/"
browser.get(new_user_url)
automate_follow(browser, follow_user=user)


# post_url_pattern = "https://www.instagram.com/ted/p/<post_slug_id>"
post_xpath_str = "//a[contains(@href, '/p/')]"
post_links = browser.find_elements_by_xpath(post_xpath_str)

sleep(1)
print('Reading posts ...')

post_link_element = None
if len(post_links) > 0:
    post_link_element = post_links[0]

if post_link_element is not None:
    post_href = post_link_element.get_attribute('href')

    sleep(1)
    print('Scraping the latest post ...')

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
VIDEO_DIR = os.path.join(DATA_DIR, 'videos')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def scrape_and_save(elements, directory):
    for el in elements:
        url = el.get_attribute('src')
        base_url = urlparse(url).path
        # print(base_url)
        filename = os.path.basename(base_url)
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            continue

        with requests.get(url, stream=True) as r:
            try:
                r.raise_for_status()
            except Exception:
                continue

            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)


# scrape_and_save(elements=img_elements, directory=IMG_DIR)
# scrape_and_save(elements=video_elements, directory=VIDEO_DIR)
