# -*- coding: UTF-8 -*-
# from __future__ import print_function
import requests
import datetime
import json
# import sys


def to_csv_line(*args):
    """Helper function to put outputs into ',' sperated csv format for future usage
    """

    return ",".join(str(v) for v in args)


if __name__ == "__main__":

    start_time = datetime.datetime.now()
    r = requests.get("http://vote.i.iqiyi.com/eagle/outer/get_votes?uid=null&vids=0536210296010472&t=1518343644386")
    end_time = datetime.datetime.now()
    data = json.loads(r.content)
    options = data["data"][0]["childs"][0]["options"]

    for option in options:
        name = option["text"].encode("utf-8").strip()  # encode utf-8 for chinese character strings
        showNum = option["showNum"]
        vipJoins = option["vipJoins"]
        print to_csv_line(start_time, end_time, name, showNum, vipJoins)

    for key, value in option.items():
        print key, value
