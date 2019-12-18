#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket

from flaskr import create_app

app = create_app()


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, debug=True)
    if socket.gethostname() in ['bcpmai-win10', 'bcpmai-mac-15']:
        app.run(host='127.0.0.1', port=5000, debug=True)
    else:
        ssl_crt = os.path.join(os.path.dirname(app.instance_path), '3189443_yijie.xiusha.net_public.crt')
        ssl_key = os.path.join(os.path.dirname(app.instance_path), '3189443_yijie.xiusha.net.key')
        app.run(host='127.0.0.1', port=5000, debug=True, ssl_context=(ssl_crt, ssl_key))
