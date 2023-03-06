import tornado.ioloop
import tornado.web


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world from Tornado!!!!!")


class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("httpServerTornado.html")


def isPrime(param):
    param = param
    if param > 1:
        for i in range(2, param):
            if (param % i) == 0:
                return False
                break
        else:
            return True
    else:
        return False


class queryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        n = self.get_argument("n")
        self.write(f"Number {n} is prime?  {isPrime(int(n))}")


class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, resource_id):
        self.write(f"Resource id: {resource_id}")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/blog", staticRequestHandler),
        # (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/isPrime", queryStringRequestHandler),
        (r"/resources/([0-9]+)", resourceRequestHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
