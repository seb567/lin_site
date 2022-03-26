# -*- coding: utf-8 -*-
import time
import traceback

from . import qzone
from . import utils
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 提前结束通过 ctrl+c

# 每次抓取数据后的休息时间(单位是秒)
sleep_time_sec = 1200
# 出问题之后重启时间(单位是秒)
restart_time_sec = 10


# 注意！
# 将带有 or 逻辑的 "关键词.txt"
# 翻译为对应笛卡尔积的 "keywords.txt"
# 如果不需要翻译可以在下面这行之前加 "# "
utils.keywords_trans()

qzone_searcher = qzone.QzoneSearcher()

utils.write_gather_time_ticks()

def start():
    while True:
        try:
            qzone_searcher.run()
        except Exception as e:
            traceback.print_exc()
            print(f'遇到问题:\n{e}\n{restart_time_sec}秒后自动启动\n')
            time.sleep(restart_time_sec)
        else:
            time.sleep(sleep_time_sec)
