# -*- coding: utf-8 -*-

from taoBaoMonitorApp.apiDataModel import mongodbConn

def GetAllTmallYuShouData():
    dbconn = mongodbConn()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.TmallYuShouDB.TmallYuShouTB.find({})

    return result