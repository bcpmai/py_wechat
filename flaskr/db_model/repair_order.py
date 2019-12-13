# -*- coding: utf-8 -*-

from flaskr.common import Base
from sqlalchemy import Column, Integer, String, Float, Text, Date


class RepairOrder(Base.Model):

    __tablename__ = 'repair_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sn = Column(String(length=50), nullable=False, default='')
    transaction_id = Column(Integer, nullable=False, default=0)
    mobile = Column(String(length=50), nullable=False, default='')
    name = Column(String(length=50), nullable=False, default='')
    price = Column(String(length=50), nullable=False, default='')
    pay_price = Column(String(length=50), nullable=False, default='')
    category_name = Column(String(length=50), nullable=False, default='')
    city_code = Column(String(length=50), nullable=False, default='')
    address = Column(String(length=50), nullable=False, default='')
    province_code = Column(String(length=50), nullable=False, default='')
    type = Column(String(length=50), nullable=False, default='')
    pay_type = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=0)
    time_end = Column(Integer, nullable=False, default=0)
    created_at = Column(Integer, nullable=False, default=0)
    updated_at = Column(Integer, nullable=False, default=0)