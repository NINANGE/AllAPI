# -*- coding: utf-8 -*-

from taoBaoMonitorApp.apiDataModel import mongodbConn

def GetAllTmallYuShouData():
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.TmallYuShouDB.TmallYuShouBaseInfoTB.find({})

    return result

def GetTmallYuShouBaseInfoData(TreasureID):
    print 'TreasureID----%s'%TreasureID
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()

    if TreasureID == None or len(str(TreasureID))==0:
        print '返回所有数据'
        result = conn.TmallYuShouDB.TmallYuShouBaseInfoTB.find({})
    else:
        print '进来了'
        result = conn.TmallYuShouDB.TmallYuShouBaseInfoTB.find({"TreasureID": {"$in": [TreasureID]}})

    print '返回基本信息'
    return result