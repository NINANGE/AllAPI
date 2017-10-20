# -*- coding: utf-8 -*-

from taoBaoMonitorApp.apiDataModel import mongodbConn

def GetAllTmallYuShouData():
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.TmallYuShouDB.TmallYuShouTB.find({})

    return result

def GetTmallYuShouBaseInfoData():
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.conn.TmallYuShouDB.TmallYuShouTB.find({})
    print '返回基本信息数据'
    return result