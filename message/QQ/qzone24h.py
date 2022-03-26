# -*- coding: utf-8 -*-
import time

from . import qzone
import tieba
from . import utils
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 搜索QQ空间过去24小时内容

qzone_searcher = qzone.QzoneSearcher()

if __name__ == '__main__':
    qzone_searcher.search_history_24h()
