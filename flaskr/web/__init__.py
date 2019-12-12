# -*- coding: utf-8 -*-

import functools
from flask import session, redirect, url_for


def login_required(view):
    """
    登陆装饰器
    :param view:
    :return:
    """
    @functools.wraps(view)
    def _(**kwargs):
        if session.get('admin_name', None) is None:
            return redirect(url_for('admin_bp.admin_login'))

        return view(**kwargs)

    return _
