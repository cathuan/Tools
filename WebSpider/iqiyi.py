import requests
import re

"""
First get the qipuId of a video

with two parameters:
    apiKey
    keyWord (title of the video)

and use regular expression to find the qipuId

match = re.search(r'"qipuId":([0-9]+)', r.content)
qipuId = int(match.group().split(":")[1])

and we should save this information in a table so we can retrive it in the future
"""

"""
Next, use qipuId to retrive playcnt

Two parameters, obvious
r = request.get("http://expand.video.iqiyi.com/api/album/info.json?apiKey=71c300df4a7f4e89a43d8e19e5458e6f&qipuId=%s" % 930572700)

and use regular expression to get the count

print re.search(u'"playcnt":[0-9]+', r.content).group()
"""

r = requests.get(b"http://expand.video.iqiyi.com/api/search/list.json?type=list&apiKey=71c300df4a7f4e89a43d8e19e5458e6f&keyWord=【直拍】小组对决《PPAP》王子异")
match = re.search(u'"playcnt":[0-9]+', r.content)
print match.group()
