# -*- coding: utf-8 -*-
import time

from . import tieba
from . import utils
from .import setting
from importlib import reload
import urllib3
from . import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 提前结束通过 ctrl+c


# 注意！
# 将带有 or 逻辑的 "关键词.txt"
# 翻译为对应笛卡尔积的 "keywords.txt"
# 如果不需要翻译可以在下面这行之前加 "# "

config._init()
config.set_value('sleep_time_sec', '60')
config.set_value('restart_time_sec', '60')
config.set_value('n_loop', '1')
config.set_value('max_page', '10')
config.set_value('one_page_interval', '10')
config.set_value('record_time', '2022-02-19 22:20:00')
def start():
    while True:
        #reload(config)
        # 每次抓取数据后的休息时间(单位是秒)
        sleep_time_sec = int(config.get_value('sleep_time_sec'))
        # 出问题之后重启时间(单位是秒)
        restart_time_sec = int(config.get_value('restart_time_sec'))
        # 每次搜索的轮数
        n_loop = int(config.get_value('n_loop'))
        #print(sleep_time_sec)

        start_date = config.get_value('record_time')

        max_page = int(config.get_value('max_page'))
        one_page_interval = int(config.get_value('one_page_interval'))

        print(f'配置的参数: {sleep_time_sec},{restart_time_sec},{n_loop},{max_page},{one_page_interval},{start_date}')
        
        utils.keywords_trans()
        tieba_searcher = tieba.TiebaSearcher("剑网三交易", start_date)

        utils.write_gather_time_ticks() 
        try:
            #print(sleep_time_sec)
            tieba_searcher.run(n_loop)
        except Exception as e:
            print(f'遇到问题:\n{e}\n{restart_time_sec}秒后自动启动\n')
            time.sleep(restart_time_sec)
        else:
            time.sleep(sleep_time_sec)
