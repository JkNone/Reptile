import re
import sys
import time
import pickle   # 用于读取历史记录
import json
import execjs
import requests
from lxml import etree
from os import path

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}

# 历史记录模块
def his():
    if path.isfile("history"):
        # 读取历史记录
        history = pickle.load(open('history', 'rb'))
        print("历史记录:")
        # 输出文件中的历史记录
        print(history.keys())
        BOOL = input("是否 修改/添加 历史记录？(Y/N)\n")
        if BOOL == "Y":
            # 输入待修改目标网址
            NAME = input("请输入待修改的漫画名称:")
            URL = input("请输入待修改的网址网址：")
            history[NAME] = URL
            pickle.dump(history, open('history', 'wb'))
        else:
            NAME = input("请输入漫画名称：")
            while not NAME in history:
                NAME = input("找不到该漫画，请重新输入：")
            return history[NAME], NAME
    else:
        print("未找到历史记录，请添加记录")
        NAME=input("请输入漫画名称：")
        URL=input("请输入目标网址：")
        pickle.dump({NAME:URL}, open('history', 'wb'))
        return URL,NAME


# 网页源码获取模块
def url_io(URL,BOOL):
    NEW= requests.get(url=URL, headers=headers)  # 模拟浏览器访问网页
    if BOOL:
        index = etree.HTML(NEW.text)# 获取网页源码
        return index
    else:
        return NEW


# 获取网页章节列表
def list(INDEX):
    the_list = INDEX.xpath('//div[@class="cartoon_online_border"]/ul/li/a/@href')  # 获取每一章节的网址  zhang_list为链接列表
    the_name = INDEX.xpath('//div[@class="cartoon_online_border"]/ul/li/a/text()')  # 获取每一章序号
    return the_list,the_name


# 计算下载范围
def x(NAMES):
    BOOL=input("是否选择下载范围？(Y/N)\n")
    while BOOL=='Y':
        TOP=input("请输入头部章节名称：")
        while not TOP in NAMES:
            TOP = input("未找到该章节，请重新输入：")
        TOP = NAMES.index(TOP)

        UNDER = input("请输入尾部章节名称：")
        while not UNDER in NAMES:
            UNDER = input("未找到该章节，请重新输入：")
        UNDER = NAMES.index(UNDER)
        if TOP<=UNDER:
            return TOP,UNDER+1
        else:
            TOP,UNDER=UNDER,TOP+1
            return TOP, UNDER
    return 0,len(NAMES)


# 获取详情页
def get_page_detail(HTML):
    page=url_io(HTML,False)
    imageUrls = parse_js(page)
    return (imageUrls)


# 执行js获取图片链接
def parse_js(r):
    js_str = re.search('eval\((.*?)\)\n', r.text).group(1)
    js_str = js_str.replace('function(p,a,c,k,e,d)', 'function fun(p, a, c, k, e, d)')
    fun = """
                 function run(){
                        var result = %s;
                        return result;
                    }
            """ % js_str
    pages = execjs.compile(fun).call('run')
    data = pages.split('=')[2][1:-2]
    url_list = json.JSONDecoder().decode(data)
    return url_list


# 获取并保存文件
def get_image(IMG_URLS,NAME,ID,COOL):
    PAGE=1
    LIST=[]
    for the_url in IMG_URLS:
        # 当前图片地址
        the_url="http://images.dmzj.com/" + the_url
        # 获取图片源码
        image=url_io(the_url,False)
        # 图片的名称
        the_name=NAME+f'-{PAGE}.jpg'
        # 记录图片名称
        LIST.append(the_name)
        bar(PAGE,len(IMG_URLS),NAME,COOL)
        # 开始下载图片
        with open(ID+the_name,'wb') as file:
            file.write(image.content)

        # 当前页码
        PAGE+=1
    # 返回图片列表
    return LIST


# 进度条模块
def bar(ALL,NOW,NAME,COOL):
    ALL=ALL*100//NOW
    print("\r",end='')
    print(f"当前进度：{COOL[1]}/{COOL[0]}\t"+NAME + ": {}%: ".format(ALL), "▓" * (ALL // 2), end='')
    sys.stdout.flush()
    time.sleep(0.05)