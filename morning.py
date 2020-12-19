import time
import requests
import re

import module


class MORNING:
    def __init__(self):
        self.key = "ServerChanKey"
        self.title = "每日早报"
        self.session = requests.Session()
        self.header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",}
        self.session.headers.update(self.header)

        self.lines = []

    def message(self, key, title, body):
        msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
        requests.get(msg_url)

    def main(self):
        dean = module.DEAN(self.session)
        self.lines += dean.run()

        self.lines += ["Have a nice day", "Best"]
        payload = "\n\n".join(self.lines)
        morning.message(self.key, self.title, payload)


if __name__ == "__main__":
    morning = MORNING()
    morning.main()
