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
        username_session = session.get('username', None)
        if username_session != 'admin_login':
            # return redirect(url_for('admin_bp.admin_index'))
            return redirect('/')

        return view(**kwargs)

    return _
