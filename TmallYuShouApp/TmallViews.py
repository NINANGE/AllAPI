# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

import pymongo
from django.http import HttpResponseRedirect,HttpResponse
from TmallYuShouApp.TmallApiConnectionModel import GetAllTmallYuShouData,GetTmallYuShouBaseInfoData
import json
import datetime
import sys
import os
import subprocess


reload(sys)
sys.setdefaultencoding("utf-8")

# @csrf_exempt
def GetTmallYuShouDataAPI(request):
    if request.method == 'POST':
        print '******************888888888888**********************'
    else:
        allData = []

        result = GetAllTmallYuShouData()
        for data in result:
            content = {}
            content['TreasureID'] = data['TreasureID']
            content['StartTime'] = data['StartTime']
            content['EndTime'] = data['EndTime']
            content['TailStartTime'] = data['paymentBeginDate']
            content['TailEndTime'] = data['paymentFinishDate']
            content['Re_PreNum'] = data['reserveCount']
            content['T_Price'] = data['presellPrice']
            content['Collection_Num'] = data['CollectionNum']
            content['URL_NO'] = data['URL_NO']
            content['CreateTime'] = data['spiderTime']
            content['ModifyTime'] = data['modifyTime']

            allData.append(content)
        res = {'Data': allData, 'totalCount': result.count()}

        response = HttpResponse(json.dumps(res,cls=DateEncoder) ,content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

def GetTmallYuShouBaseInfoDataAPI(request):
    if request.method == 'GET':
        allData = []

        result = GetAllTmallYuShouData()
        for data in result:
            content = {}
            content['TreasureID'] = data['TreasureID']
            content['TreasureName'] = data['title']
            content['TreasureLink'] = data['detailURL']
            content['ShopID'] = data['ShopID']
            content['ShopName'] = data['shopName']
            content['Is_Search'] = data['Is_Search']
            content['InsertDate'] = data['spiderTime']
            content['ModifyDate'] = data['modifyTime']
            content['Category_Name'] = data['categoryName']
            content['spuId'] = data['spuId']
            content['EvaluationScores'] = data['EvaluationScores']
            content['ShopURL'] = data['ShopURL']
            content['TreasureHref'] = data['mainPic']
            content['TreasureFileURL'] = data['mainPic']
            content['Url_No'] = data['URL_NO']
            content['CategoryId'] = data['categoryId']
            content['brandId'] = data['brandId']
            content['brand'] = data['brand']
            content['rootCatId'] = data['rootCatId']
            content['StyleName'] = data['StyleName']
            content['CollectionNum'] = data['popularity']
            content['JHSmodifyTime'] = data['JHSmodifyTime']
            content['ItemName'] = data['ItemName']

            allData.append(content)
        res = {'Data': allData, 'totalCount': result.count()}

        response = HttpResponse(json.dumps(res, cls=DateEncoder), content_type="application/json")
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































