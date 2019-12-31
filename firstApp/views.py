from django.shortcuts import render, reverse, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from . import models
import urllib.parse
import json
from pandas import *

livetemplate = models.livetemplate()

# current sub template list
info = {}

# 解析url中的第二个参数
def reverseParse(fileName, subname):
    try:
        fileName = reverse(subname, args=(fileName,))
        fileName = urllib.parse.unquote(fileName)
        print('fileName: ', fileName)
    except Exception as e:

        print(e)


# note 左边导航的Ajax请求
@csrf_exempt
def home(request, fileName=""):
    global info

    # 修改的内容均放在这里
    reverseParse(fileName, 'home')

    if request.method == "POST":
        if not fileName == "":
            info = livetemplate.read(fileName.replace('/home/', '').replace(r'/', ''))
            print("info ", info)

        allfile = livetemplate.readAllFile()
        print("allfile", allfile)

        return JsonResponse({"files": allfile, 'infos': info})




# note view函数-初次get请求

@csrf_exempt
def newindex(request, fileName=""):
    global info

    reverseParse(fileName, 'newindex')

    if request.method == "GET":
        if not fileName == "":
            info = livetemplate.read(fileName.replace('/newindex/', '').replace(r'/', ''))
            print("info ", info)


        allfile = livetemplate.readAllFile()
        print("allfile", allfile)
        # info代表的是单个文件的所有的信息 ： info  {1: {'envi': '', 'value': "describe('$NAME$', func
        return render(request, 'home.html', context={"files": allfile, 'infos': info})


# 保存返回的信息
# note Django保存返回的ajax info信息
@csrf_exempt
def save(request):
    if request.method=='POST':

        originalInfos=json.loads(request.body.decode('utf-8'))
        updatedinfos=originalInfos.get('updatedinfos')
        title=originalInfos.get('title')

        print("updatedInfos_1: ",updatedinfos)
        print("title: ",title)
        livetemplate.update(updatedinfos,title)
        print("updated success")

        return HttpResponse("Yes")

