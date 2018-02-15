# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import re
from selenium import webdriver


# in case old cookie method fails
def get_cookie_with_selenium():
    chromePath = "/usr/local/bin/chromedriver"
    wd = webdriver.Chrome(executable_path=chromePath)
    loginUrl = 'http://www.weibo.com/login.php'
    wd.get(loginUrl)
    wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('wanshendujiequ@yahoo.com')
    wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('Lg590219')
    wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()

    req = requests.Session()
    cookies = wd.get_cookies()
    for cookie in cookies:
        req.cookies.set(cookie["name"], cookie["value"])
    url = "https://weibo.cn/1776448504/fans?page=19&display=0&retcode=6102"
    r = req.get(url)
    print r.content


# Manually concatenate cookies from response header
def get_cookie():

    payload = {"username": "wanshendujiequ@yahoo.com",
               "password": "Lg590219",
               "savestate": "1",
               "ec": "0",
               "entry": "mweibo",
               "mainpageflag": "1"}
    headers = {"Accept-Encoding": "gzip, deflate, br",
               "Connection": "keep-alive",
               "Content-Length": "162",
               "Content-Type": "application/x-www-form-urlencoded",
               "Host": "passport.weibo.cn",
               "Origin": "https://passport.weibo.cn",
               "Referer": "https://passport.weibo.cn/signin/login",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}
    url = "https://passport.weibo.cn/sso/login"

    r = requests.post(url, data=payload, headers=headers)
    cookies_infos = r.headers["Set-Cookie"]
    cookie_parts = []

    # The method to combine cookie info
    for info in cookies_infos.split():
        if info.startswith("SUB=") or info.startswith("SUHB=") or info.startswith("SCF=") or info.startswith("SSOLoginState="):
            cookie_parts.append(info)
    cookie = " ".join(cookie_parts)
    return {"Cookie": cookie}


def get_followers(cookie, username):
    def retrive_followers_content(cookie, username):
        url = "https://weibo.cn/%s?display=0&retcode=6102" % username
        r = requests.get(url, cookies=cookie)
        return r.content

    def extract_follower_from_content(content):
        selector = etree.HTML(content)
        str_gz = selector.xpath("//div[@class='tip2']/a/text()")[1]
        pattern = r"\d+\.?\d*"
        guid = re.findall(pattern, str_gz, re.M)
        followers = int(guid[0])
        return followers

    content = retrive_followers_content(cookie, username)
    return extract_follower_from_content(content)


"""
Some links for other purposes
url = "http://energy.tv.weibo.cn/e/10173/index?display=0&retcode=6102"

Followers details:
This requires more information in cookie to access: _T_WM
I think using selenium with simulated web browser behavior it is achievable, but
1. I don't fully understand the package
2. not very familiar with xtree path (bs4 is better)
Leave it until I know what happened

url = "https://weibo.cn/1776448504/fans?page=19&display=0&retcode=6102"
r = requests.get(url, cookies={"Cookie": "_T_WM=ec1a4454c0d9d6d28bb947142ca09f4f; SUB=_2A253gE9VDeThGeVM6FQZ9yvOyD6IHXVUi1EdrDV6PUJbkdBeLUbdkW1NTKWBvjMxvfXWbMrYJ01hTA-fdYsQshDp; SUHB=0OM0IZCuuDil4y; SCF=Aj52M7AisY2zemY_Am0nKcL71Og-kwj4KrbW9HkL8O51TjMxprJ7l2Sryhd6P9gtzV7sn1wG4n0t3QM9ZNxcc0w.; SSOLoginState=1518616325"}, headers=headers)
"""


if __name__ == "__main__":

    cookie = get_cookie()
    username = "caizicaixukun"
    followers = get_followers(cookie, username)
    print username, followers
