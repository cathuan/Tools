# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import re


if __name__ == "__main__":

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
    for info in cookies_infos.split():
        if info.startswith("SUB=") or info.startswith("SUHB=") or info.startswith("SCF=") or info.startswith("SSOLoginState="):
            cookie_parts.append(info)
    cookie = " ".join(cookie_parts)

    url = "https://weibo.cn/caizicaixukun?display=0&retcode=6102"
    r = requests.get(url, cookies={"Cookie": cookie})

    selector = etree.HTML(r.content)
    str_gz = selector.xpath("//div[@class='tip2']/a/text()")[1]
    pattern = r"\d+\.?\d*"
    guid = re.findall(pattern, str_gz, re.M)
    followers = int(guid[0])
    print str(followers)
