
class Result(object):
    def __init__(self, code, message="成功", data=None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return "Result(code={}, message={}, data={})".format(self.code, self.message, self.data)

    def __repr__(self):
        return self.__str__()