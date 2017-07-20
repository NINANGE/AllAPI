# -*- coding: utf-8 -*-
import pymongo
import time
import datetime
from bson.objectid import ObjectId

#mongodb连接类
class mongodbConn:
    conn = None
    servers = "mongodb://127.0.0.1:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)
    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn



def getAllData(itemID):

    dbconn = mongodbConn()
    dbconn.connect()
    print '****************************************'
    conn = dbconn.getConn()
    print '******************###3**********************'
    table = conn.TaoBaoScrapyDB.TaoBaoSTB

    print '你大爷的数据------------------------%s'%itemID

    # result = table.find({'city':cityName,'itemID':itemID})
    result = table.find({'itemID': itemID})
    print '你大爷的数据2------------------------%s' % result
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
        # currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
        #
        # delta = datetime.timedelta(days=int(data['dayNumber']))
        #
        # endTime = (datetime.datetime.now() + delta).strftime('%Y-%m-%d')
        #
        # state = ''
        # start_Time = datetime.datetime.strptime(currentTime, '%Y-%m-%d')
        # end_Time = datetime.datetime.strptime(endTime, '%Y-%m-%d')


        currentTime = datetime.datetime.now().strftime('%Y-%m-%d')

        # delta = datetime.timedelta(days=int(data['dayNumber']))

        # endTime = (datetime.datetime.now() + delta).strftime('%Y-%m-%d')

        print 'endTime类型是----------------%s'%data['endTime']

        state = ''
        start_Time = datetime.datetime.strptime(currentTime, '%Y-%m-%d')
        end_Time = datetime.datetime.strptime(data['endTime'], '%Y-%m-%d')


        D_value = end_Time - start_Time

        detailResult = detailT.find({'itemID':str(data['_id'])})

        # print '数据个数为--------------------------%s' % data['_id']

        print '打印数据为--------------------------%s' % detailResult.count()
        # for datas in detailResult:
        #     print '打印数据为--------------------------%s'%datas

        if D_value.days < 0:
            print '456456------------------%s'%data['_id']
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
        priceRange = data['priceUpperLimit']+'-'+data['priceDownLimit']

        conn.TaoBaoScrapyDB.projectKeyWordTB.save({'name':data['name'],'keyword':data['keyword'],
                                                   'pageNumber':data['pageNumber'],'dayNumber':data['dayNumber'],
                                                   'priceUpperLimit':data['priceUpperLimit'],'priceDownLimit':data['priceDownLimit'],
                                                   'priceRange':priceRange,'creator':data['creator'],'beginTime':currentTime,
                                                   'endTime':endTime,'state':state})


#删除指定数据
def removeDatabaseChoiceData(removeData):
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()

    for data in removeData:
        conn.TaoBaoScrapyDB.projectKeyWordTB.remove({'_id':ObjectId(data['id'])})
        conn.TaoBaoScrapyDB.TaoBaoSTB.remove({'itemID':data['id']})

























