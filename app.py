# -*- coding:utf-8 -*- 
# @Author: Jone Chiang
# @Date  : 2019/6/13 9:34
# @File  : app

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'welcome'


if __name__ == '__main__':
    app.run()
