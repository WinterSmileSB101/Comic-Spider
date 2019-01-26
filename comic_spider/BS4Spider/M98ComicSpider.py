import requests
from bs4 import BeautifulSoup
import os


def get_all_98comic(host):

    url = "{host}/list/{page}.html";

    page = 0
    haveNextPage = True

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }

    proxies = {
        'http': "http://172.22.8.39:3128",
        'https': "http://172.22.8.39:3128"
    }

    while haveNextPage:
        page += 1
        targetUrl = str.format(url, host=host, page=page)
        res = requests.get(targetUrl, headers=headers, proxies=proxies)
        res.encoding = 'UTF-8'
        # print(res.text)

        domSoup = BeautifulSoup(res.text,features = "lxml-xml")  # 加上 lxml-xml 可以去掉自己选择解析器可能造成差异的提醒
        parse_current_comic(domSoup, host)

        # title = domSoup.select(".book-list > #contList a.bcover")[0]['title']

        prevBtnDom = domSoup.select('a.prev')
        nextBtn = prevBtnDom[prevBtnDom.__len__() - 1]
        haveNextPage = nextBtn.text == "下一頁"
        # haveNextPage = False # 测试时的开关
        # print(title)


def parse_current_comic(domSoup, host):
    # domSoup = BeautifulSoup(page.text)
    comics = domSoup.select(".book-list > #contList > li")
    for comic in comics:
        comicContainer = comic.select("a.bcover")[0];
        title = comicContainer['title']
        link = str.format("{host}{href}", host=host, href=comicContainer['href'])
        coverLink = comicContainer.select("a > img")[0]['data-src']
        print(coverLink)
        create_comic_floder(title, link, coverLink, "Comics")


def create_comic_floder(name, link, coverLink, path):
    print(name)
    name = replace_invalide_words(name)
    print(name)
    comicPath = str.format("{path}/{name}", path=path, name=name)
    exist = os.path.exists(comicPath)
    if(not exist):
        # 创建相对路径的文件夹
        if(not os.path.exists(path)):
            os.makedirs(path)
        os.makedirs(comicPath)

    # 放入comic 的基本信息
    index_file = str.format("{comicPath}/index.txt",comicPath=comicPath)
    with open(index_file,"wt",encoding="utf-16") as f:  # 使用 with 方式打开文件不需要释放资源 ，编码必须utf-16,utf-8打开会有特殊字符如❤，• 的写入失败
        comic_properties = [
            str.format("Title: {name}\n", name=name),
            str.format("Link: {link}\n", link=link),
            str.format("Cover: {coverLink}", coverLink=coverLink)
        ]
        f.writelines(comic_properties)


def replace_invalide_words(target):
    target = str.replace(target, "*", "")
    target = str.replace(target, "\\", "")
    target = str.replace(target, "/", "")
    target = str.replace(target, ":", "")
    target = str.replace(target, "?", "")
    target = str.replace(target, "\"", "")
    target = str.replace(target, "<", "")
    target = str.replace(target, ">", "")
    target = str.replace(target, "|", "")
    target = str.replace(target, ".", "")
    # target = str.replace(target, "•", "") # 改变读取文件时的编码即可，不需要去除

    return target


# 获取跳转之后的真实302 地址
def handle_http302(link):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }

    proxies = {
        'http': "http://172.22.8.39:3128",
        'https': "http://172.22.8.39:3128"
    }
    res = requests.get(link, headers=headers, proxies=proxies)
    url302_final = res.url
    print(url302_final)


host = "https://www.98comic.com"
# get_all_98comic(host)  # 入口


# true url:https://pic.98comic.com/ede4f7cab3a61bca5b55133a2bac2c35/3F747D20283F3F7F7B3D737F7D797320283F5E3F23272023203F7173644F2020213F6A4F202020214F24252925213E5A40573D17063D3.jpg
handle_http302("https://www.98comic.com/g.php?ede4f7cab3a61bca5b55133a2bac2c35/3F747D20283F3F7F7B3D737F7D797320283F5E3F23272023203F7173644F2020213F6A4F202020214F24252925213E5A40573D2C21991")
