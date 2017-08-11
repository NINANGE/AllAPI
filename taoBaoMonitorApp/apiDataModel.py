# -*- coding: utf-8 -*-
import pymongo
import time
import datetime
from bson.objectid import ObjectId
import pandas as pd
import numpy
import os

#mongodb连接类
class mongodbConn:
    conn = None
    # servers = "mongodb://127.0.0.1:27017"
    servers = "mongodb://192.168.3.172:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)
    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn



def getAllData(itemID,state,pageSize,pageNumber,searchTEXTS):

    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    table = conn.TaoBaoScrapyDB.TaoBaoSTB

    # print '你大爷的数据------------------------%s'%market

    # result = table.find({'city':cityName,'itemID':itemID})
    # if market == '1':
    #     result = table.find({"itemID" : itemID,"detailURL":{'$regex':"taobao"}})
    #
    # else:



    table.update({'itemID':itemID }, {'$set': {'state': state}})
    tables = conn.TaoBaoScrapyDB.TaoBaoSTB
    # result = tables.find({'itemID': itemID}).skip(0).limit(pageCount).sort([{"yearAndMonth":-1}])

    if pageNumber == 1:
        pageNumbers = pageNumber
    else:
        pageNumbers = (pageNumber-1)*pageSize
    print '结果----中啦-----%s---%s---%s'%(pageNumbers,pageSize,searchTEXTS)

    # if len(searchText)==0:

    if len(searchTEXTS)== 0:

        result = tables.find({'itemID': itemID}).skip(pageNumbers).limit(pageSize).sort("yearAndMonth",pymongo.ASCENDING) #分页查询，sort里面只能写一个字段，默认为升序,升序：ASCENDING 降序：DESCENDING
    # result = tables.find({'itemID': itemID})
    else:
        result = tables.find({'itemID': itemID,"ID": {'$regex': searchTEXTS, '$options':'i'}})#.skip(pageNumbers).limit(pageSize).sort("yearAndMonth",pymongo.ASCENDING)

    # result = tables.find({'itemID': itemID}).skip(0).limit(500)

    return result

def getAllProjectData():
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    table = conn.TaoBaoScrapyDB.projectKeyWordTB
    conn = dbconn.getConn()
    detailT = conn.TaoBaoScrapyDB.TaoBaoSTB

    result = table.find({})
    updateProjectState(table,detailT,result) #更新状态

    result = table.find({}) #由于result是迭代器，在上面迭代器已经用完了，所以在这下面必须重新赋值数据源
    return result


def updateProjectState(table,detailT,result):

    for data in result:

        currentTime = datetime.datetime.now().strftime('%Y-%m-%d')

        # delta = datetime.timedelta(days=int(data['dayNumber']))

        # endTime = (datetime.datetime.now() + delta).strftime('%Y-%m-%d')

        # print 'endTime类型是----------------%s'%data['endTime']

        state = ''
        start_Time = datetime.datetime.strptime(currentTime, '%Y-%m-%d')
        end_Time = datetime.datetime.strptime(data['endTime'], '%Y-%m-%d')


        D_value = end_Time - start_Time

        detailResult = detailT.find({'itemID':str(data['_id'])})

        # print '数据个数为--------------------------%s' % data['_id']

        # print '打印数据为--------------------------%s' % detailResult.count()
        # for datas in detailResult:
        #     print '打印数据为--------------------------%s'%datas

        if D_value.days <= 0:
            table.update({'_id': ObjectId(data['_id'])}, {'$set': {'state': '已完成'}})

        elif detailResult.count()==0 and D_value.days>=0:
            table.update({'_id':ObjectId(data['_id'])},{'$set': {'state':'待开启'}})

        else:
            table.update({'_id': ObjectId(data['_id'])},  {'$set':{'state':'进行中'}})



#创建项目插入数据
def insertProjectData(Datas):

    dbconn = mongodbConn()
    dbconn.connect()

    conn = dbconn.getConn()

    for data in Datas:
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=int(data['dayNumber']))
        endTime = (datetime.datetime.now() + delta).strftime('%Y-%m-%d')


        state = ''
        start_Time = datetime.datetime.strptime(currentTime,'%Y-%m-%d')
        end_Time = datetime.datetime.strptime(endTime,'%Y-%m-%d')

        D_value = end_Time-start_Time

        if D_value.days >= 0:
            state = '进行中'
        else:
            state = '已完成'
        #价格区间
        priceRange = ''
        if len(data['priceUpperLimit'])>0 and len(data['priceDownLimit'])==0:
            priceRange = data['priceUpperLimit']+'-'+'无'
        elif len(data['priceUpperLimit'])==0 and len(data['priceDownLimit'])>0:
            priceRange = '0' + '-' + data['priceDownLimit']
        else:
            priceRange = data['priceUpperLimit'] + '-' + data['priceDownLimit']
        conn.TaoBaoScrapyDB.projectKeyWordTB.save({'name':data['name'],'keyword':data['keyword'],
                                                   'pageNumber':data['pageNumber'],'dayNumber':data['dayNumber'],
                                                   'priceUpperLimit':data['priceUpperLimit'],'priceDownLimit':data['priceDownLimit'],
                                                   'priceRange':priceRange,'creator':data['creator'],'beginTime':currentTime,
                                                   'endTime':endTime,'start_Time':start_Time,'end_Time':end_Time,'state':state,'market':data['market'],
                                                   'customized':data['customized']
                                                   })


#删除指定数据
def removeDatabaseChoiceData(removeData):
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()

    for data in removeData:
        conn.TaoBaoScrapyDB.projectKeyWordTB.remove({'_id':ObjectId(data['id'])})
        conn.TaoBaoScrapyDB.TaoBaoSTB.remove({'itemID':data['id']})
        conn.TaoBaoScrapyDB.ALLStoreTB.remove({'itemID':data['id']})


#生成excel并导出下载
def downloadExcel(itemID, path):
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()

    # if market == '1':
    #     curr = conn.TaoBaoScrapyDB.TaoBaoSTB.find({'itemID': itemID,"detailURL":{'$regex':"taobao"}},{'_id':0,'province':1,'city':1,'name':1,'payPerson':1,'price':1,
    #                                                                   'mainPic':1,'detailURL':1,'yearAndMonth':1,'shopName':1,'category':1})
    # else:
    curr = conn.TaoBaoScrapyDB.TaoBaoSTB.find({'itemID': itemID},{'_id': 0, 'province': 1, 'city': 1, 'name': 1, 'payPerson': 1,'price': 1,
                                                   'mainPic': 1, 'detailURL': 1, 'yearAndMonth': 1, 'shopName': 1,'category': 1,'market':1,'offTime':1})
    df = pd.DataFrame(list(curr))



    df.rename(columns={'province':'省份','name':'宝贝名称','payPerson':
                        '付款人数','price':'价格','mainPic':'宝贝图片链接','yearAndMonth':'收录时间',
                       'shopName': '店铺名','city':'城市','detailURL':'宝贝链接','category':'类目','market':'平台',
                       'offTime':'下架时间'},inplace=True)

    df.sort_index()

    # df.sort_values(by='city',axis=0,ascending=True,inplace=False,kind='quicksort',na_position='last')
    # df.sort()
    # df.columns = ['城市','省份','宝贝名称','付款人数','价格','宝贝图片链接','收录时间','店铺名','宝贝链接']


    try:
        write = pd.ExcelWriter(path)
        df.to_excel(write,u'林氏木业')
        write.save()
        return True
    except Exception as e:
        print 'miss-------%s'%e
        return  False

#得到宝贝店铺地区
def getStorePosition(itemID):
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()

    # storeTB = conn.TaoBaoScrapyDB.ALLStoreTB
    # result = storeTB.find({'itemID':itemID})
    # result = storeTB.find({})
    return conn.TaoBaoScrapyDB.ALLStoreTB.find({'itemID':itemID})




























