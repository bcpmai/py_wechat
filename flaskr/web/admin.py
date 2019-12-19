# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import traceback
from flask import Flask, session, redirect, url_for
from flask import Blueprint, jsonify, Flask, request, render_template

from flaskr.common import db_session, password, app
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

            update_sql = "update repair_order set status = 1,updated_at={updated_at} where id={order_id}". \
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

    query_address_sql = "SELECT * FROM member_types order by id desc"
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

    op_type = request.args.get("type", "")
    member_id = request.args.get("id", 0)

    member_title = ""
    member_price = 0
    member_limit = ""
    member_describe = ""
    member_details = ""
    number = 0

    if int(member_id) > 0:
        query_sql = "select * from member_types where id={member_id}".format(member_id=member_id)
        res = db_session.execute(query_sql).first()
        res = dict(res)
        member_title = res['member_title']
        member_price = res['member_price']
        member_limit = res['member_limit']
        member_describe = res['member_describe']
        member_details = res['member_details']
        number = res['number']

    return render_template('member-type-add.html',
                           op_type=op_type, member_id=member_id, member_title=member_title, member_price=member_price,
                           member_limit=member_limit, member_describe=member_describe, member_details=member_details,
                           number=number
                           )


@admin_bp.route('/admin/member-types/update', methods=["POST"])
@login_required
def member_types_update():
    """
    修改会员类型
    :return:
    """
    if request.method == 'POST':
        member_id = request.form['member_id']
        member_title = request.form['title']
        member_price = request.form['price']
        member_limit = request.form['limit']
        number = request.form['number']
        member_describe = request.form['describe']
        member_details = request.form.get('details', '')
        updated_at = int(time.time())

        try:

            updated_sql = "update member_types set member_title='{member_title}',member_price={member_price}, " \
                          "member_limit='{member_limit}',member_describe='{member_describe}',number={number}," \
                          "member_details='{member_details}',updated_at={updated_at} " \
                          "where id={id}" \
                .format(id=member_id, member_title=member_title, member_price=member_price, member_limit=member_limit,
                        member_describe=member_describe, member_details=member_details, updated_at=updated_at,
                        number=number)

            db_session.execute(updated_sql)
            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'modify date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@admin_bp.route('/admin/memberTypes/submit', methods=["POST"])
@login_required
def submit_member_types():
    """
    提交会员类型
    :return:get-member-wxcode-update
    """
    if request.method == 'POST':
        member_title = request.form['title']
        member_price = request.form['price']
        member_limit = request.form['limit']
        number = request.form['number']
        member_describe = request.form['describe']
        member_details = request.form.get('details', '')
        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into member_types (member_title,member_price,member_limit," \
                                 "member_describe,number,member_details,created_at,updated_at) " \
                                 "values ('{member_title}','{member_price}','{member_limit}','{member_describe}',{number}," \
                                 "'{member_details}',{created_at},{updated_at})". \
                format(member_title=member_title, member_price=member_price, member_limit=member_limit,
                       member_describe=member_describe, member_details=member_details, created_at=created_at,
                       number=number,
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

    query_sql = "SELECT t1.id,t1.category_name,t2.type_name,t1.price,t1.created_at,t1.updated_at " \
                "FROM types_category t1 LEFT JOIN types t2 ON t2.id=t1.type_id"
    res = db_session.execute(query_sql).fetchall()

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


@admin_bp.route('/admin/service-types-edit', methods=["POST", "GET"])
@login_required
def service_types_edit():
    """
    服务类型编辑
    :return:
    """
    service_types_id = request.args.get("id")

    query_sql = "SELECT t1.id,t1.type_id,t1.category_name,t2.type_name,t1.price,t1.created_at,t1.updated_at " \
                "FROM types_category t1 LEFT JOIN types t2 ON t2.id=t1.type_id where t1.id ={service_types_id} ". \
        format(service_types_id=service_types_id)
    record = db_session.execute(query_sql).first()

    query_type_sql = "select * from types"
    type_records = list()
    res = db_session.execute(query_type_sql).fetchall()
    for temp in res:
        temp = dict(temp)
        type_records.append(temp)

    if request.method == 'POST':
        type_id = request.form['type_id']
        category_name = request.form['category_name']
        price = request.form['price']

        try:

            update_sql = "update types_category set price={price},category_name='{category_name}',type_id={type_id} " \
                         "where id={id}". \
                format(type_id=type_id, price=price, category_name=category_name, id=service_types_id)
            db_session.execute(update_sql)
            db_session.commit()
            db_session.close()

            return jsonify({'success': True, 'msg': 'modify success'})
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'modify delete'})

    db_session.close()
    return render_template('service_types_edit.html', service_types_id=service_types_id, type_records=type_records,
                           record=record)


@admin_bp.route('/admin/service_types/del', methods=["POST"])
@login_required
def service_types_del():
    """
    删除
    :return:
    """
    if request.method == 'POST':
        types_category_id = request.form['id']

        try:
            delete_sql = "delete from types_category where id={id}".format(id=types_category_id)
            db_session.execute(delete_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'delete data error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'delete success'})


@admin_bp.route('/admin/typesCategory/add')
@login_required
def admin_types_category_add():
    """
    添加清洗类型
    :return:
    """
    records = list()

    query_address_sql = "SELECT * FROM types order by id desc"
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


@admin_bp.route('/admin/upload', methods=["POST"])
@login_required
def admin_upload():
    """
    上传图片并保存文件
    :return:
    """
    images = request.files.get('file')

    # 得到upload的路径
    upload_dir = os.path.join(os.path.dirname(app.instance_path), 'flaskr/static/upload/')

    # 得到上传图片的url
    image_path = os.path.join(upload_dir, images.filename)
    image_url = os.path.join(os.getenv('domain_name', ''), 'static/upload/', images.filename)
    print(image_url)
    print(image_path)

    try:
        # 保存图片
        images.save(image_path)
        return jsonify({"code": 0, "msg": "success", "data": {"src": image_url, "title": images.filename}})
    except Exception:
        return jsonify({"code": 1, "msg": "false"})


# def check_login():
#     """
#     检查登录
#     :return:
#     """
#     if session.get('username') != 'admin_login':
#         return redirect(url_for('admin_bp.admin_login'))

# data_sj = time.localtime(time_sj)
# time_str = time.strftime("%Y-%m-%d %H:%M:%S",data_sj)
