import re
import time

import requests

from .utils import PLUGGING


class DEAN(PLUGGING):
    def __init__(self, session):
        super().__init__(session)
        self.name = "教务处"

        self.urlBase = "http://dean.xjtu.edu.cn/"
        self.urlPage = "http://dean.xjtu.edu.cn/jxxx/{content}.htm"
        self.contents = {"xwdt": "新闻动态", "xytz": "学业通知", "zhtz": "综合通报",}
        self.daysToKeep = 3

        self.res = ["" + "**{name}**".format(name=self.name)]

    def run(self):
        for content in self.contents:
            r = self.session.get(self.urlPage.format(content=content))
            if not r.status_code == 200:
                continue
            r.encoding = "utf-8"
            text = r.text
            lines = re.findall(r'id="line_u8_.*?time">(.*?)<.*?href="(.*?)".*?title="(.*?)"', text, re.S)

            def timeToKeep(strTime):
                return time.time() - time.mktime(time.strptime(strTime, "%Y-%m-%d")) < 3600 * 24 * self.daysToKeep
            lines = [line for line in lines if timeToKeep(line[0])]

            if lines:
                self.res += ["**{content}**".format(content=self.contents[content])]

                for line in lines:
                    # Line = [time, url, title]
                    print(line)
                    self.res += ["**[{time}][{title}]({url})**".format(time=line[0], title=line[2], url=self.urlBase + line[1][3:])]

                    r = self.session.get(self.urlBase + line[1][3:])
                    if r.status_code == 200:
                        r.encoding = "utf-8"
                        div = re.findall(r'"vsb_content(.*?)</div', r.text, re.S)
                        p = re.findall(r'<p.*?>(.*?)</p', div[0], re.S)
                        if not re.search(r'span', p[0]):
                            spans = p
                        else:
                            spans = ["".join(re.findall(r'>(.*?)</', p[i], re.S)) for i in range(len(p))]
                        if not spans:
                            continue
                        spans = [span for span in spans if span and span != " "]

                        if len(spans) > 1 and spans[0] and spans[0][-1] == "：":
                            info = spans[1]
                        else:
                            info = spans[0]
                        
                        if info: 
                            info = re.subn(r'&nbsp;', "", info)[0]
                            info = re.subn(r'<.*?>', "", info)[0]
                            self.res += ["    " + info,]
                        print(spans)

        return self.res
