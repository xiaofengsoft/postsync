# -*- coding: utf-8 -*-
import sys
import json


def handle_global_exception(e):
    return handle_global_exception_with_exception(*sys.exc_info())


def handle_global_exception_with_exception(exc_type, exc_value, exc_traceback):
    """
    Global exception handler
    To be used with try-except block
    """
    exc_json_map = {'code': -1, 'message': exc_value.__str__(), 'data': {
        'type': exc_type.__name__.__str__(),
        'value': exc_value.__str__(),
        'traceback': exc_traceback.__str__()
    }}
    exc_json_map_msg = json.dumps(exc_json_map)
    print(exc_json_map_msg)
    return exc_json_map



