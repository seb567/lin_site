# -*- coding: utf-8 -*-
''' 用来检索置顶贴吧中 1楼 内容是否包含指定关键词
    每次搜索过的url记录放置在 /tiebaLog 文件夹内'''

from . import utils
import requests
import os
import time

from bs4 import BeautifulSoup, NavigableString


max_page = 35

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

# ---------- main ---------- #
sep = os.sep


class TiebaSearcher:
    def __init__(self, tieba_name='path'):
        self.base_url = 'https://tieba.baidu.com'
        if tieba_name == 'path':
            self.is_path = True
            self.tieba_path = f'message{sep}Tieba{sep}input{sep}tieba.txt'
        else:
            self.is_path = False
            self.tieba_list = [tieba_name]
        self.keywords_path = f'message{sep}Tieba{sep}input{sep}keywords.txt'
        # 已经找到的内容
        self.note_dict = {}
        self.load_data()

    def load_data(self):
        if self.is_path:
            self.tieba_list = utils.get_tieba_or_qq(self.tieba_path)
        self.keywords_list = utils.get_keywords(self.keywords_path)

        self.record_time = utils.get_time_str()
        self.update_time = self.record_time
        self.log = []

    def addr2bs(self, addr):
        ''' from the net addr to BeautifulSoup'''

        # html string
        # string = requests.get(addr, verify=False, proxies=utils.get_proxy(), headers=headers).content
        string = requests.get(addr, verify=False,
                              proxies=utils.get_proxy(), headers=headers).content
        string.decode('utf-8')

        # beautiful soup
        soup = BeautifulSoup(string, 'html.parser')
        return soup

    def start_new_search(self):
        for tieba_name in self.tieba_list:
            print(f'开始搜索贴吧: {tieba_name}')
            post_num = 0
            for page in range(0, 35*max_page, 35):  # 0 50 100 ... 950 前20页
                # print(f'第{int(page/50+1)}页')
                time.sleep(16)
                tieba_addr = f'{self.base_url}/f?kw={tieba_name}&ie=utf-8&pn={page}'
                homepage_soup = self.addr2bs(tieba_addr)
                #print("network connected!")
                # get the posts list
                posts_list = homepage_soup.find_all(
                    'div', 'col2_right j_threadlist_li_right')

                post_num += len(posts_list)
                #print(f'post_num: {post_num}')

                for post in posts_list:
                    # 得到帖子的时间标签
                    time_tag = post.find(
                        'span', 'pull-right is_show_create_time').contents[0]
                    #print(time_tag)
                    # 如果不是今天的就不看了
                    if ':' not in time_tag:
                        continue

                    # 本文章的发布时间
                    post_time = time.strftime(
                        f'%Y-%m-%d {time_tag}', time.localtime())
                    #print("post_time:",post_time)
                    #print("record_time:",self.record_time)
                    # 如果早于运行时间也不看了
                    if not utils.is_new_post(self.record_time, post_time):
                        continue

                    # 现在开始确定是新帖子了
                    # 先看看是不是已经扫描过的最新的时间(最后用来更新record_time)
                    if utils.is_new_post(self.update_time, post_time):
                        self.update_time = post_time

                    # 检查新贴子的关键字
                    href = post.find('a', 'j_th_tit')['href']
                    if href in self.log:
                        continue
                    else:
                        self.log.append(href)

                    for keywords in self.keywords_list:
                        # search the detail
                        if post.find('div', 'threadlist_abs threadlist_abs_onlyline') != None:
                            title = post.find('a', 'j_th_tit').contents
                            title = utils.del_space(title)
                            content = post.find(
                                'div', 'threadlist_abs threadlist_abs_onlyline').contents
                            content = utils.del_space(content)
                            content = title + '\n' + content

                            content = content.replace(' ', '')
                            # content = content.replace(' ', '').replace('\n', '')

                            utils.check_all(self.base_url + href,
                                            content, keywords, self.note_dict)
            print(f'本次查询帖子共{post_num}个')

        # self.update_new_post_time()

    def update_new_post_time(self):
        if self.update_time > self.record_time:
            print(f'本次启动时间是: {self.record_time}')
            print(f'更新到: {self.update_time}')
            #self.record_time = self.update_time
        else:
            print(f'本次扫描没有发现新内容\n更新时间为{self.update_time} (没发现新内容就不变)')
        print('完成一次对所有贴吧的搜索')
        print(f'新帖标记时间是: {self.record_time}')

    def run(self, n=2):
        for i in range(n):
            print(f'第 {i+1}/{n} 轮搜索')
            self.start_new_search()
        self.update_new_post_time()
