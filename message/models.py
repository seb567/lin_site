from django.db import models

# Create your models here.
class tiebainfo(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=30)
    userbackup = models.CharField(max_length=1000)
    webaddr = models.CharField(max_length=500)
    keywordlist = models.CharField(max_length=1000)
    detail = models.CharField(max_length=2000)
    createTime = models.DateTimeField(auto_now=True)


class qqinfo(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=30)
    userbackup = models.CharField(max_length=1000)
    qqnumber = models.CharField(max_length=500)
    keywordlist = models.CharField(max_length=1000)
    detail = models.CharField(max_length=2000)
    createTime = models.DateTimeField(auto_now=True)


class tiebaads(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(primary_key=True)
    webaddr = models.CharField(max_length=500)
    keywordlist = models.CharField(max_length=1000)
    detail = models.CharField(max_length=2000)
    createTime = models.DateTimeField(auto_now=True)


class lastpos(models.Model):
    id = models.AutoField(primary_key=True)
    postype = models.IntegerField(default=999)
    lastposition = models.IntegerField(default=0)
    createTime = models.DateTimeField(auto_now=True)
    userid = models.CharField(max_length=30)

class userInfo(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    usertype = models.IntegerField(default=0)
