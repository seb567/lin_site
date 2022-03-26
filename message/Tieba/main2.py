# -*- coding: utf-8 -*-
import time
from . import tieba
from . import utils
from . import setting
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 提前结束通过 ctrl+c

# 每次抓取数据后的休息时间(单位是秒)
sleep_time_sec = 2500
# 出问题之后重启时间(单位是秒)
restart_time_sec = 110
# 每次搜索的轮数
n_loop = 1

# 注意！
# 将带有 or 逻辑的 "关键词.txt"
# 翻译为对应笛卡尔积的 "keywords.txt"
# 如果不需要翻译可以在下面这行之前加 "# "
utils.keywords_trans()

tieba_searcher = tieba.TiebaSearcher("剑三交易")

utils.write_gather_time_ticks()


def start():
    while not setting.stop_flag:
        try:
            tieba_searcher.run(n_loop)
        except Exception as e:
            print(f'遇到问题:\n{e}\n{restart_time_sec}秒后自动启动\n')
            time.sleep(restart_time_sec)
        else:
            time.sleep(sleep_time_sec)