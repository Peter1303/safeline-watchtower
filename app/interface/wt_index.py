#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

import json

import tornado


class Index(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(200)
        self.finish(json.dumps({'code': 404, 'msg': '不存在的'}))
