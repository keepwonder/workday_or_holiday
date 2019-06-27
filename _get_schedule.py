# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2019/6/11 14:48
# @File  : get_schedule_from_baidu
"""
百度获取一年的节假日时间安排表
"""
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3


def get_schedule():
    # 获取当前年
    cur_year = datetime.now().year

    # 开启浏览器无头模式访问百度
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./dr/chromedriver.exe')
    driver.get('http://www.baidu.com')

    # 连接数据库
    is_exist_db_path = os.path.exists('./db')
    if not is_exist_db_path:
        os.mkdir('./db')
    con = sqlite3.connect('./db/holiday.db')
    cur = con.cursor()

    # 百度搜索关键字: 假日表
    driver.find_element_by_id('kw').send_keys(u'假日表')
    driver.find_element_by_id('su').click()
    time.sleep(2)


    # 将获取的信息存入数据库holiday中
    # 表名为holiday_year： holiday_2019
    # 字段：id(主键自增), holiday_name(节日), holiday_period(放假时间), paid_leave(调休上班日期), days_off_num(放假天数)
    holiday_table = driver.find_element_by_xpath('//*[@id="content_left"]//table[@class="c-table"]/tbody')

    for tr in holiday_table.find_elements_by_xpath('./tr')[1:]:
        tr_value = []
        for td in tr.find_elements_by_xpath('./td'):
            # print(td.text, end=' ')
            tr_value.append(td.text)
        insert_sql = """
            insert into holiday_{}(holiday_name, holiday_period, paid_leave, days_off_num) 
            values('{}','{}','{}','{}')
        """.format(cur_year, tr_value[0], tr_value[1], tr_value[2], tr_value[3])
        cur.execute(insert_sql)

    con.commit()
    cur.close()
    con.close()

    driver.quit()
