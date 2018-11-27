import pandas as pd
import json
import time
import random
import bs4
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, Firefox
from pymongo import MongoClient

mc = MongoClient()
db = mc['IFFD']
fc = db['followers'] #followers collection



def get_info(url):
    browser = Chrome()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sel = "meta"
    s = soup.find_all(sel, attrs={'name': 'description'})

    # find user name
    user_name = s[0]["content"].split()[-1].replace("(@", "").replace(")", "")
    # find full name
    full_name = soup.find("title").text.split("(@")[0].replace("\n", "")
    #num posts
    num_posts = s[0]["content"].split()[4]
    # find number of followers
    num_followers = s[0]["content"].split()[0]
    # find number of following by
    num_followings = s[0]["content"].split()[2]
    return user_name, full_name, num_posts, num_followers, num_followings


def write_info(url):
    # filename = "users_data.csv"
    # f = open(filename, "w")
    # headers = "user_name, full_name, num_posts, num_followed_by, num_following_by\n"
    # f.write(headers)
    # for url in urls:
    user_name, full_name, num_posts, num_followers, num_followings = get_info(url)
    f.write(user_name + ',' + full_name + ',' + str(num_posts) + ',' + str(num_followers) + ',' + str(num_followings) + "\n")
    # f.close()

def scroll_to_last_follower(browser=browser, sel="li.wo9IH"):
    followers = browser.find_elements_by_css_selector(sel)
    len(followers)
    last_follower = followers[-1]
    last_follower.location_once_scrolled_into_view

def get_followers(browser=browser, sel="li.wo9IH", n=5, wait_time=5):
    for i in range(n):
        scroll_to_last_follower()
        time.sleep(wait_time)
    followers = browser.find_elements_by_css_selector(sel)
    follower_urls = [get_follower_url(follower) for follower in followers]
    return follower_urls

def get_follower_url(follower):
    link = follower.find_element_by_css_selector('a.FPmhX')
    return link.get_attribute('href')




def add_url_to_fc(url):
    if fc.count_documents({'url': url}) > 0:
        return False
    fc.insert_one({'url': url})
    return True
