# -*- coding: utf-8 -*-
import os
import requests

import re
import json
import time

from itertools import product
import random

#######################################
# ----------- general I/O ----------- #
#######################################
sep = os.sep
# 全局统计结果
gather_file_path = '结果.txt'

# 得到所有体型列表
with open(f'input{sep}体型.txt', 'r', encoding='utf-8') as f:
    body_type = f.read().split('\n')


def get_tieba_or_qq(path):
    ''' 读取文件得到需要查询的所有贴吧或QQ列表'''
    with open(path, 'r', encoding='utf-8') as f:
        tieba_list = f.read().split('\n')
    return tieba_list


def get_keywords(path):
    ''' 读取文件得到关键词列表
        返回的是关键词列表, 和关键词与id的关系的字典
    '''
    with open(path, 'r', encoding='utf-8') as f:
        keywords_str_list = f.read().split('\n')

    input_list = [string.split(' ') for string in keywords_str_list]

    # 老版本内容
    # keywords_list = []
    # id_dict = {}

    # for row in input_list:
    #     id_num = row[0]
    #     keywords = row[1:]
    #     keywords_list.append(keywords)
    #     keywords_without_space = del_space(keywords)
    #     id_dict[keywords_without_space] = id_num

    # return keywords_list, id_dict
    # 老版本内容end
    return input_list


def read_file(path):
    ''' 读取文件内容 如果没有则返回空'''
    # if the file is not exist: build it, otherwise pass it
    with open(path, 'a', encoding='utf-8') as f:
        pass
    # read the file
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def write_time_ticks(dir_path, keywords_list):
    ''' 对指定的目录下对应关键词记录时间标签'''
    ticks = get_ticks()
    keywords_without_space_list = [
        del_space(keywords) for keywords in keywords_list]
    for keywords_without_space in keywords_without_space_list:
        file_path = f'{dir_path}{sep}{keywords_without_space}.txt'
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(ticks)


def write_gather_time_ticks():
    ticks = get_ticks()
    with open(gather_file_path, 'a', encoding='utf-8') as f:
        f.write(ticks)


#########################################
# ----------- check content ----------- #
#########################################
def check_all(source, origin_content, keywords, note_dict, result_path=gather_file_path):
    ''' 内容总检查流程'''
    content_list = origin_content.split('\n')
    for content in content_list:
        check_content(source, content, keywords, note_dict, result_path)


def check_content(source, content, keywords, note_dict, result_path=gather_file_path):
    ''' 分行后内容总检查流程'''
    
    # 找到所有括号内容
    # print(content)
    bracket_list = find_bracket(content)
    # print(bracket_list)
    if len(bracket_list) == 0:
        # 没有括号 正常查找
        content_check_keywords(source, content, keywords, note_dict)
    else:
        # 有括号
        key_bracket_list = bracket_has_body(bracket_list)
        if len(key_bracket_list) == 0:
            # 括号没有关键词
            content_check_keywords(source, content, keywords, note_dict)
        else:
            # 有关键词
            for bracket in key_bracket_list:
                # 对于一个具体的括号匹配的内容 如“喵萝1k3”
                body, price = get_bracket_body_and_price(bracket)
                # print(f'体型:{body}, 价格:{price}')
                if ((price == 0) or (price <= int(keywords[1]) and body == keywords[2])):
                    content_check_keywords(source, content, keywords, note_dict, result_path)


def get_bracket_body_and_price(bracket):
    ''' 返回括号内的体型关键词和价格关键词'''
    # 找 body
    for item in body_type:
        if item in bracket:
            body = item
            break
    # 找 price
    price = find_price(bracket)
    return body, price
    

def find_price(string):
    string = string.upper()
    pattern = re.compile(r'\d+[KW]*\d*')
    res = re.findall(pattern, string)
    
    if len(res) == 0:
        return 0
    else:
        res = re.findall(pattern, string)[0]
    
    if 'K' in res:
        res = re.sub(r'K+', '.', res)
        res = float(res) * 1000
    elif 'W' in res:
        res = re.sub(r'W+', '.', res)
        res = float(res) * 10000
    return int(res)


def bracket_has_body(bracket_list):
    res = []
    for bracket in bracket_list:
        has_a_body_type = any([item in bracket for item in body_type])
        if has_a_body_type:
            res.append(bracket)
    return res


def content_check_keywords(source, content, keywords, note_dict, result_path=gather_file_path):
    ''' 检查内容是否包含关键词
        如果包含则写入文件
    '''
    if content_has_keywords(content, keywords[2:]):
        if not flicker(content, note_dict, keywords[0]):
            print_info(source, content, keywords, result_path)


def flicker(content, note_dict : dict, id_num : str, max_length = 10):
    ''' 记录新内容到 note_dict 看看是不是新表
        return:
        True: 是老内容
        False: 是新内容
    '''
    cut_str = content[-20:]
    
    if id_num not in note_dict.keys():
        note_dict[id_num] = [cut_str]
        return False

    note_list = note_dict[id_num]

    if cut_str not in note_list:
        note_list.append(cut_str)
        if len(note_list) > max_length:
            note_list.pop(0)
        return False
    # else cut_str in note_list
    note_list.remove(cut_str)
    note_list.append(cut_str)
    return True


def find_bracket(content):
    ''' 查找内容是否含有括号
        1. 【】
        2. 『』
    '''
    pattern = re.compile(r'[【『].*?[】』]')
    res = re.findall(pattern, content)
    res = [item[1:-1] for item in res]
    return res


def content_has_keywords(content, keywords):
    ''' is_and 是否对所有关键词是 "与" 操作
        即是否要包括所有关键词
        如果 is_and=False 则是 "或" 操作
        即只要有一个关键词符合都会推送
    '''
    # need to include all keywords
    for item in keywords:
        if content.find(item) < 0:
            # has not find
            return False
    return True


def print_info(source, content, keywords, result_path=gather_file_path):
    # write into the result
    print('发现新内容!')
    print(keywords)
    id_num = keywords[0]

    # mode='a' can create a new file (if it isnot exist)
    content = content.replace('\n', '')
    div_line = '-'*16
    
    output_info = f'【{id_num}】{source}\n{keywords}\n{content}\n{div_line}\n\n'
    print(output_info, end='')

    # gather file
    with open(result_path, 'a', encoding='utf-8') as f:
        f.write(output_info)

#################################
# ----------- utils ----------- #
#################################
def del_space(string_list):
    string_list = [str(s) for s in string_list]
    return ''.join(string_list)


def check_path(path):
    '''This method use to check if the path is exists.
       If not, create that'''
    if not os.path.exists(path):
        os.mkdir(path)


def check_all_dir():
    all_path = [
        f'qzoneLog',
        f'tiebaLog',
        f'result',
        f'result{sep}qzone',
        f'result{sep}tieba',
    ]
    for path in all_path:
        check_path(path)


########################################
# ----------- time related ----------- #
########################################
def get_ticks():
    ''' 获取时间戳'''
    data = time.strftime(' %Y-%m-%d %H:%M:%S ', time.localtime())
    # ticks = f'<====================== {data} ======================>'
    div_len = 20
    div_str = '=' * div_len

    mid_ticks = '<' + div_str + data + div_str + '>'

    ticks = f'\n{mid_ticks}\n'

    return ticks


def get_time_stamp():
    return int(time.time())


def get_time_str():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def time_stamp_2_str(ts):
    # ts: time.time()
    time_array = time.localtime(ts)
    ret = time.strftime("%Y-%m-%d %H:%M:%S",time_array)
    return ret


def str_2_stamp(s):
    # 2020-10-26 20:00:18
    s = s.strip()
    timeArray = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    stamp = int(time.mktime(timeArray))
    return stamp


def get_last_time_str(path='QQ空间记录检查.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        flag = lines[-2]
    
    pattern = re.compile(r'\d+-\d+-\d+\s\d+:\d+:\d+')
    ret = re.findall(pattern, flag)
    return ret[0]


def is_new_post(record_time, post_time):
    if record_time <= post_time:
        return True
    else:
        return False


def get_proxy():
    ''' 选择一个代理'''
    proxy_list = load_proxy_list()
    # 随机选择一个代理
    proxy = random.choice(proxy_list)
    return proxy


def load_proxy_list(path='proxy'):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().split('\n')
    res = []
    for item in text:
        res.append({'http' : item})
    return res

# --------- 关键词转换 --------- #
def trans(string):
    keywords = string.split(' ')
    decare_elem = [item.split('/') for item in keywords]
    decare_product = list(product(*decare_elem))
    res = [' '.join(item) for item in decare_product]
    return res


def keywords_trans():
    with open(f'input{sep}关键词.txt', 'r', encoding='utf-8') as f:
        text_list = f.read().split('\n')

    res = []
    for item in text_list:
        res += trans(item)

    with open(f'input{sep}keywords.txt', 'w+', encoding='utf-8') as f:
        f.write('\n'.join(res))
