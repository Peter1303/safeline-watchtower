#  Author: Peter1303
#  Date: 2024/7/29
#  Copyright (c) 2024.

import requests

from module.logger import *
from module.notify import Notifier


class WeComNotify(Notifier):
    _template_api = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='

    def __init__(self):
        super().__init__()
        self._api = ''
        self._key = ''

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_value):
        self._key = new_value
        self._api = self._template_api + self._key

    def notify(self, event):
        try:
            content = self.convert(event)
            data = {
                'msgtype': 'text',
                'text': {
                    'content': content
                }
            }
            resp = requests.post(self._api, json=data)
            res = resp.json()
            if res['errcode'] == 0:
                logger.info('发送微信通知成功')
            else:
                logger.error(f'发送微信通知失败 | {res}')
        except Exception as e:
            logger.error(f'wecom: {e}')
