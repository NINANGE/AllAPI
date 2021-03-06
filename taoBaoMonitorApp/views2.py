# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

import pymongo
from django.http import HttpResponseRedirect,HttpResponse
from taoBaoMonitorApp.apiDataModel import getAllData,insertProjectData,getAllProjectData,removeDatabaseChoiceData,downloadExcel,downloadShopExcel,getStorePosition
import json
import datetime
import time
import sys
import os
import subprocess
import createIDProject.settings


reload(sys)
sys.setdefaultencoding("utf-8")


def startUpSpider(request):
    if request.method == 'POST':
        os.popen('sh /home/django/nange/taoBaoSpider/taoBaoScrapy/spiders/startUpTimeTask.sh')
        # os.popen('sh /Users/zhuoqin/taoBaoScrapy/taoBaoScrapy/spiders/startUpTimeTask.sh')
        allData = []

        allData.append({'Data': '爬虫启动成功'})
        response = HttpResponse(json.dumps(allData), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        return {'Data': '爬虫启动失败'}



# @csrf_exempt
def getAllDatas(request):
    if request.method == 'POST':
        print '******************888888888888**********************'
    else:

        itemID = request.GET.get('itemID')
        market = request.GET.get('market')
        state = request.GET.get('state')
        # pageCount = request.GET.get('page')

        pageSize = request.GET.get('pageSize')
        pageNumber = request.GET.get('pageNumber')
        # searchText = request.GET.get('searchText')
        searchTEXTS = request.GET.get('searchTEXT')

        # print '测试数据-----%s-----%s-----%s'%(pageSize,pageNumber,searchTEXTS)
        allData = []

        # result = getAllData('上海',itemID)
        result = getAllData(itemID,state,int(pageSize),int(pageNumber),searchTEXTS)
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
            content['category'] = data['category']
            content['categoryId'] = data['categoryId']
            content['market'] = data['market']
            content['customized'] = data['customized']
            content['offTime'] = data['offTime']
            content['totalCount'] = result.count()

            allData.append(content)
        # ErrDesc = {'ErrDesc':result.count()}
        # allData.append(ErrDesc)

        res = {'Data': allData, 'totalCount': result.count()}

        response = HttpResponse(json.dumps(res) ,content_type="application/json")
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
        for data in result:
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
            content['market'] = data['market']
            content['customized'] = data['customized']

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

        datas = request.POST.get('Datas')
        datas = json.loads(datas)
        insertProjectData(datas)

        # print '数据是-----%s' % len(datas)

        # for ceShiData in datas:
        #     print '结果数据是-----%s' %ceShiData
        #     print '结果数据是类型-----%s' % ceShiData['priceDownLimit']

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


        # for data in removeData:
        #     print '删除数据id------------%s' % data['id']


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
        # print '删除数据id------------%s' % removeData
        # 跨域问题需要
        response = HttpResponse(json.dumps({'info': 'OK'}, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

#生成excel并导出下载excel
def makeDownloadExcel(request):

    if request.method == 'POST':
        itemID = request.POST.get('babyItemID')
        name = str(request.POST.get('name'))
        market = request.POST.get('market')

        path = os.path.join(createIDProject.settings.BASE_DIR, 'static', 'downloadExcel')
        fileName = os.path.join(path,name+'.xlsx')

        yes = downloadExcel(itemID,fileName)
        print 'yes或no----------------%s' % yes
        if yes:
            url = 'static/downloadExcel/'+name+'.xlsx'
            content = {'IsErr':False,'IsSuccess':True,'url':url}
        else:
            content = {'IsErr':True,'IsSuccess':False,'url':''}

        response = HttpResponse(json.dumps(content, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        itemID = request.GET.get('babyItemID')
        name = str(request.GET.get('name'))
        path = os.path.join(createIDProject.settings.BASE_DIR, 'static', 'ShopDownloadExcel')
        fileName = os.path.join(path,name+'店铺信息.xlsx')
        yes = downloadShopExcel(itemID,fileName)
        if yes:
            url = 'static/ShopDownloadExcel/' + name + '店铺信息.xlsx'
            content = {'IsErr':False,'IsSuccess':True,'url':url}
        else:
            content = {'IsErr':False,'IsSuccess':True,'url':''}
        response = HttpResponse(json.dumps(content, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

#店铺地区
def storeAllPosition(request):
    if request.method == 'GET':
        itemID = request.GET.get('itemID')
        result = getStorePosition(itemID)
        allData = []

        for data in result:
            conntent = {}
            conntent['id'] = str(data['_id'])
            conntent['url'] = data['url']
            conntent['cityCode'] = data['cityCode']
            conntent['tel'] = data['tel']
            conntent['district'] = data['district']
            conntent['address'] = data['address']
            conntent['latitude'] = data['latitude']
            conntent['storeName'] = data['storeName']
            conntent['ID'] = data['ID']
            conntent['longitude'] = data['longitude']
            allData.append(conntent)
        response = HttpResponse(json.dumps(allData), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        pass





class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
































