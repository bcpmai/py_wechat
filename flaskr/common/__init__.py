# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import socket

# 配置数据库 todo 迁移到 dotenv

app = Flask(__name__)
if socket.gethostname() == 'bcpmai-win10':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dev2312@127.0.0.1/api_wechat?charset=utf8mb4'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://baernaoer:baernaoer@127.0.0.1/yijiemp?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db_session = SQLAlchemy(app).session
