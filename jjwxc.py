# -*- coding: utf-8 -*-

import requests, csv, sys
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

keyword = "弱受"

open("{}.csv".format(keyword), "w", encoding='utf-8-sig').close()
file = open("{}.csv".format(keyword), "a", encoding='utf-8-sig')
writer = csv.writer(file)

def get_url(page):
    return "http://www.jjwxc.net/bookbase.php?fw0=0&fbsj=0&ycx0=0&xx0=0&mainview0=0&sd0=0&lx0=0&fg1=1&fg2=2&fg3=3&fg4=4&fg5=5&sortType=4&page=591&isfinish=0&collectiontypes=ors&searchkeywords={}&page={}".format(requests.utils.quote(keyword, encoding="GBK"),page)

def get_page(page):
    try:
        soup = BeautifulSoup(session.get(get_url(page)).content, features="html.parser", from_encoding="GBK")
        rows = soup.select_one("table.cytable").select("tr")[1:]
    except AttributeError:
        raise AttributeError("错误：第{}页未能加载".format(page))
    if len(rows) != 100:
        print("警告：第{}页不足100条（{}条）".format(page, len(rows)))
    for row in rows:
        cols = row.select("td")
        assert len(cols) == 8
        item = [cols[1].text.strip(), int(cols[6].text)]
        if cols[7].text == "":
            item += [None, None]
        else:
            item += [int(cols[7].text[:4]), int(cols[7].text[5:7])]
        writer.writerow(item)

def login():
    img_url = "http://my.jjwxc.net/include/checkImage.php?"
    img = Image.open(BytesIO(session.get(img_url, stream=True).content))
    img.show()
    data = {"loginname": "15601979170", "loginpassword": "042800@Nyu", "auth_num": input("输入验证码：")}
    session.post("http://my.jjwxc.net/login.php?action=login&referer=", data)

session = requests.Session()

soup = BeautifulSoup(session.get(get_url(0)).content, features="html.parser", from_encoding="GBK")
page_num = int(soup.select_one(".controlbar1").font.text)
login()

for i in range(page_num):
    sys.stdout.write("正在处理：{}/{}\r".format(i+1, page_num))
    get_page(i+1)
    sys.stdout.flush()
    
file.close()
