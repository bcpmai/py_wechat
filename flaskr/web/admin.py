# -*- coding: utf-8 -*-
import datetime
import json
import time
import traceback
from flask import Flask, session, redirect, url_for
from flask import Blueprint, jsonify, Flask, request, render_template

from flaskr.common import db_session, password
from flaskr.db_model.repair_order import RepairOrder
from flaskr.web import login_required

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/', methods=["POST", "GET"])
@admin_bp.route('/admin/login', methods=["POST", "GET"])
def admin_login():
    """
    后台用户登录
    :return:
    """
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        admin_password = request.form['admin_password']

        if admin_name == 'admin' and admin_password == password:
            session['username'] = 'admin_login'
            return redirect('/admin/index')

    return render_template('login.html')


@login_required
@admin_bp.route('/admin/index')
def admin_index():
    """
    后台用户主界面
    :return:
    """
    return render_template('index.html')


@login_required
@admin_bp.route('/admin/member/list')
def admin_member_list():
    """
    后台用户列表
    :return:
    """

    records = list()

    query_address_sql = "SELECT * FROM member "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('member-list.html', records=records)


@login_required
@admin_bp.route('/admin/order/list')
def admin_order_list():
    """
    后台订单列表
    :return:
    """
    # records = list()
    #
    # query_address_sql = "SELECT * FROM repair_order "
    # res = db_session.execute(query_address_sql).fetchall()
    #
    # for temp in res:
    #     records.append(dict(temp))
    #
    # db_session.close()

    page = request.args.get('page', 1)

    pagination = RepairOrder.query.order_by(RepairOrder.id.desc()).paginate(int(page), 5)
    return render_template('order-list.html', pagination=pagination, records=pagination.items)


@login_required
@admin_bp.route('/admin/memberType/list')
def admin_member_type_list():
    """
    会员类型列表
    :return:
    """

    records = list()

    query_address_sql = "SELECT * FROM member_types "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('member-type-list.html', records=records)


@login_required
@admin_bp.route('/admin/memberType/add')
def admin_member_type_add():
    """
    添加会员类型
    :return:
    """
    return render_template('member-type-add.html')


@login_required
@admin_bp.route('/admin/memberTypes/submit', methods=["POST"])
def submit_member_types():
    """
    提交会员类型
    :return:
    """
    if request.method == 'POST':
        member_title = request.form['title']
        member_price = request.form['price']
        member_limit = request.form['limit']
        member_describe = request.form['describe']
        member_details = request.form.get('details', '')
        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into member_types (member_title,member_price,member_limit," \
                                 "member_describe,member_details,created_at,updated_at) " \
                                 "values ('{member_title}','{member_price}','{member_limit}','{member_describe}'," \
                                 "'{member_details}',{created_at},{updated_at})". \
                format(member_title=member_title, member_price=member_price, member_limit=member_limit,
                       member_describe=member_describe, member_details=member_details, created_at=created_at,
                       updated_at=updated_at)

            db_session.execute(insert_address_sql)
            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'save date error'})

        return jsonify({'success': True, 'msg': 'save ok'})


@login_required
@admin_bp.route('/admin/memberType/delete', methods=["POST"])
def delete_member_type():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        member_id = request.form['id']

        try:

            insert_address_sql = "delete from member_types where id={id}".format(id=member_id)

            db_session.execute(insert_address_sql)
            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'delete date error'})

        return jsonify({'success': True, 'msg': 'delete ok'})


@login_required
@admin_bp.route('/admin/order/delete', methods=["POST"])
def delete_order():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        repair_order = request.form['id']

        try:

            delete_sql = "delete from repair_order where id={id}".format(id=repair_order)
            db_session.execute(delete_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'delete data error'})

        return jsonify({'success': True, 'msg': 'delete ok'})


@login_required
@admin_bp.route('/admin/types/list')
def admin_types_list():
    """
    后台类型列表
    :return:
    """
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


@login_required
@admin_bp.route('/admin/typesCategory/add')
def admin_types_category_add():
    """
    添加清洗类型
    :return:
    """
    records = list()

    query_address_sql = "SELECT * FROM types "
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        records.append(dict(temp))

    db_session.close()

    return render_template('types-category-add.html', records=records)


@login_required
@admin_bp.route('/admin/typesCategory/submit', methods=["POST"])
def submit_types_category():
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
                format(category_name=type_name, price=price, type_id=type_id, created_at=created_at,
                       updated_at=updated_at)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            return jsonify({'success': False, 'msg': 'save date error'})

        return jsonify({'success': True, 'msg': 'save ok'})


@login_required
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


@login_required
@admin_bp.route('/admin/types/delete', methods=["POST"])
def delete_types():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        types_id = request.form['id']

        try:

            insert_address_sql = "delete from types where id={id}".format(id=types_id)
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
    # check_login()

    session.pop('username')

    return redirect('/admin/login')

# def check_login():
#     """
#     检查登录
#     :return:
#     """
#     if session.get('username') != 'admin_login':
#         return redirect('/admin/login')

# data_sj = time.localtime(time_sj)
# time_str = time.strftime("%Y-%m-%d %H:%M:%S",data_sj)
