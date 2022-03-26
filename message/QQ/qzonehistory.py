# -*- coding: utf-8 -*-
import time

from . import qzone
from . import utils
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 搜索QQ空间过去24小时内容

qzone_searcher = qzone.QzoneSearcher()

if __name__ == '__main__':
    # eg
    # 2020-10-26 20:00:18
    # data = "2020-10-26 20:00:18"
    data = ""
    qzone_searcher.search_history_24h(data)
