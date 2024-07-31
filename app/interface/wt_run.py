#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.
import asyncio
import json

import tornado

import module.notify as notify
from exception.param_exception import ParamException
from module.config import Config
from module.logger import *

config = Config(config_path='./config/', name='config.yml')


def resp_data(code=200, msg='OK', data=None):
    resp = {
        'code': code,
        'msg': msg
    }
    if data is not None:
        resp['data'] = data
    return json.dumps(resp)


class WatchTowerRun(tornado.web.RequestHandler):
    def log_request(self):
        ip = self.request.remote_ip
        path = self.request.path
        method = self.request.method
        logger.info(f'{method} {ip} {path}')

    def get(self):
        self.set_status(200)
        self.log_request()
        self.finish(resp_data(404, '不存在的'))

    @tornado.gen.coroutine
    def post(self):
        self.set_status(200)
        self.log_request()
        try:
            body = self.request.body
            try:
                arr = json.loads(body)
                # 判断 arr 是否为一个数组
                if not isinstance(arr, list):
                    raise ParamException()
            except Exception:
                raise ParamException()
            # 推送通知
            asyncio.create_task(notify.notify(arr))
            self.finish(resp_data())
        except ParamException as e:
            self.finish(resp_data(400, e.message))
        except Exception as e:
            logger.error(e)
            self.finish(resp_data(500, str(e)))
