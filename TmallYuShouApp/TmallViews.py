# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

import pymongo
from django.http import HttpResponseRedirect,HttpResponse
from TmallYuShouApp.TmallApiConnectionModel import GetAllTmallYuShouData
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

        # result = getAllData('上海',itemID)
        result = GetAllTmallYuShouData()
        for data in result:
            content = {}
            content['NCategory_Name'] = data['NCategory_Name']
            content['Re_PreNum'] = data['reserveCount']
            content['Category_Name'] = data['categoryName']
            content['spuId'] = data['spuId']
            content['ReservationStatus'] = data['ReservationStatus']
            content['brand'] = data['brand']
            content['modifyTime'] = data['modifyTime']

            content['productState'] = data['productState']
            content['TreasureID'] = data['TreasureID']
            content['ShopID'] = data['ShopID']
            content['Is_Search'] = data['Is_Search']
            content['EvaluationScores'] = data['EvaluationScores']
            content['NStyleName'] = data['NStyleName']

            content['paymentFinishDate'] = data['paymentFinishDate']
            content['EndTime'] = data['EndTime']
            content['CollectionNum'] = data['CollectionNum']
            content['brandId'] = data['brandId']

            content['ItemName'] = data['ItemName']
            content['presellPrice'] = data['presellPrice']
            content['ShopURL'] = data['ShopURL']

            content['StyleName'] = data['StyleName']
            content['shopName'] = data['shopName']
            content['title'] = data['title']
            content['EffectiveTime'] = data['EffectiveTime']
            content['presellPrice'] = data['presellPrice']
            content['ShopURL'] = data['ShopURL']
            content['popularity'] = data['popularity']
            content['paymentBeginDate'] = data['paymentBeginDate']

            content['mainPic'] = data['mainPic']
            content['JHSmodifyTime'] = data['JHSmodifyTime']
            content['rootCatId'] = data['rootCatId']

            content['StartTime'] = data['StartTime']
            content['NewstPrice'] = data['NewstPrice']
            content['categoryId'] = data['categoryId']
            content['URL_NO'] = data['URL_NO']


            allData.append(content)
        # ErrDesc = {'ErrDesc':result.count()}
        # allData.append(ErrDesc)
        # print allData
        res = {'Data': allData, 'totalCount': result.count()}

        response = HttpResponse(json.dumps(res,cls=DateEncoder) ,content_type="application/json")
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