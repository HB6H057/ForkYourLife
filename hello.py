#!env/bin/python

import os
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default="8080", help="run on the given port", type=int)

SETTING = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    cookie_secret='buyayongroot'
)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        name = None
        if not self.current_user:
            name = self.get_secure_cookie('user')

        self.render('default.html', name=name)

class ResultHandler(BaseHandler):
    def firend(self, name):
        return 'my dear firend %s' % (name)

    def post(self):
        greeting = self.get_argument('name', 'Guest')

        if greeting == 'hacker':
            self.redirect('/test')
        elif greeting != 'Guest' and not self.current_user:
            self.set_secure_cookie('user', greeting)

        self.render('result.html', greeting=greeting, firend=self.firend,
                    path=self.request.path, headers=self.request.headers)

class HTTPErrorHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(403)


if __name__ == '__main__':

    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers = [
            (r'/', IndexHandler),
            (r'/result', ResultHandler),
            (r'/test', HTTPErrorHandler),
            (r'/(static_file\.txt)', tornado.web.StaticFileHandler,
                                     dict(path=SETTING['static_path'])),
        ],
        **SETTING
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
