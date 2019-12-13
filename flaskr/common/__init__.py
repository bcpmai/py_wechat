# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import socket

app = Flask(__name__)
# if socket.gethostname() == 'bcpmai-win10':
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dev2312@127.0.0.1/api_wechat?charset=utf8mb4'
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://baernaoer:baernaoer@127.0.0.1/yijiemp?charset=utf8mb4'

dotenv_path = os.path.join(os.path.dirname(app.instance_path), '.env')
load_dotenv(dotenv_path=dotenv_path)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('mysql_link', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Base = SQLAlchemy(app)
db_session = Base.session
