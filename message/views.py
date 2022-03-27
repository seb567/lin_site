from django.shortcuts import render
# Create your views here.
from message.Tieba import main,setting,config
from django.http import HttpResponse
from django.core import serializers
from django.db.models import F
import json
import datetime
import threading
from . import models
from django.conf import settings
from django.db.models import Q
class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        main.start()

def start():
    thread1 = myThread("Thread1")
    thread1.start()


def index(request):
    
    return render(request,'message/login.html')
#start()

def getConfig(request):
    return render(request, 'message/param_config.html')
def usermanger(reqeust):
    return render(request, 'message/user_manger.html')

def login(request):
    userId = request.POST.get('u','')
    password = request.POST.get('p','')
    userinfo = models.userInfo.objects. \
                filter(userid=userId, password=password). \
                values('userid', 'usertype').first()
    if not userinfo:
        return HttpResponse("用户名或密码错误，请重新输入")
    else:
        print(userinfo)
        request.session['userid'] = userinfo['userid']
        request.session.set_expiry(60 * 60 * 24)
        usertype = userinfo['usertype']
        if usertype == 0:
            return render(request, 'message/user_main.html')
        elif usertype == 1:
            return render(request, 'message/main.html')
        else :
            return HttpResponse("未知的用户")




def main(request):
    context = {}
    #context = {
    #    "userids" : json.dumps(user_id_list),
    #    "userbackups" : json.dumps(user_backup_list),
    #    "webaddrs" : json.dumps(webaddr_list),
    #    "keywordslist" : json.dumps(keywords_list),
    #    "details" : json.dumps(detail_list)
    #}
    return render(request, 'message/main.html', context)

def user_main(request):
    context = {}
    #context = {
    #    "userids" : json.dumps(user_id_list),
    #    "userbackups" : json.dumps(user_backup_list),
    #    "webaddrs" : json.dumps(webaddr_list),
    #    "keywordslist" : json.dumps(keywords_list),
    #    "details" : json.dumps(detail_list)
    #}
    return render(request, 'message/user_main.html', context)

def search(request):

    keywordsList = request.POST.get('key_word','')
    startDate = datetime.datetime.strptime(request.POST.get('start_date',''), "%Y-%m-%d")
    endDate = datetime.datetime.strptime(request.POST.get('end_date',''), "%Y-%m-%d")
    print(keywordsList)
    print(startDate)
    print(endDate)
    latest_tieba_data = models.tiebainfo.objects.filter(createTime__range=(startDate,endDate),keywordlist__contains=keywordsList)
    #latest_tieba_data = models.tiebainfo.objects.all()
    print(latest_tieba_data)
    id_list = []
    user_backup_list = []
    webaddr_list = []
    keywords_list = []
    detail_list = []
    num = 0;
    for record in latest_tieba_data:
        num = num + 1
        id_list.append(record.id)
        user_backup_list.append(record.userbackup)
        webaddr_list.append(record.webaddr)
        keywords_list.append(record.keywordlist)
        detail_list.append(record.detail)
    
    print(num)
    result = [num, id_list, user_backup_list, webaddr_list, keywords_list, detail_list]
    context = json.dumps(result)
    #context = {
    #    "userids" : json.dumps(user_id_list),
    #    "userbackups" : json.dumps(user_backup_list),
    #    "webaddrs" : json.dumps(webaddr_list),
    #    "keywordslist" : json.dumps(keywords_list),
    #    "details" : json.dumps(detail_list)
    #}
    return HttpResponse(context)
def submit_tieba_config(request):
    sleep_time_sec = request.POST.get('rest_time','')
    restart_time_sec = request.POST.get('bug_restart_time','')
    max_page = request.POST.get('max_page','')
    n_loop = request.POST.get('round','')
    record_time = request.POST.get('record_time','')
    one_page_interval = request.POST.get('one_page_interval','')
    if sleep_time_sec != "" :
        config.set_value('sleep_time_sec',sleep_time_sec)
    if restart_time_sec != "" :
        config.set_value('restart_time_sec',restart_time_sec)
    if max_page != "" :
        config.set_value('max_page',max_page)
    if n_loop != "" :
        config.set_value('n_loop',n_loop)
    if record_time != "" :
        config.set_value('record_time',record_time)
    if one_page_interval != "" :
        config.set_value('one_page_interval',one_page_interval)   

    #config.set_value('restart_time_sec', '10')
    #config.set_value('n_loop', '1')
    #config.set_value('max_page', '3')
    #config.set_value('one_page_interval', '10')
    #config.set_value('record_time', '2022-02-09 23:30:00')
    sleep_time_sec = int(config.get_value('sleep_time_sec'))
        # 出问题之后重启时间(单位是秒)
    restart_time_sec = int(config.get_value('restart_time_sec'))
        # 每次搜索的轮数
    n_loop = int(config.get_value('n_loop'))
        #print(sleep_time_sec)

    start_date = config.get_value('record_time')

    max_page = int(config.get_value('max_page'))
    one_page_interval = int(config.get_value('one_page_interval'))

    print(f'修改后的参数: {sleep_time_sec},{restart_time_sec},{n_loop},{max_page},{one_page_interval},{start_date}')
    #return render(request,resttime)
    return HttpResponse("配置修改成功，等待下轮搜索生效")

def start_tieba1(request):
    latest_tieba_data = [1,2,3,4]
    latest_qq_data = 2
    context = json.dumps(latest_tieba_data)
    return HttpResponse(context)

def start_tieba(request):

    latest_tieba_data = models.tiebainfo.objects.filter(id__gt=setting.last_view_posision)
    #latest_tieba_data = models.tiebainfo.objects.all()
    id_list = []
    user_backup_list = []
    webaddr_list = []
    keywords_list = []
    detail_list = []
    num = 0;
    for record in latest_tieba_data:
        num = num + 1
        id_list.append(record.id)
        user_backup_list.append(record.userbackup)
        webaddr_list.append(record.webaddr)
        keywords_list.append(record.keywordlist)
        detail_list.append(record.detail)
    
    print(num)
    result = [num, id_list, user_backup_list, webaddr_list, keywords_list, detail_list]
    context = json.dumps(result)
    #context = {
    #    "userids" : json.dumps(user_id_list),
    #    "userbackups" : json.dumps(user_backup_list),
    #    "webaddrs" : json.dumps(webaddr_list),
    #    "keywordslist" : json.dumps(keywords_list),
    #    "details" : json.dumps(detail_list)
    #}
    return HttpResponse(context)

def refresh(request):
    last_view_posision = models.lastpos.objects.filter(postype = 0)
    last_pos = 0
    for temp in last_view_posision:
        last_pos = temp.lastposition
    print(last_pos)
    latest_tieba_data = models.tiebainfo.objects.filter(id__gt=last_pos)
    #latest_tieba_data = models.tiebainfo.objects.all()
    id_list = []
    user_backup_list = []
    webaddr_list = []
    keywords_list = []
    detail_list = []
    num = 0;
    for record in latest_tieba_data:
        print(record)
        num = num + 1
        id_list.append(record.id)
        user_backup_list.append(record.userbackup)
        webaddr_list.append(record.webaddr)
        keywords_list.append(record.keywordlist)
        detail_list.append(record.detail)
        #print(record.createTime)
    
    print(num)
    result = [num, id_list, user_backup_list, webaddr_list, keywords_list, detail_list]
    context = json.dumps(result)
    #context = {
    #    "userids" : json.dumps(user_id_list),
    #    "userbackups" : json.dumps(user_backup_list),
    #    "webaddrs" : json.dumps(webaddr_list),
    #    "keywordslist" : json.dumps(keywords_list),
    #    "details" : json.dumps(detail_list)
    #}
    return HttpResponse(context)

def test(request):
    latest_tieba_data = models.tiebainfo.objects.all()
    latest_qq_data = models.qqinfo.objects.all()
    context = {
        'tieba_data': latest_tieba_data
    }
    return render(request, 'message/main.html', context)

def savelastpos(request,pos):
    if request.method == "POST":
        print(pos)
        models.lastpos.objects.filter(postype = 0).update(lastposition=pos)
        res = "ok"
        return HttpResponse(res)