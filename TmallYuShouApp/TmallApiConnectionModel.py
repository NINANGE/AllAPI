# -*- coding: utf-8 -*-

from taoBaoMonitorApp.apiDataModel import mongodbConn

def GetAllTmallYuShouData():
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.TmallYuShouDB.TmallYuShouTB.find({})

    return result

def GetTmallYuShouBaseInfoData(TreasureID):
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    if TreasureID:
        result = conn.TmallYuShouDB.find({"TreasureID": {"$in": [TreasureID]}})
    else:
        result = conn.TmallYuShouDB.find({})
    print '返回基本信息'
    return result