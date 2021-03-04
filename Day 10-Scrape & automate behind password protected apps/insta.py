import os
from time import sleep
from urllib.parse import urlparse

import requests
from decouple import config
from selenium import webdriver

from conf import GECKODRIVER_PATH


browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
url = 'https://www.instagram.com'
browser.get(url)
print(browser.current_url)

sleep(1)
username = browser.find_element_by_name("username")
username.send_keys(config('INSTA_USERNAME'))

username = browser.find_element_by_name("password")
username.send_keys(config('INSTA_PASSWORD'))

print('Logging in ...')

sleep(1)
login = browser.find_element_by_css_selector("button[type='submit']")
login.click()

sleep(3.1)
print('Logged in ...')


def automate_follow(browser, follow_user: str):
    # it will click the first follow btn of page
    sleep(2)
    follow_btn_xpath = ("//button[contains(text(), 'Follow')]")
    follow_btn = browser.find_element_by_xpath(follow_btn_xpath)
    print(follow_btn)

    sleep(2)
    try:
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
# automate_follow(browser, follow_user=user)


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


def automate_comment(browser, content="That is cool!"):
    sleep(10)
    comment_xpath = "//textarea[contains(@placeholder, 'Add a comment…')]"
    comment_element = browser.find_element_by_xpath(comment_xpath)
    comment_element.send_keys(content)
    print('commenting on the post ...')
    post_btn_path = "button[type='submit']"
    post_btn_elements = browser.find_elements_by_css_selector(post_btn_path)
    sleep(2)
    for btn in post_btn_elements:
        try:
            btn.click()
        except Exception:
            pass


# automate_comment(browser=browser)
