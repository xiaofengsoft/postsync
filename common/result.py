from flask import jsonify


class Result(object):
    def __init__(self, code, data=None, message="成功"):
        self.code = code
        self.message = message
        self.data = data

    @staticmethod
    def success(data=None, message="成功"):
        return Result(0, data, message).__str__()

    @staticmethod
    def error(data=None, message="失败"):
        return Result(-1, data, message=message).__str__()

    @staticmethod
    def build(code, data=None, message="异常"):
        return Result(code, data, message).__str__()

    def __str__(self):
        return jsonify({"code": self.code, "message": self.message, "data": self.data})

    def __repr__(self):
        return self.__str__()
