#  Author: Peter1303
#  Date: 2024/6/11
#  Copyright (c) 2024.

class ParamException(Exception):
    def __init__(self, message='参数错误'):
        self.message = message

    def __str__(self):
        return self.message
