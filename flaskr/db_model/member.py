# -*- coding: utf-8 -*-

from flaskr.common import Base
from sqlalchemy import Column, Integer, String, Float, Text, Date


class Member(Base.Model):

    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=50), nullable=False, default='')
    wx_code = Column(String(length=50), nullable=False, default='')
    is_member = Column(String(length=50), nullable=False, default='')
    warranty_time = Column(String(length=50), nullable=False, default='')
    wx_name = Column(String(length=50), nullable=False, default='')
    member_grade = Column(String(length=50), nullable=False, default='')
    mobile = Column(String(length=50), nullable=False, default='')
    address = Column(String(length=50), nullable=False, default='')
    created_at = Column(Integer, nullable=False, default=0)
    updated_at = Column(Integer, nullable=False, default=0)
