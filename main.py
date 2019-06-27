# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2019/6/12 14:33
# @File  : main

"""
查询日期接口
step:
1. 从百度查询假日表关键字获取本年的节假日安排并存入表中（一年只需要查询一次）
2. 分析表中放假时间和调休上班两个字段并分别生成两个文件存储对应的日期 (一年只需要分析一次)
3. 输入对应的日期，并结合上面两个文件，判断是工作日还是休息日

"""
import os
from _db_utils import *
from _get_schedule import get_schedule
from datetime import datetime

CUR_YEAR = datetime.now().year


class Api:
    def __init__(self):
        self.db_path = './db'
        self.db_utils = DbUtils(self.db_path + '/holiday.db')

    def _create_db_directory_and_files(self):
        is_exist_db_path = os.path.exists(self.db_path)
        if not is_exist_db_path:
            os.mkdir(self.db_path)

        f = []
        for root, dirs, files in os.walk(self.db_path):
            for file in files:
                f.append(file)

        if 'holiday.db' not in f:
            self.db_utils.create_tab_holiday(CUR_YEAR)
            get_schedule()

        self.db_utils.analyze_holiday_period(CUR_YEAR)
        self.db_utils.analyze_paid_leave(CUR_YEAR)

    def workday_or_holiday(self, d):
        """

        :param d: 传入日期(2019年6月12日 2019.06.12 2019/06/12 2019-06-12 20190612)
        :return: 工作日 or 休息日
        """
        holiday = self.db_utils.get_holiday()
        workday = self.db_utils.get_workday()

        if '月' in d or '日' in d:
            d = re.findall('\d+月\d+日', d)[0]
            print(d)

        if '.' in d:
            d = d.split('.')[-2:]
            d = d[0].lstrip('0')+'月'+d[1]+'日'
            print(d)

        if '/' in d:
            d = d.split('/')[-2:]
            d = d[0].lstrip('0') + '月' + d[1] + '日'
            print(d)

        if '-' in d:
            d = d.split('-')[-2:]
            d = d[0].lstrip('0') + '月' + d[1] + '日'
            print(d)

        if len(d) == 8:
            d = d[-4:]
            print(d)
            d = d[:2].lstrip('0') + '月' + d[2:] + '日'
            print(d)

        if d in holiday:
            return '节假日'
        elif d in workday:
            return '休息日'
        else:  # 判断是否是普通周末
            print(d)
            d = str(CUR_YEAR) + '年' + d
            print(d)
            weekday = datetime.strptime(d, '%Y年%m月%d日').weekday()
            if weekday in (5, 6):
                return '休息日'
            else:
                return '工作日'

    def get_result(self, d):
        self._create_db_directory_and_files()
        return self.workday_or_holiday(d)


if __name__ == '__main__':
    api = Api()
    res = api.get_result('20190612')
    print(res)
