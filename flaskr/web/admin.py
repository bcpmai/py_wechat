# -*- coding: utf-8 -*-
import datetime
import json
import time
import traceback
from flask import Flask, session, redirect, url_for
from flask import Blueprint, jsonify, Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from flaskr.common import db_session

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin/login', methods=["POST", "GET"])
def admin_login():
    """
    后台用户登录
    :return:
    """
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        admin_password = request.form['admin_password']

        if admin_name == 'admin' and admin_password == 'test123456':
            session['username'] = 'admin_login'
            return redirect('/admin/index')

    return render_template('login.html')


@admin_bp.route('/admin/index')
def admin_index():
    """
    后台用户主界面
    :return:
    """
    check_login()
    return render_template('index.html')


@admin_bp.route('/admin/member/list')
def admin_member_list():
    """
    后台用户列表
    :return:
    """
    check_login()

    records = list()

    query_address_sql = "SELECT * FROM member "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('member-list.html', records=records)

@admin_bp.route('/admin/order/list')
def admin_order_list():
    """
    后台订单列表
    :return:
    """
    check_login()

    records = list()

    query_address_sql = "SELECT * FROM repair_order "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('order-list.html', records=records)

@admin_bp.route('/admin/memberType/list')
def admin_memberType_list():
    """
    会员类型列表
    :return:
    """
    check_login()

    records = list()

    query_address_sql = "SELECT * FROM membertypes "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('member-type-list.html', records=records)

@admin_bp.route('/admin/memberType/add')
def admin_memberType_add():
    """
    添加会员类型
    :return:
    """

    return render_template('member-type-add.html')

@admin_bp.route('/admin/memberTypes/submit', methods=["POST"])
def submit_memberTypes():
    """
    提交会员类型
    :return:
    """
    if request.method == 'POST':
        member_title = request.form['title']
        member_price = request.form['price']
        member_limit = request.form['limit']
        member_describe = request.form['describe']
        member_details = request.form['details']
        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into membertypes (member_title,member_price,member_limit,member_describe,member_details,created_at,updated_at) " \
                                 "values ('{member_title}','{member_price}','{member_limit}','{member_describe}','{member_details}',{created_at},{updated_at})". \
                format(member_title=member_title, member_price=member_price, member_limit=member_limit, member_describe=member_describe, member_details=member_details, created_at=created_at, updated_at=updated_at)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'save date error'})

        return jsonify({'success': True, 'msg': 'save ok'})

@admin_bp.route('/admin/memberType/delete', methods=["POST"])
def delete_memberType():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        id = request.form['id']

        try:

            insert_address_sql = "delete from membertypes where id={id}".format(id=id)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'delete date error'})

        return jsonify({'success': True, 'msg': 'delete ok'})

@admin_bp.route('/admin/order/delete', methods=["POST"])
def delete_order():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        id = request.form['id']

        try:

            insert_address_sql = "delete from repair_order where id={id}".format(id=id)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'delete date error'})

        return jsonify({'success': True, 'msg': 'delete ok'})



@admin_bp.route('/admin/types/list')
def admin_types_list():
    """
    后台类型列表
    :return:
    """
    check_login()

    records = list()

    query_address_sql = "SELECT * FROM types LEFT JOIN types_category ON types.id=types_category.type_id"
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('types-list.html', records=records)


@admin_bp.route('/admin/types/add')
def admin_types_add():
    """
    添加清洗类型
    :return:
    """

    return render_template('types-add.html')

@admin_bp.route('/admin/typesCategory/add')
def admin_typesCategory_add():
    """
    添加清洗类型
    :return:
    """
    check_login()

    records = list()

    query_address_sql = "SELECT * FROM types "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('types-category-add.html', records=records)

@admin_bp.route('/admin/typesCategory/submit', methods=["POST"])
def submit_typesCategory():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        type_name = request.form['type_name']
        price = request.form['price']
        type_id = request.form['type_id']
        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into types_category (category_name,price,type_id,created_at,updated_at) " \
                                 "values ('{category_name}',{price},{type_id},{created_at},{updated_at})". \
                format(category_name=type_name, price=price, type_id=type_id, created_at=created_at, updated_at=updated_at)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'save date error'})

        return jsonify({'success': True, 'msg': 'save ok'})


@admin_bp.route('/admin/types/submit', methods=["POST"])
def submit_types():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        type_name = request.form['typename']
        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into types (type_name,created_at,updated_at) " \
                                 "values ('{type_name}',{created_at},{updated_at})". \
                format(type_name=type_name, created_at=created_at, updated_at=updated_at)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'save date error'})

        return jsonify({'success': True, 'msg': 'save ok'})

@admin_bp.route('/admin/types/delete', methods=["POST"])
def delete_types():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        id = request.form['id']

        try:

            insert_address_sql = "delete from types where id={id}".format(id=id)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'delete date error'})

        return jsonify({'success': True, 'msg': 'delete ok'})


@admin_bp.route('/admin/logout')
def admin_logout():
    """
    后台用户退出
    :return:
    """
    check_login()

    session.pop('username')

    return redirect('/admin/login')


def check_login():
    """
    检查登录
    :return:
    """
    if session.get('username') != 'admin_login':
        return redirect('/admin/login')
