# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import time
import sys
import os
import createIDProject.settings


import uuid
from createIdApp.connectionModel import initConnect,getAll_Data,getAll_DetailData,getAll_PinLun,Mssql,getProjectData,getProject_DetailData,insertProAndProDetail,getAllProDetailComment,removeProAndDetailWithComment,downloadCommentExcel
from sqlalchemy.orm import sessionmaker

reload(sys)
sys.setdefaultencoding( "utf-8" )

@csrf_exempt
def createPros(request):

    if request.method == 'POST':

        # ItemName = request.POST.get('ItemName')
        # Validity = request.POST.get('Validity')
        # ID = request.POST.get('ID')
        print '123456789'
        Datas = request.POST.get('Datas')

        datas = json.loads(Datas)

        creator = request.POST.get('Creator')
        ItemName = request.POST.get('ItemName')

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        createTime = datetime.datetime.strptime(nowTime, '%Y-%m-%d %H:%M:%S')

        if insertProAndProDetail(datas,creator,createTime,ItemName):
            backInfoData = {'IsErr': False, 'ErrDesc': u'爬虫启动成功','Data': 'OK','startUpSpider':1}
        else:
            backInfoData = {'IsErr': True, 'ErrDesc': u'爬虫启动失败', 'Data': 'Fail', 'startUpSpider': 0}


        # res = {}
        # sameData = []
        # for data in datas:
        #
        #     if data['name'] not in res.keys():
        #         res[data['name']] = list()
        #         res[data['name']].append(data)
        #     else:
        #         res[data['name']].append(data)
        # for k, v in res.items():
        #     ItemID = uuid.uuid1()
        #     insert_data = []
        #     for d in v:
        #         # print d.values() #一次性打印出v中value值
        #         sameData = []
        #         sameData.append(ItemID)
        #         sameData.append(d['name'])
        #         sameData.append(int(d['days']))
        #         sameData.append(d['IDs'])
        #         sameData.append('')
        #         sameData.append(createTime)
        #         sameData.append('')
        #         sameData.append('')
        #         sameData.append('')
        #         sameData.append(creator)
        #         insert_data.append(sameData)

            # conn = Mssql()
            # conn.exec_one_by_one_query('', insert_data)
            #
            # sql_text = "insert into T_Treasure_EvalCustomItem (ItemID, ItemName, Validity, ItemStatus, CreateTime, PollCount, Creator) VALUES ('%s', '%s', '%d', 1, '%s', 1, '%s')" % (ItemID,v[0]['name'],int(v[0]['days']),createTime,creator)
            # conn.exec_non_query(sql_text)

        #跨域问题需要
        response = HttpResponse(json.dumps(backInfoData, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response



    else:
        allData = []
        name = request.GET.get('Creator')
        # res = getAll_Data(name) #TODO 这是旧数据
        res = getProjectData()

        if res.count() == 0:
            content = {}
            content['id'] = ''
            content['ItemID'] = ''
            content['name'] = ''
            content['Validity'] = ''
            content['CreateTime'] = ''
            content['Trailer_Tips'] = ''
            content['PollCount'] = ''

            content['Creator'] = ''

            allData.append(content)

            res = {'Data': allData, 'Creator': name}
            response = HttpResponse(json.dumps(res, cls=DateEncoder), content_type="application/json")
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        else:
            #TODO 旧数据，弃用
            # for data in res:
            #     datas = list(data)
            #     content = {}
            #     content['id'] = datas[0]
            #     content['ItemID'] = str(datas[1])
            #     content['name'] = datas[2]
            #     content['Validity'] = datas[3]
            #     # content['ItemStatus'] = data.ItemStatus
            #     content['CreateTime'] = datas[5]
            #     content['Trailer_Tips'] = datas[6]
            #     content['PollCount'] = datas[4]
            #     # content['ModifyTime'] = data.ModifyTime
            #     # content['SkuModifyTime'] = data.SkuModifyTime
            #
            #     content['Creator'] = datas[9]
            #
            #     allData.append(content)

            for data in res:
                content = {}
                content['id'] = str(data['_id'])
                content['ItemID'] = str(data['ItemID'])
                content['name'] = data['ItemName']
                content['Validity'] = data['Validity']
                content['CreateTime'] = data['CreateTime']
                content['Trailer_Tips'] = data['Trailer_Tips']
                content['PollCount'] = data['PollCount']

                content['Creator'] = data['Creator']

                allData.append(content)

            res = {'Data': allData, 'Creator': name}
            response = HttpResponse(json.dumps(res, cls=DateEncoder), content_type="application/json")
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response

#删除操作
def lsDelete_data(request):
    if request.method == 'POST':

        ItemID = request.POST.get('ItemID')
        ItemIDS = json.loads(ItemID)
        #TODO: XDF 旧数据，弃用
        # conn = Mssql()
        #
        # sql_text = "delete from T_Treasure_EvalCustomItem where ID='%s'"%ID
        # conn.exec_non_query(sql_text)

        #TODO:XDF 新数据
        removeProAndDetailWithComment(ItemIDS)

        response = HttpResponse(json.dumps({'info':'OK'},cls=DateEncoder),content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    else:
        return HttpResponseRedirect('/')

def lsedit_projects(request):
    if request.method == 'GET':
        ItemID = request.GET.get('ItemID')

        babyID = request.GET.get('babyID')

        # res = getAll_DetailData(ItemID) #TODO 旧数据，弃用

        res = getProject_DetailData(ItemID)

        all_detailData = []
        if res.count() == 0:
            all_detailData.append({'babyID':babyID})
            response = HttpResponse(json.dumps(all_detailData, cls=DateEncoder), content_type="application/json")
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        # for data in res:
        #     datas = list(data)
        #     content = {}
        #     content['babyID'] = babyID
        #     content['id'] = datas[0]
        #     content['ItemID'] = str(datas[1])
        #     content['TreasureID'] = datas[2]
        #     content['TreasureName'] = datas[3]
        #     content['TreasureLink'] = datas[4]
        #     content['ShopName'] = datas[5]
        #     content['Shop_Platform'] = datas[6]
        #     content['Treasure_Status'] = datas[7]
        #     content['Monthly_volume'] = datas[8]
        #     content['IsMerge'] = datas[9]
        #     content['MergeGuid'] = None
        #     content['Category_Name'] = datas[11]
        #     content['GrpName'] = datas[12]
        #     content['spuId'] = datas[13]
        #     content['EvaluationScores'] = str(datas[14])
        #     content['ShopURL'] = datas[15]
        #     content['TreasureFileURL'] = datas[16]
        #     content['Url_No'] = datas[17]
        #     content['CategoryId'] = str(datas[18])
        #     content['brandId'] = datas[19]
        #     content['brand'] = datas[20]
        #     content['rootCatId'] = str(datas[21])
        #     content['StyleName'] = datas[22]
        #     content['CollectionNum'] = datas[23]
        #     content['ItemName'] = datas[24]
        #     content['InsertDate'] = datas[25]
        #     content['ModifyDate'] = datas[26]
        #     content['ShortName'] = datas[27]
        #     content['shopID'] = datas[28]
        #
        #     all_detailData.append(content)

        for data in res:
            print '数据测试中.......%s'%data
            content = {}
            content['babyID'] = babyID
            content['id'] = str(data['_id'])
            content['ItemID'] = str(data['ItemID'])
            content['TreasureID'] = data['TreasureID']
            content['TreasureName'] = str(data['TreasureName'])
            content['TreasureLink'] = data['TreasureLink']
            content['ShopName'] = data['ShopName']
            content['Shop_Platform'] = data['Shop_Platform']
            content['Treasure_Status'] = data['Treasure_Status']
            # content['Monthly_volume'] = data['Monthly_volume']
            content['IsMerge'] = data['IsMerge']
            content['MergeGuid'] = None
            content['Category_Name'] = data['Category_Name']
            content['GrpName'] = data['GrpName']
            content['spuId'] = data['spuId']
            content['EvaluationScores'] = str(data['EvaluationScores'])
            content['ShopURL'] = data['ShopURL']
            content['TreasureFileURL'] = data['TreasureFileURL']
            content['Url_No'] = data['Url_No']
            content['CategoryId'] = str(data['CategoryId'])
            content['brandId'] = data['brandId']
            content['brand'] = data['brand']
            content['rootCatId'] = str(data['rootCatId'])
            content['StyleName'] = data['StyleName']
            content['CollectionNum'] = data['CollectionNum']
            content['ItemName'] = data['ItemName']
            content['InsertDate'] = data['InsertDate']
            content['ModifyDate'] = data['ModifyDate']
            content['ShortName'] = data['ShortName']
            content['shopID'] = data['shopID']

            all_detailData.append(content)


        response = HttpResponse(json.dumps(all_detailData, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    else:
        return HttpResponseRedirect('/')

#全部宝贝评论
def lsAll_PinLun(request):
    if request.method == 'GET':
        treasureID = request.GET.get('TreasureID')
        itemName = request.GET.get('ItemName')
        # res = getAll_PinLun(itemName,treasureID) #TODO 旧数据，弃用
        res = getAllProDetailComment(itemName,treasureID)
        all_PinLun = []
        #TODO:XDF 旧数据，弃用
        # if len(res) == 0:
        #     return all_PinLun
        # for data in res:
        #     datas = list(data)
        #     content = {}
        #
        #     content['ItemName'] = datas[1]
        #     content['RateDate'] = datas[0]
        #     content['TreasureID'] = datas[2]
        #     content['TreasureName'] = datas[3]
        #     content['TreasureLink'] = datas[4]
        #     content['ShopName'] = datas[5]
        #     content['Category_Name'] = datas[6]
        #     content['Level_Name'] = datas[7]
        #     content['AuctionSku'] = datas[8]
        #     content['DisplayUserNick'] = datas[9]
        #     content['RateContent'] = datas[10]
        #     content['IsAppend'] = datas[11]
        #     content['ImgServiceURL'] = datas[12]
        #
        #     all_PinLun.append(content)


        if res.count() == 0:
            return all_PinLun
        for data in res:
            content = {}

            content['ItemName'] = data['ItemName']
            content['RateDate'] = data['RateDate']
            content['TreasureID'] = data['TreasureID']
            content['TreasureName'] = data['TreasureName']
            content['TreasureLink'] = data['TreasureLink']
            content['ShopName'] = data['ShopName']
            content['Category_Name'] = data['Category_Name']
            # content['Level_Name'] = data[7]
            content['AuctionSku'] = data['auctionSku']
            content['DisplayUserNick'] = data['displayUserNick']
            content['RateContent'] = data['rateContent']
            content['IsAppend'] = data['IsAppend']
            content['pics'] = data['ImgServiceURL']
            content['appendContent'] = data['appendContent']

            all_PinLun.append(content)


        response = HttpResponse(json.dumps(all_PinLun,cls=DateEncoder),content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return  response

    else:
        return HttpResponseRedirect('/')

#下载评论内容
def downloadAllCommentAPI(request):
    if request.method == 'GET':
        ItemID = request.GET.get('item_id')
        path = os.path.join(createIDProject.settings.BASE_DIR, 'static', 'downloadAllComment')
        fileName = os.path.join(path, ItemID + '.xlsx')
        yes = downloadCommentExcel(ItemID,fileName)
        if yes:
            url = 'static/downloadAllComment/' + ItemID + '.xlsx'
            content = {'IsErr': False, 'IsSuccess': True, 'url': url}
        else:
            content = {'IsErr': True,'ErrDesc':'下载内容出错', 'IsSuccess': False, 'url': ''}
        response = HttpResponse(json.dumps(content, cls=DateEncoder), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

#启动评论爬虫
def startUpCommentSpider(request):
    if request.method == 'POST':

        allData = []


        # os.popen('sh /Users/zhuoqin/commentSpider/startSpider/startSpiderTask.sh')

        os.popen('sh /home/django/nange/commentSpider/startSpider/startSpiderTask.sh')

        allData.append({'IsErr': False, 'ErrDesc': u'爬虫启动成功','Data': '爬虫启动成功'})

        response = HttpResponse(json.dumps(allData), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        return {'Data': '爬虫启动失败'}

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)




























