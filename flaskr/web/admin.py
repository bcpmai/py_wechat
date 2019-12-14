# -*- coding: utf-8 -*-
import datetime
import json
import time
import traceback
from flask import Flask, session, redirect, url_for
from flask import Blueprint, jsonify, Flask, request, render_template

from flaskr.common import db_session, password
from flaskr.common.utils import timestamp_to_date
from flaskr.db_model.member import Member
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


@admin_bp.route('/admin/index')
@login_required
def admin_index():
    """
    后台用户主界面
    :return:
    """
    return render_template('index.html')


@admin_bp.route('/admin/member/list')
@login_required
def admin_member_list():
    """
    后台用户列表
    :return:
    """

    page = request.args.get('page', 1)
    pagination = Member.query.order_by(Member.id.desc()).paginate(int(page), 10)

    records = list()
    for items in pagination.items:
        items.created_at = timestamp_to_date(items.created_at)
        items.updated_at = timestamp_to_date(items.updated_at)
        records.append(items)

    db_session.close()
    return render_template('member-list.html', pagination=pagination, records=records)


@admin_bp.route('/admin/order/list')
@login_required
def admin_order_list():
    """
    后台订单列表
    :return:
    """
    page = request.args.get('page', 1)
    pagination = RepairOrder.query.order_by(RepairOrder.id.desc()).paginate(int(page), 10)

    records = list()
    for items in pagination.items:
        items.created_at = timestamp_to_date(items.created_at)
        records.append(items)

    db_session.close()
    return render_template('order-list.html', pagination=pagination, records=records)


@admin_bp.route('/admin/order/edit/status', methods=["POST", "GET"])
@login_required
def admin_order_status_edit():
    """
    后台订单列表状态数据编辑
    :return:
    """

    if request.method == 'POST':
        updated_at = int(time.time())
        order_id = request.form['order_id']

        try:

            update_sql = "update repair_order set status = 1,updated_at={updated_at} where id={order_id}".\
                format(order_id=order_id, updated_at=updated_at)

            db_session.execute(update_sql)
            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'update ok'})


@admin_bp.route('/admin/memberType/list')
@login_required
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


@admin_bp.route('/admin/memberType/add')
@login_required
def admin_member_type_add():
    """
    添加会员类型
    :return:
    """
    return render_template('member-type-add.html')


@admin_bp.route('/admin/memberTypes/submit', methods=["POST"])
@login_required
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
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@admin_bp.route('/admin/memberType/delete', methods=["POST"])
@login_required
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
            db_session.close()
            return jsonify({'success': False, 'msg': 'delete date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'delete ok'})


@admin_bp.route('/admin/order/delete', methods=["POST"])
@login_required
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
            db_session.close()
            return jsonify({'success': False, 'msg': 'delete data error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'delete ok'})


@admin_bp.route('/admin/types/list')
@login_required
def admin_types_list():
    """
    后台类型列表
    :return:
    """
    records = list()

    query_address_sql = "SELECT * FROM types LEFT JOIN types_category ON types.id=types_category.type_id"
    res = db_session.execute(query_address_sql).fetchall()

    for temp in res:
        temp = dict(temp)
        temp['created_at'] = timestamp_to_date(temp['created_at'])
        temp['updated_at'] = timestamp_to_date(temp['updated_at'])

        records.append(temp)

    db_session.close()

    return render_template('types-list.html', records=records)


@admin_bp.route('/admin/types/add')
@login_required
def admin_types_add():
    """
    添加清洗类型
    :return:
    """

    return render_template('types-add.html')


@admin_bp.route('/admin/typesCategory/add')
@login_required
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


@admin_bp.route('/admin/typesCategory/submit', methods=["POST"])
@login_required
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
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@admin_bp.route('/admin/types/submit', methods=["POST"])
@login_required
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
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@admin_bp.route('/admin/types/delete', methods=["POST"])
@login_required
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
            db_session.close()
            return jsonify({'success': False, 'msg': 'delete date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'delete ok'})


@admin_bp.route('/admin/logout')
@login_required
def admin_logout():
    """
    后台用户退出
    :return:
    """
    session.pop('username')

    return redirect('/admin/login')


# def check_login():
#     """
#     检查登录
#     :return:
#     """
#     if session.get('username') != 'admin_login':
#         return redirect(url_for('admin_bp.admin_login'))

# data_sj = time.localtime(time_sj)
# time_str = time.strftime("%Y-%m-%d %H:%M:%S",data_sj)
