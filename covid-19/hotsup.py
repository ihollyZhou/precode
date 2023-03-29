import traceback

import requests
import json
import time
import pymysql
from selenium.webdriver import Chrome, ChromeOptions


def get_conn():
    # 建立连接
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="cov", charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 返回百度疫情热搜
def get_baidu_hot():
    option = ChromeOptions()  # 创建谷歌浏览器实例

    url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'
    brower = Chrome(options=option)
    brower.get(url)
    # 找到展开按钮
    # but = brower.find_element_by_css_selector(
    #     '#ptab-0 > div > div.VirusHot_1-5-5_32AY4F.VirusHot_1-5-5_2RnRvg > section > div')  # 定位到点击展开按钮
    # but.click()  # 点击展开

    time.sleep(1)  # 爬虫与反爬，模拟人等待1秒

    c = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    context = [i.text for i in c]  # 获取标签内容
    print(context)
    return context


# 将疫情热搜插入数据库
def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))  # 插入数据
        conn.commit()  # 提交事务保存数据
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


update_hotsearch()