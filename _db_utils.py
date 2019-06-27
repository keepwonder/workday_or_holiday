# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2019/6/12 9:03
# @File  : db_utils
import re
import os
import calendar
import sqlite3
from datetime import datetime

cur_year = datetime.now().year
common_year = [-1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
leap_year = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def get_all_days(s):
    """
    '12月30日~1月1日'
    :param s:
    :return:
    """
    begin, end = s.split('~')
    begin_0, begin_1 = re.findall('\d+', begin)
    end_0, end_1 = re.findall('\d+', end)
    begin_0, begin_1 = int(begin_0), int(begin_1)
    end_0, end_1 = int(end_0), int(end_1)

    # print(begin, end)

    date = []

    if begin_0 == end_0:  # 起止日期在同一个月
        days = list(range(begin_1, end_1+1))
        for day in days:
            day = str(begin_0) + '月' + str(day) + '日'
            date.append(day)

    elif begin_0 > end_0:  # 跨年 begin_0 12月 end_0 1月
        days_of_last_month = list(range(begin_1, begin_1 + leap_year[begin_0] - begin_1 + 1))
        for day in days_of_last_month:
            day = str(begin_0) + '月' + str(day) + '日'
            date.append(day)

        days_of_cur_month = list(range(1, end_0 + 1))
        for day in days_of_cur_month:
            day = str(end_0) + '月' + str(day) + '日'
            date.append(day)

    elif begin_0 < end_0:  # 起止日期不在同一个月
        if calendar.isleap(cur_year):
            days_of_last_month = list(range(begin_1, begin_1 + leap_year[begin_0] - begin_1 + 1))
            for day in days_of_last_month:
                day = str(begin_0) + '月' + str(day) + '日'
                date.append(day)

            days_of_cur_month = list(range(1, end_0 + 1))
            for day in days_of_cur_month:
                day = str(end_0) + '月' + str(day) + '日'
                date.append(day)
        else:
            days_of_last_month = list(range(begin_1, begin_1 + common_year[begin_0] - begin_1 + 1))
            for day in days_of_last_month:
                day = str(begin_0) + '月' + str(day) + '日'
                date.append(day)

            days_of_cur_month = list(range(1, end_1 + 1))
            for day in days_of_cur_month:
                day = str(end_0) + '月' + str(day) + '日'
                date.append(day)
    # print(date)
    return date


def get_all_days_2(s):
    res = re.findall('\d+月\d+日', s)
    print(res)
    return res


class DbUtils:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_con(self):
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()

    def close_db(self):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()

    def create_tab_holiday(self, year):
        """
        新建holiday表
        :return:
        """
        self.get_con()
        holiday_sql = """
            create table holiday_{}(id INTEGER primary key autoincrement, holiday_name varchar(50), holiday_period varchar(200), paid_leave varchar(200), days_off_num integer(2))
        """.format(year)
        self.cur.execute(holiday_sql)
        self.close_db()

    def analyze_holiday_period(self, year):
        """
        分析holiday表中的数据: 放假时间
        :return:
        """
        self.get_con()
        holiday_period_sql = """
            select holiday_period from holiday_{}
        """.format(year)
        self.cur.execute(holiday_period_sql)
        result = []
        results = self.cur.fetchall()
        for res in results:
            res0 = get_all_days(res[0])
            result.extend(res0)
        # print(result)

        path = './db/holiday_period_{}.txt'.format(cur_year)
        if os.path.exists(path):
            os.remove(path)
        for i in result:
            with open('./db/holiday_period_{}.txt'.format(cur_year), 'a+', encoding='utf-8') as f:
                f.write(i+'\n')

        self.close_db()

    def analyze_paid_leave(self, year):
        """
        分析holiday表中的数据: 调休上班日期
        :param year:
        :return:
        """
        self.get_con()
        paid_leave_sql = """
            select paid_leave from holiday_{}
        """.format(year)
        self.cur.execute(paid_leave_sql)
        result = []
        results = self.cur.fetchall()
        for res in results:
            res0 = get_all_days_2(res[0])
            result.extend(res0)
        # print(result)

        path = './db/paid_leave_{}.txt'.format(cur_year)
        if os.path.exists(path):
            os.remove(path)

        for i in result:
            with open('./db/paid_leave_{}.txt'.format(cur_year), 'a+', encoding='utf-8') as f:
                f.write(i+'\n')

        self.close_db()

    def get_holiday(self):
        with open('./db/holiday_period_{}.txt'.format(cur_year), 'r', encoding='utf-8') as f:
            res = f.readlines()
            res = [i.strip() for i in res]

        print(res)
        return res

    def get_workday(self):
        with open('./db/paid_leave_{}.txt'.format(cur_year), 'r', encoding='utf-8') as f:
            res = f.readlines()
            res = [i.strip() for i in res]

        print(res)
        return res


if __name__ == '__main__':
    cur_year = datetime.now().year
    db_util = DbUtils('./db/holiday.db')
    # db_util.create_tab_holiday(cur_year)
    # db_util.analyze_holiday_period(cur_year)
    # db_util.analyze_paid_leave(cur_year)

    # get_all_days('2月27日~3月5日')
    # # get_all_days('5月29日(除夕）~6月2日')

    # get_all_days_2('2月2日（周六）、2月3日（周日）上班')

    db_util.get_workday()


