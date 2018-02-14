# -*- coding: UTF-8 -*-
from __future__ import print_function
import requests
import datetime
import json
import sys


def parse_data(r, params):
    """Save the response to local disk and return an dictionary with parsed json data
    """

    js = json.loads(r.content)
    params_list = ["%s_%s" % (key, value) for key, value in params.items()]
    filename = ".response-%s.json" % ("-".join(params_list))
    with open(filename, "w") as f:
        json.dump(js, f)
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def to_csv_line(*args):
    """Helper function to put outputs into ',' sperated csv format for future usage
    """

    return ",".join(str(v) for v in args)


def request(url, params, timeout=5):
    """Request with try-except block. Decouple the error handling process with actual logic.
    """

    try:
        start_time = datetime.datetime.now()
        r = requests.get(url, params=params, timeout=timeout)
        finish_time = datetime.datetime.now()
        data = parse_data(r, params)
        if data["code"] == "A00000":
            data["start_time"] = start_time
            data["finish_time"] = finish_time
            return data
        else:
            print("Rejected request: ", r.url, file=sys.stderr)
            return None
    except requests.exceptions.ConnectTimeout as e:
        print("Timeout Error", e, file=sys.stderr)
        return None


def get_count_by_qipuId(qipuId):
    """Retrive title and playcounts given a qipuId
    """

    url_retrive_by_qipuId = "http://expand.video.iqiyi.com/api/album/info.json"
    apiKey = "71c300df4a7f4e89a43d8e19e5458e6f"
    params = {"apiKey": apiKey, "qipuId": str(qipuId)}

    data = request(url_retrive_by_qipuId, params, timeout=5)

    # r is None if the request failed.
    if data is not None:
        start_time = data["start_time"]
        finish_time = data["finish_time"]
        count = data["data"]["playcnt"]
        title = data["data"]["desc"].encode("utf-8").strip()  # encode utf-8 for chinese character strings
        print(to_csv_line(start_time, finish_time, title, qipuId, count))


if __name__ == "__main__":
    get_count_by_qipuId(922792900)
