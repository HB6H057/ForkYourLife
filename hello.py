#!env/bin/python

import os
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default="8080", help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('default.html')

class ResultHandler(tornado.web.RequestHandler):
    def firend(self, name):
        return 'my dear firend %s' % (name)

    def post(self):
        greeting = self.get_argument('name', 'Guest')
        self.render('result.html', greeting=greeting, firend=self.firend)


if __name__ == '__main__':

    handler_list = [
        (r'/', IndexHandler),
        (r'/result', ResultHandler),
    ]

    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=handler_list,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
