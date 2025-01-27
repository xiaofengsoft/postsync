from common.core import Community


class Test(Community):

    conf = {
        "category": "科技",
        "columns": ["Python"],
        "cover": None,
        "tags": ["Python"],
        "timeout": 40000,
        "topic": None,

    }

    def __init__(self):
        super().__init__()
