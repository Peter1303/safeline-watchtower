#  Author: Peter1303
#  Date: 2024/7/29
#  Copyright (c) 2024.

import tornado
import logging
import module.notify as notify
from tornado.options import define, options
from module.config import *


def print_banner():
    banner = """ __        __    _       _   _____                      
 \ \      / /_ _| |_ ___| |_|_   _|____      _____ _ __ 
  \ \ /\ / / _` | __/ __| '_ \| |/ _ \ \ /\ / / _ \ '__|
   \ V  V / (_| | || (__| | | | | (_) \ V  V /  __/ |   
    \_/\_/ \__,_|\__\___|_| |_|_|\___/ \_/\_/ \___|_|   
    """
    print(banner)


def make_app():
    from interface import wt_index
    from interface import wt_run

    return tornado.web.Application([
        (r'/api/?', wt_run.WatchTowerRun),
        (r'(.*)', wt_index.Index),
    ])


def init_config(path):
    config = Config(config_path=path)
    active = config.get(const.Yml.active)
    notify.active = active
    notify.init()
    for key in active:
        notifier = notify.notifiers[key]
        notifier_config = config.get(key)
        notifier.template = notifier_config.get(const.Yml.template, '')
        notifier.rule_filter = notifier_config.get(const.Yml.rule_filter, {})
        if key == const.Yml.we_com:
            notifier.key = notifier_config.get(const.Yml.key)


if __name__ == '__main__':
    print_banner()
    define("port", default=8015, type=int, help='指定运行时端口号')
    define("host", default='0.0.0.0', type=str, help='指定运行时监听地址')
    define("config_path", default=None, type=str, help='指定配置文件路径')

    options.logging = None
    tornado.options.parse_command_line()
    host = options.host
    port = options.port

    logging.getLogger("tornado.access").setLevel(logging.CRITICAL)
    logging.getLogger("tornado.application").setLevel(logging.CRITICAL)

    app = make_app()

    curr_path = os.path.dirname(os.path.abspath(__file__))

    if options.config_path:
        init_config(options.config_path)
    else:
        init_config(os.path.join(curr_path, 'config'))

    server = tornado.httpserver.HTTPServer(app)
    server.bind(port=port, address=host)
    server.start(1)
    print(f'Running: http://{host}:{port}')
    tornado.ioloop.IOLoop.current().start()
