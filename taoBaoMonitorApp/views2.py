# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

import pymongo
from django.http import HttpResponseRedirect,HttpResponse
from taoBaoMonitorApp.apiDataModel import getAllData,insertProjectData,getAllProjectData,removeDatabaseChoiceData
import json
import datetime
import time
import sys
import os
import subprocess


reload(sys)
sys.setdefaultencoding("utf-8")


def startUpSpider(request):
    if request.method == 'POST':
        print '启动爬虫失败'
        return {'Data': '爬虫启动失败'}
    else:
        print '启动爬虫成功'
        allData = []

        allData.append({'Data': '爬虫启动成功'})
        response = HttpResponse(json.dumps(allData), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response



# @csrf_exempt
def getAllDatas(request):
    if request.method == 'POST':
        print '******************888888888888**********************'
    else:

        itemID = request.GET.get('itemID')
        print '你瞧瞧这数据******************888888888888**********************%s'%(request.GET.get('itemID'))
        allData = []

        # result = getAllData('上海',itemID)
        result = getAllData(itemID)
        for data in result:

            content = {}
            content['province'] = data['province']
            content['city'] = data['city']
            content['name'] = data['name']
            content['payPerson'] = data['payPerson']
            content['price'] = data['price']
            content['mainPic'] = data['mainPic']
            content['month'] = data['month']
            content['pageNumber'] = data['pageNumber']
            content['year'] = data['year']
            content['yearAndMonth'] = data['yearAndMonth']
            content['ID'] = data['ID']
            content['shopName'] = data['shopName']
            content['itemID'] = data['itemID']
            content['detailURL'] = data['detailURL']


            allData.append(content)
        response = HttpResponse(json.dumps(allData) ,content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def getAllBuildData(request):
    if request.method == 'POST':
        print ''
    else:
        allData = []

        result = getAllProjectData()
        print '_id类型---------999999999999======%s'%result
        for data in result:

            print '_id类型---------%s---------%s'%(type(data['_id']),data['_id'])


            content = {}
            content['name'] = data['name']
            content['keyword'] = data['keyword']
            content['priceUpperLimit'] = data['priceUpperLimit']
            content['priceDownLimit'] = data['priceDownLimit']
            content['priceRange'] = data['priceRange']
            content['dayNumber'] = data['dayNumber']
            content['pageNumber'] = data['pageNumber']
            content['creator'] = data['creator']
            content['beginTime'] = data['beginTime']
            content['endTime'] = data['endTime']
            content['state'] = data['state']
            content['id'] = str(data['_id'])

            allData.append(content)
        response = HttpResponse(json.dumps(allData), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


#插入数据
def inserProject(request):
    if request.method == 'POST':
        print '插入成功'

        datas = request.POST.get('Datas')
        datas = json.loads(datas)
        insertProjectData(datas)

        print '数据是-----%s' % len(datas)

        for ceShiData in datas:
            print '结果数据是-----%s' %ceShiData
            print '结果数据是类型-----%s' % ceShiData['priceDownLimit']

        # 跨域问题需要
        response = HttpResponse(json.dumps({'info': 'OK'}, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        datas = request.POST.get('Datas')
        datas = json.loads(datas)
        print '数据是*********-----%s' % datas

        # 跨域问题需要
        response = HttpResponse(json.dumps({'info': 'OK'}, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

#删除数据
def removeDataAPI(request):
    if request.method == 'POST':

        removeData = request.POST.get('ID')

        removeData = json.loads(removeData)

        removeDatabaseChoiceData(removeData)


        for data in removeData:
            print '删除数据id------------%s' % data['id']


        # 跨域问题需要
        response = HttpResponse(json.dumps({'info': 'OK'}, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    else:
        removeData = request.POST.get('ID')

        # removeData = json
        print '删除数据id------------%s' % removeData
        # 跨域问题需要
        response = HttpResponse(json.dumps({'info': 'OK'}, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response



class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
































