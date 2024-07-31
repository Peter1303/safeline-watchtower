#  Author: Peter1303
#  Date: 2024/7/29
#  Copyright (c) 2024.
import re

import const
from module.logger import *

active = []
notifiers = {}


class Notifier:
    def __init__(self):
        self.template = ''
        self.rule_filter = {}

    def notify(self, events):
        raise NotImplementedError('没有实现通知方法')

    def event_filter(self, event):
        rule_filter = self.rule_filter
        rule_id_filter = rule_filter.get(const.Yml.rule_id, {})
        if not rule_id_filter:
            return True
        pattern = rule_id_filter.get(const.Yml.pattern, '')
        if pattern == '':
            return True
        # 正则匹配
        if not re.match(pattern, event[const.Variable.rule_id]):
            return False
        return True

    def convert(self, event):
        """
        将事件转换为通知格式
        :param event: 事件
        :return:
        """
        template = self.template
        if template == '':
            logger.warning('通知模板为空')
            return ''
        for key in event:
            if key not in event:
                continue
            value = event[key]
            if value == '':
                value = '未知'
            template = template.replace(f'{{{key}}}', str(value))
        return template.strip()


def init():
    for name in active:
        trans_name = name.replace('-', '_')
        # 导入模块
        module = __import__(f'notify.{trans_name}', fromlist=['notify'])
        # 初始化模块中的通知类
        for module_name in dir(module):
            # 必须以 Notify 结尾
            if module_name.endswith('Notify'):
                notifier = getattr(module, module_name)
                obj = notifier()
                notifiers[name] = obj
                break
        logger.info(f'{name} 通知模块加载成功')


async def notify(events):
    for notifier in notifiers.values():
        for event in events:
            if not notifier.event_filter(event):
                continue
            notifier.notify(event)
