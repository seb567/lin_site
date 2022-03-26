# 每次抓取数据后的休息时间(单位是秒)
sleep_time_sec = 60
# 出问题之后重启时间(单位是秒)
restart_time_sec = 10
# 每次搜索的轮数
n_loop = 1
# 每次抓取数据后的休息时间(单位是秒)
max_page = 35

#搜索一页的休息时间
one_page_interval = 12

#中断flag
run_flag = 1

#搜索开始时间
record_time = "2022-02-13 15:30:00"

def _init():#初始化
    global config_dict
    config_dict = {}
 
 
def set_value(key,value):
    config_dict[key] = value
 
 
def get_value(key,defValue=None):
    try:
        return config_dict[key]
    except KeyError:
        print("无法找到对应的配置")