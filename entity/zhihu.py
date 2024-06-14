from entity.community import Community
from playwright.sync_api import sync_playwright

class Zhihu(Community):
    url_post_new = "https://zhuanlan.zhihu.com/write"

    def __init__(self):
        super().__init__()

    async def async_post_new(self, title: str, digest: str, content: str, file_path: str = None, tags: list = None,
                 category: str = None, cover: str = None, columns: list = None, topic: str = None) -> str:
        # self.page.goto(self.url_post_new)
        api_request_context = self.browser.request
        resp = api_request_context.get("zhuanlan.zhihu.com/api/autocomplete/topics",
                                       params={
                                       "token": "a",
                                       "max_matches": 5,
                                       "use_similar": 0,
                                       "topic_filter": 1
                                       })
        print(resp.body())

    def upload_img(self, img_path: str) -> str:
        pass

    def convert_html_img_path(self, content: str, file_path: str) -> str:
        pass


