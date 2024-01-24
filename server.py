from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from web import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(5000)
IOLoop.current().start()