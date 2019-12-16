# -*- coding: utf-8 -*-

import json
import random
import time
import traceback
from decimal import Decimal
import requests

from flask import Blueprint, jsonify, request
from flaskr.common import db_session
from flaskr.common.utils import get_random, md5, dict_to_xml, client_post_xml_data_requests, xml_to_dict, \
    timestamp_to_date

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/bind-address/put', methods=["POST"])
def bind_address():
    """
    绑定地址
    :return:
    """

    if request.method == 'POST':
        username = request.form['username']
        address = request.form['address']
        mobile = request.form['mobile']
        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into address (username,address,mobile,created_at,updated_at) " \
                                 "values ('{username}','{address}','{mobile}',{created_at},{updated_at})". \
                format(username=username, address=address, mobile=mobile, created_at=created_at, updated_at=updated_at)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})

        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@api_bp.route('/add-member/put', methods=["POST"])
def add_member():
    """
    购买会员
    :return:
    """
    if request.method == 'POST':

        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        username = json_data_dict.get('name', '')
        address = json_data_dict.get('address', '')
        mobile = json_data_dict.get('mobile', '')
        wx_code = json_data_dict.get('wxCode', '')
        warranty_time = json_data_dict.get('warrantyTime', '')
        is_member = json_data_dict.get('isMember', '')
        member_grade = json_data_dict.get('memberGrade', '')

        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into member " \
                                 "(username,address,mobile,created_at," \
                                 "updated_at,wx_code,warranty_time,is_member,member_grade) " \
                                 "values (" \
                                 "'{username}','{address}','{mobile}',{created_at},{updated_at},'{wx_code}'," \
                                 "'{warranty_time}','{is_member}','{member_grade}')". \
                format(
                username=username, address=address, mobile=mobile, created_at=created_at, updated_at=updated_at,
                wx_code=wx_code, warranty_time=warranty_time, is_member=is_member, member_grade=member_grade)

            db_session.execute(insert_address_sql)
            db_session.commit()

        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})
        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@api_bp.route('/add-order/put', methods=["POST"])
def add_order():
    """
    我要报修
    :return:
    """
    if request.method == 'POST':
        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        province_code = json_data_dict.get('provinceCode', '')
        city_code = json_data_dict.get('cityCode', '')
        name = json_data_dict.get('name', '')
        mobile = json_data_dict.get('mobile', '')
        address = json_data_dict.get('address', '')
        type = json_data_dict.get('type', '')
        types_category = json_data_dict.get('typesCategory', '')
        price = json_data_dict.get('price', '')
        wx_code = json_data_dict.get('wx_code', '')

        created_at = int(time.time())
        updated_at = int(time.time())

        try:

            insert_address_sql = "insert into repair_order (" \
                                 "province_code,city_code,name,mobile,address,type,category_name," \
                                 "price,created_at,updated_at,wx_code) " \
                                 "values ('{province_code}','{city_code}','{name}','{mobile}','{address}','{type}'," \
                                 "'{category_name}',{price},{created_at},{updated_at},'{wx_code}')". \
                format(province_code=province_code, city_code=city_code, name=name, mobile=mobile, address=address,
                       type=type, category_name=types_category, price=price,
                       created_at=created_at, updated_at=updated_at, wx_code=wx_code)

            db_session.execute(insert_address_sql)

            db_session.commit()
        except Exception:
            print(traceback.format_exc())
            db_session.rollback()
            db_session.close()
            return jsonify({'success': False, 'msg': 'save date error'})
        db_session.close()
        return jsonify({'success': True, 'msg': 'save ok'})


@api_bp.route('/get-orders')
def get_orders():
    """
    我要报修
    :return:
    """

    records = list()
    try:

        insert_address_sql = "SELECT * FROM repair_order"
        res = db_session.execute(insert_address_sql).fetchall()

        for temp in res:
            records.append(dict(temp))

    except Exception:
        print(traceback.format_exc())
        db_session.rollback()
        db_session.close()
        return jsonify({'success': False, 'msg': 'search error'})
    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-member-types')
def get_member_types():
    """
    后台类型列表
    :return:
    """

    records = list()
    try:

        query_address_sql = "SELECT * FROM member_types "
        res = db_session.execute(query_address_sql).fetchall()

        for temp in res:
            records.append(dict(temp))


    except Exception:
        print(traceback.format_exc())
        db_session.rollback()
        db_session.close()
        return jsonify({'success': False, 'msg': 'search error'})
    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-types')
def get_types():
    """
    微信类型列表
    :return:
    """

    records = list()
    try:

        query_address_sql = "SELECT * FROM types "
        res = db_session.execute(query_address_sql).fetchall()

        for temp in res:
            records.append(dict(temp))

    except Exception:
        print(traceback.format_exc())
        db_session.rollback()
        db_session.close()
        return jsonify({'success': False, 'msg': 'search error'})

    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-types-category', methods=["POST"])
def get_types_category():
    """
    获取子类
    :return:
    """
    records = list()
    if request.method == 'POST':
        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        type_id = json_data_dict.get('type_id', '')

    try:

        insert_address_sql = "SELECT * FROM types_category where type_id={type_id}".format(type_id=type_id)
        res = db_session.execute(insert_address_sql).fetchall()
        for temp in res:
            records.append(dict(temp))

    except Exception:
        print(traceback.format_exc())
        db_session.rollback()
        db_session.close()
        return jsonify({'success': False, 'msg': 'search error'})

    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-repair-order', methods=["POST"])
def get_repair_order():
    """
    获取子类
    :return:
    """
    records = list()
    if request.method == 'POST':
        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        status = json_data_dict.get('status', '')
        wx_code = json_data_dict.get('wx_code', '')

    try:

        insert_address_sql = "SELECT * FROM repair_order where status={status} and wx_code='{wx_code}'".format(
            status=status, wx_code=wx_code)
        res = db_session.execute(insert_address_sql).fetchall()
        for temp in res:
            temp = dict(temp)
            temp['price'] = str(temp['price'])
            temp['pay_price'] = str(temp['pay_price'])
            temp['created_at'] = timestamp_to_date(temp['created_at'])
            temp['updated_at'] = timestamp_to_date(temp['updated_at'])

            records.append(temp)

    except Exception:
        print(traceback.format_exc())
        db_session.rollback()
        db_session.close()
        return jsonify({'success': False, 'msg': 'search error'})

    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-member-wxname', methods=["GET"])
def get_member_wxname():
    """
    我要报修
    :return:
    """
    records = list()
    wx_name = request.args.get('wx_name')
    insert_address_sql = "SELECT * FROM member where wx_name='{wx_name}'".format(wx_name=wx_name)
    res = db_session.execute(insert_address_sql).fetchall()
    for temp in res:
        records.append(dict(temp))

    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-member-wxcode', methods=["GET"])
def get_member_wxcode():
    """
    :return:
    """
    records = list()
    wx_code = request.args.get('wx_code')
    insert_address_sql = "SELECT * FROM member where is_member='是' and wx_code='{wx_code}'".format(wx_code=wx_code)
    res = db_session.execute(insert_address_sql).fetchall()
    for temp in res:
        records.append(dict(temp))

    db_session.close()
    return jsonify({'success': True, 'list': records})


@api_bp.route('/get-member-wxcode-update', methods=["GET"])
def get_member_wxcode_update():
    """
    :return:
    """
    wx_code = request.args.get('wx_code')
    query_sql = "SELECT * FROM member where is_member='是' " \
                "and wx_code='{wx_code}' and warranty_time >= 1".format(wx_code=wx_code)
    res = db_session.execute(query_sql).first()

    if res is None:
        return jsonify({'success': False, 'is_member': False})

    res = dict(res)

    if int(res['warranty_time']) > 1:
        update_sql = "update member set warranty_time = {warranty_time} " \
                     "where wx_code='{wx_code}'".format(wx_code=wx_code, warranty_time=(int(res['warranty_time']) - 1))
    if int(res['warranty_time']) == 1:
        update_sql = "update member set is_member = '否' ,warranty_time = {warranty_time} " \
                     "where wx_code='{wx_code}'".format(wx_code=wx_code, warranty_time=(int(res['warranty_time']) - 1))

    try:
        db_session.execute(update_sql)
        db_session.commit()
        db_session.close()
        return jsonify({'success': True})
    except Exception:
        print(traceback.format_exc())
        db_session.rollback()
        db_session.close()
        return jsonify({'success': False})


@api_bp.route('/get-open-id', methods=["POST"])
def get_open_id():
    """
    我要报修
    :return:
    """

    if request.method == 'POST':
        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        app_id = json_data_dict.get('app_id', '')
        code = json_data_dict.get('code', '')
        app_secret = json_data_dict.get('app_secret', '')
    else:
        return jsonify({'success': False, 'msg': 'no post http'})

    try:

        url = "https://api.weixin.qq.com/sns/jscode2session?" \
              "appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code". \
            format(app_id=app_id, app_secret=app_secret, code=code)
        r = requests.get(url)
        wx_res_dict = json.loads(r.text)
        db_session.close()
        return jsonify(
            {
                'success': True,
                'openid': wx_res_dict['openid'], 'session_key': wx_res_dict['session_key'], 'msg': 'get data success'})

    except Exception:
        db_session.close()
        return jsonify({'success': False, 'msg': 'search error'})


@api_bp.route('/save-order-and-payment', methods=["POST"])
def save_order_and_payment():
    """
    保存订单并且请求微信接口获取支付
    :return:
    """
    sn = str(int(time.time())) + get_random(1, 999)
    print(sn)
    db_session.close()
    try:
        return jsonify({'success': True, 'msg': 'error'})
    except Exception:
        return jsonify({'success': False, 'msg': 'error'})


@api_bp.route('/notice-weixin-payment', methods=["POST"])
def notice_weixin_payment():
    """
    微信回调订单是否支付状态
    :return:
    """
    if request.method == 'POST':
        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        # 微信金额保存均已整型保存
        # 比较订单金额以及支付金额是否一致
        total_fee = json_data_dict.get('total_fee', 0)
        total_fee = total_fee / 100
        total_fee = Decimal(total_fee).quantize(Decimal("0.00"))

        settlement_total_fee = json_data_dict.get('settlement_total_fee', 0)
        settlement_total_fee = settlement_total_fee / 100
        settlement_total_fee = Decimal(settlement_total_fee).quantize(Decimal("0.00"))

        # 支付状态为0
        pay_type = 0
        if settlement_total_fee == total_fee:
            # 支付完成
            pay_type = 1
        elif settlement_total_fee < total_fee:
            # 未支付完
            pay_type = 2

        # 商家订单号
        out_trade_no = json_data_dict.get('out_trade_no', 0)

        #  微信订单号
        transaction_id = json_data_dict.get('transaction_id', 0)

        # 下单时间
        time_end = json_data_dict.get('time_end', 0)
    else:
        return jsonify({'return_code': 'FAIL'})

    # 验证签名 todo...

    try:
        # 修改订单数据
        update_sql = "update repair_order set pay_type={pay_type}, transaction_id={transaction_id}, " \
                     "pay_price = {settlement_total_fee} ,time_end ={time_end} where sn={sn} ". \
            format(pay_type=pay_type, transaction_id=transaction_id, settlement_total_fee=settlement_total_fee,
                   time_end=time_end, sn=out_trade_no)

        db_session.execute(update_sql)
        db_session.commit()
        db_session.close()
        return jsonify({'return_code': 'SUCCESS'})
    except Exception:
        db_session.rollback()
        db_session.close()
        return jsonify({'return_code': 'FAIL'})


@api_bp.route('/weixin-pay', methods=["POST"])
def weixin_pay():
    """
    微信下单支付接口
    :return:
    """
    if request.method == 'POST':
        data = request.get_data()
        json_data_dict = json.loads(data.decode("utf-8"))

        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        data = dict()

        # 小程序ID 前端获取
        app_id = json_data_dict['appid']
        data['appid'] = app_id
        # 商户号 前端获取
        data['mch_id'] = json_data_dict['mch_id']
        # 获取时间戳信息
        time_stamp = json_data_dict['timeStamp']

        # open_id
        data['openid'] = json_data_dict['open_id']

        # API 秘钥KEY
        api_key = json_data_dict['api_key']
        # api_key = 'J4sQ3YdrgAyrUznO13KKDE7e5D3j1cJz'

        str_random = str(int(time.time()) + random.randint(1, 1000))
        nonce_str = md5(str_random)

        # 随机字符串
        data['nonce_str'] = nonce_str
        # 商品名称
        data['body'] = 'service'

        # 下单金额 前端获取 微信规则必须是整数
        data['total_fee'] = int(json_data_dict['total_fee'] * 100)
        # data['total_fee'] = 7500
        # 终端IP，由前端获取
        data['spbill_create_ip'] = json_data_dict['ip']
        # 线上通知回调地址
        data['notify_url'] = 'http://yije.xiusha.net/notice-weixin-payment'
        # 交易类型
        data['trade_type'] = 'JSAPI'
        # data['trade_type'] = 'NATIVE'

        # 订单号由订单生成时产生 todo
        data['out_trade_no'] = json_data_dict['out_trade_no']

        # todo ...
        total_fee = json_data_dict['total_fee']

        # 生成md5算法的sign
        sort_dict_key = sorted(data.keys())
        key_value_str_list = list()
        for k in sort_dict_key:
            key_value_str = "{k}={v}".format(k=k, v=data[k])
            key_value_str_list.append(key_value_str)

        string_sign_temp = "&".join(key_value_str_list) + '&key={key}'.format(key=api_key)

        sign = md5(string_sign_temp).upper()

        data['sign'] = sign

        xml_data = dict_to_xml(data)

        rep = client_post_xml_data_requests(url, xml_data)
        # print(data)
        xml_res_str = rep.text.encode('raw_unicode_escape').decode()

        res = xml_to_dict(xml_res_str)

        db_session.close()
        if res.get('return_code', '') == 'SUCCESS':

            data = dict()
            data['appId'] = app_id
            data['timeStamp'] = time_stamp
            str_random = str(int(time.time()) + random.randint(1, 1000))
            data['nonceStr'] = md5(str_random)
            data['package'] = 'prepay_id={prepay_id}'.format(prepay_id=res.get('prepay_id', ''))
            data['signType'] = 'MD5'

            sort_dict_key = sorted(data.keys())
            key_value_str_list = list()
            for k in sort_dict_key:
                key_value_str = "{k}={v}".format(k=k, v=data[k])
                key_value_str_list.append(key_value_str)

            string_sign_temp = "&".join(key_value_str_list) + '&key={key}'.format(key=api_key)
            sign = md5(string_sign_temp).upper()
            data['paySign'] = sign

            # return jsonify({'return_code': 'SUCCESS', 'xml_data':xml_data,'prepay_id':res.get('prepay_id',''),"sign":res.get('sign','')})
            return jsonify({'return_code': 'SUCCESS', 'data': data, 'string_sign_temp': string_sign_temp})
        else:
            return jsonify({'return_code': 'FAIL', 'msg': xml_res_str})

    else:
        db_session.close()
        return jsonify({'return_code': 'FAIL'})

# @api_bp.route('/weixin-request-payment', methods=["POST"])
# def weixin_request_payment():
#     if request.method == 'POST':
#         http_data = request.get_data()
#         json_data_dict = json.loads(http_data.decode("utf-8"))
#
#         data = dict()
#         data['timeStamp'] = int(time.time())
#
#         str_random = str(int(time.time()) + random.randint(1, 1000))
#         data['nonceStr'] = md5(str_random)
#         data['package'] = json_data_dict['package']
#         data['signType'] = 'MD5'
#         api_key = json_data_dict['api_key']
#
#         # 生成md5算法的sign
#         sort_dict_key = sorted(data.keys())
#         key_value_str_list = list()
#         for k in sort_dict_key:
#             key_value_str = "{k}={v}".format(k=k, v=data[k])
#             key_value_str_list.append(key_value_str)
#
#         string_sign_temp = "&".join(key_value_str_list) + '&key={key}'.format(key=api_key)
#
#         sign = md5(string_sign_temp).upper()
#
#         data['paySign'] = sign
