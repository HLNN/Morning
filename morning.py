import time
import requests
import re


class MORNING:
    def __init__(self):
        self.key = "ServerChanKey"
        self.session = requests.Session()
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",}
        self.session.headers.update(header)
        self.urlBase = "http://dean.xjtu.edu.cn/"

    def dean(self):
        urlBase = "http://dean.xjtu.edu.cn/jxxx/{}.htm"
        contents = {"xwdt": "新闻动态", "xytz": "学业通知", "zhtz": "综合通报",}

        res = ["" + "**<h1>教务处</h1>**"]
        for content in contents:
            r = self.session.get(urlBase.format(content))
            if not r.status_code == 200:
                return
            r.encoding = "utf-8"
            text = r.text
            lines = re.findall(r'id="line_u8_.*?time">(.*?)<.*?href="(.*?)".*?title="(.*?)"', text, re.S)

            def timeToKeep(strTime):
                return time.time() - time.mktime(time.strptime(strTime, "%Y-%m-%d")) < 3600 * 24 * 3
            lines = [line for line in lines if timeToKeep(line[0])]

            if lines:
                res += ["**" + contents[content] + "**"]

                for line in lines:
                    res += ["**[{time}][{title}]({url})**".format(time=line[0], title=line[2], url=self.urlBase + line[1][3:])]

                    print(line[2])
                    r = self.session.get(self.urlBase + line[1][3:])
                    if r.status_code == 200:
                        r.encoding = "utf-8"
                        div = re.findall(r'"vsb_content(.*?)</div', r.text, re.S)
                        p = re.findall(r'<p.*?>(.*?)</p', div[0], re.S)
                        if not re.search(r'span', p[0]):
                            spans = p
                        else:
                            spans = ["".join(re.findall(r'<span.*?>(.*?)<', p[i], re.S)) for i in range(len(p))]
                        if not spans:
                            continue

                        if len(spans) > 1 and spans[0] and spans[0][-1] == "：":
                            info = spans[1]
                            print(spans[0][-1])
                        else:
                            info = [spans[0]]
                        
                        if info: res += ["    " + re.subn(r'&nbsp;', "", info)[0],]
                        print(spans)


        return res + ["Have a nice day", "Best"]

    def message(self, key, title, body):
        msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
        requests.get(msg_url)

    def main(self):
        lines = morning.dean()
        payload = "\n\n".join(lines)
        morning.message(self.key, "每日早报", payload)


if __name__ == "__main__":
    morning = MORNING()
    morning.main()
