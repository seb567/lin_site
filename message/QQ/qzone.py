# -*- coding: utf-8 -*-
''' 用来检索指定 QQ 的空间内是否包含指定关键词, 只检查最新的 QQ
    每个 QQ 搜索过的最新的内容时间标签用字典的形式记录'created_time'
'''

from . import utils
import requests
from urllib import parse
import os

sep = os.sep


class QzoneSearcher:
    def __init__(self):
        self.qq_path = f'input{sep}qq.txt'
        self.keywords_path = f'input{sep}keywords.txt'
        self.cookie_path = f'input{sep}cookie_file'
        # 已经找到的内容
        self.note_dict = {}
        self.load_data()

    def load_data(self):
        self.qq_list = utils.get_tieba_or_qq(self.qq_path)
        self.keywords_list = utils.get_keywords(self.keywords_path)
        self.cookie = self.get_cookie(self.cookie_path)

        self.time_stamp = {}
        self.update_stamp = {}
        base_stamp = utils.str_2_stamp(
            open('time_stamp_str.txt', 'r').readline())
        for qq in self.qq_list:
            self.time_stamp[qq] = base_stamp
            self.update_stamp[qq] = base_stamp

    def get_cookie(self, path):
        ''' Get cookie from cookie_file'''
        with open(path, encoding='utf-8') as f:
            cookie = f.read()
        cookie = cookie.replace('\n', '')
        return cookie

    def build_headers(self, qq):
        referer = f'http://user.qzone.qq.com/{qq}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
            'accept-encoding': 'gzip, deflate, br',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'cookie': self.cookie,
            'referer': referer,
            'connection': 'keep-alive',
            'upgrade-insecure-requests': '1'
        }
        return headers

    def get_g_tk(self):
        ''' make g_tk value'''
        pskey_start = self.cookie.find('p_skey=')
        pskey_end = self.cookie.find(';', pskey_start)

        # 有时 p_skey 会出现在 cookie 的最后，此时 pskey_end 会返回-1
        # 应该直接取到结束
        if pskey_end == -1:
            p_skey = self.cookie[pskey_start+7:]
        else:
            p_skey = self.cookie[pskey_start+7:pskey_end]

        h = 5381
        for s in p_skey:
            h += (h << 5) + ord(s)

        return h & 2147483647

    def build_url(self, qq):
        g_tk = self.get_g_tk()
        params = {
            'cgi_host': 'http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
            'code_version': 1,
            'format': 'jsonp',
            'inCharset': 'utf-8',
            'need_private_comment': 1,
            'notice': 0,
            'num': 20,
            'outCharset': 'utf-8',
            'sort': 0,
            'g_tk': g_tk,
            'hostUin': qq,
            'uin': qq,
        }
        host = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        url = host + parse.urlencode(params)
        return url

    def run(self):
        n = len(self.qq_list)
        self.pass_qq_list = []
        self.start_new_search()
        l = len(self.pass_qq_list)
        if l > 0:
            print(f'<<<<<< QQ 第 1 轮搜索: 成功 {n-l} 次 失败 {l} 次 | 开始 2 轮搜索 >>>>>>')
            next_list = self.pass_qq_list.copy()
            self.pass_qq_list = []
            self.start_new_search(next_list)

            l2 = len(self.pass_qq_list)
            print(f'<<<<<< QQ 第 2 轮搜索: 成功 {l-l2} 次 失败 {l2} 次 >>>>>>')
        else:
            print(f'<<<<<< QQ 第 1 轮搜索: {n} 次搜索全部成功 >>>>>>')

    def start_new_search(self, search_list=[]):
        if (len(search_list) == 0):
            search_list = self.qq_list

        l = len(search_list)
        for idx, qq in enumerate(search_list):
            print(f'[{idx+1}/{l}] 开始搜索QQ: {qq}')

            headers = self.build_headers(qq)
            url = self.build_url(qq)

            # get the msg-list
            con = requests.get(url, headers=headers,
                               proxies=utils.get_proxy()).text

            if con == '':
                print(f'{qq} 无法访问QQ空间')
                continue
            if '请先登录空间' in con:
                # cookie is wrong
                print('cookie 有误, 请重新登陆网页空间粘贴 cookie 至 ./input/cookie_file')

            if '没有权限' in con:
                print(f'{qq} 无权访问QQ空间')
                continue

            if '使用人数过多' in con:
                print('使用人数过多，下次再访问该空间')
                self.pass_qq_list.append(qq)
                continue

            if 'gtimg' in con:
                print('gtimg问题，估计是时间问题，下次再来')
                self.pass_qq_list.append(qq)
                continue

            json_str = con[10:-2].replace('null', 'None')
            # print(con)
            json = eval(json_str)
            # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
            msglist = json['msglist']

            if msglist == None:
                print(f'{qq} 无法访问QQ空间')
                continue

            for msg in msglist:
                # 检查时间是否是更新的
                if msg['created_time'] > self.time_stamp[qq]:
                    print(f'发现{qq}发布新内容')
                    for keywords in self.keywords_list:
                        utils.check_all(
                            qq, msg['content'], keywords, self.note_dict)
                else:
                    if self.update_stamp[qq] < msglist[0]['created_time']:
                        self.update_stamp[qq] = msglist[0]['created_time']
                    break
            if self.update_stamp[qq] > self.time_stamp[qq]:
                self.time_stamp[qq] = self.update_stamp[qq]

        time_str = utils.get_time_str()
        open('time_stamp_str.txt', 'w').write(time_str)
        print(f'结束时间: {time_str}')

    def search_history_24h(self, start_str=""):
        end_point = utils.get_time_stamp()
        end_str = utils.time_stamp_2_str(end_point)
        result_path = 'QQ空间记录检查.txt'
        if start_str == "":
            # diff_24h_time_stamp = 60 * 60 * 24
            # start_point = end_point - diff_24h_time_stamp
            # start_str = utils.time_stamp_2_str(start_point)
            start_str = utils.get_last_time_str()

        start_point = utils.str_2_stamp(start_str)

        time_stamp_info = f'\n====== 下方搜索结果起点 {start_str} ======\n\n'
        with open(result_path, 'a', encoding='utf-8') as f:
            f.write(time_stamp_info)

        if self.first:
            self.load_data()
            self.first = False

        l = len(self.qq_list)
        for idx, qq in enumerate(self.qq_list):
            print(f'[{idx+1}/{l}] 开始搜索QQ: {qq} / From: {start_point}')

            headers = self.build_headers(qq)
            url = self.build_url(qq)

            # get the msg-list
            con = requests.get(url, headers=headers,
                               proxies=utils.get_proxy()).text

            if con == '':
                print(f'{qq} 无法访问QQ空间')
                continue
            if '请先登录空间' in con:
                # cookie is wrong
                print('cookie 有误, 请重新登陆网页空间粘贴 cookie 至 ./input/cookie_file')

            json_str = con[10:-2].replace('null', 'None')
            json = eval(json_str)
            msglist = json['msglist']

            if msglist == None:
                print(f'{qq} 无法访问QQ空间')
                continue

            for msg in msglist:
                # 检查时间 24h
                if msg['created_time'] > start_point:
                    print(f'发现{qq} 检索时间内发布内容 检查是否有匹配')
                    for keywords in self.keywords_list:
                        utils.check_all(
                            qq, msg['content'], keywords, self.note_dict, result_path=result_path)
                else:
                    break

        time_stamp_info = f'\n====== 上方搜索结果结束至 {end_str} ======\n\n'
        with open(result_path, 'a', encoding='utf-8') as f:
            f.write(time_stamp_info)
