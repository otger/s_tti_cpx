#!/usr/bin/python
# -*- coding: utf-8 -*-
from entropyfw import System
from s_tti_cpx.module import EntropyTTiCPX
import time

"""
system
Created by otger on 19/04/17.
All rights reserved.
"""


class SystemTTiCPX(System):

    def __init__(self, flask_app):
        System.__init__(self, flask_app)
        self.add_module(EntropyTTiCPX())


if __name__ == "__main__":
    from entropyfw.logger import log, formatter
    import logging
    from gevent.wsgi import WSGIServer
    from flask import Flask, url_for

    from flask.templating import DispatchingJinjaLoader

    app = Flask(__name__)
    server = WSGIServer(("", 5000), app)
    server.start()


    @app.errorhandler(Exception)
    def all_exception_handler(error):
        log.exception('Whatever exception')

    @app.errorhandler(404)
    def handle_bad_request(e):
        log.exception('Whatever exception')

    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        for line in sorted(output):
            print(line)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    s = SystemTTiCPX(flask_app=app)
    print(app.url_map)

    # log.info('Created system')
    # r = s.activate_timer(2)
    # r.wait_answer()
    # log.info("Sum('a', 'b') returned: {0}".format(r.return_value))
    # s.list_functionality()
    #
    # time.sleep(10)
    # r = s.stop_timer()
    # log.info('Asked stop timer')
    # r.wait_answer()
    #
    # time.sleep(5)

    # list_routes()
    try:
        server.serve_forever()
    finally:
        s.exit()
