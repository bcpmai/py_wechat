# -*- coding: utf-8 -*-
import time
import xml.sax.handler
import hashlib
import requests
import random


class XMLHandler(xml.sax.handler.ContentHandler):
    """
    子类实现xml功能
    """

    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def get_dict(self):
        return self.mapping


def xml_to_dict(xml_str):
    """
    转换xml为字典
    :param xml_str:
    :return:
    """
    xh = XMLHandler()
    xml.sax.parseString(xml_str.encode(), xh)
    ret = xh.get_dict()
    return ret


def dict_to_xml(target_dict):
    """
    转换字典为xml
    :param target_dict:
    :return:
    """
    item = ""
    for k, v in target_dict.items():
        item += "<{k}>{v}</{k}>".format(k=k, v=v)

    message = "<xml>" + item + "</xml>"
    return message


def md5(target_str):
    """
    随机生成字符串
    :param target_str:
    :return:
    """
    m = hashlib.md5()
    b = target_str.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()

    return str_md5


def client_post_xml_data_requests(request_url, request_xml_data):
    """
    功能说明：发送请求报文到指定的地址并获取请求响应报文
    输入参数说明：接收请求的URL，xml请求报文数据
    输出参数：请求响应报文
    :param request_url:
    :param request_xml_data:
    :return:
    """

    head = {"Content-Type": "text/xml; charset=UTF-8", 'Connection': 'close'}

    # 客户端发送请求报文到服务端
    r = requests.post(request_url, data=request_xml_data, headers=head)
    # 客户端获取服务端的响应报文数据

    # 返回请求响应报文
    return r


def get_random(star, end):
    """
    获取随机数
    :return:
    """
    r = random.randint(star, end)
    res_random = r
    if r < 10:
        res_random = '0' + '0' + str(r)
    if r >= 10 and r < 100:
        res_random = '0' + str(r)

    return str(res_random)


def timestamp_to_date(time_stamp):
    """
    时间戳转日期
    :param time_stamp:
    :return:
    """
    time_array = time.localtime(time_stamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)
