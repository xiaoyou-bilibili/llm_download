GOOGLE_SPIDER = "google-spider"


class Base:
    def __init__(self):
        self.http_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
        }
        self.proxy = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
        self.openapi_key = "sk-xxx"
        self.openapi_base = "https://xxx"
        self.max_size = 2  # 最大链接个数
