# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,bindparam,and_,or_
import pymssql
import uuid
from  datetime import datetime as dt
import pymongo
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

#TODO：XDF 这是连接sql server数据库数据，现在迁移到mongodb中，所以，这些被舍弃掉
def initConnect(tableName):
    #create_engine 方法进行数据库连接，返回一个 db 对象。
    #echo = True 是为了方便 控制台 logging 输出一些sql信息，默认是False
    engine = create_engine('mssql+pymssql://bs-prt:123123@192.168.1.253:1433/Collectiondb?charset=utf8',poolclass=NullPool,echo=False)
    connection = engine.connect()
    metaData = sqlalchemy.schema.MetaData(bind=engine,reflect=True)
    table_schema = sqlalchemy.Table(tableName,metaData,autoload=True)
    return engine,connection,table_schema


def getAll_Data1(creator):

    engine,connection,table_schema = initConnect("T_Treasure_EvalCustomItem")
    #创建session:
    Session = sessionmaker(bind=engine)
    session = Session()
    #获取任务
    # res = session.query(table_schema).all()

    res = session.query(table_schema).filter(table_schema.columns.Creator == creator).all()

    # res = session.execute("SELECT * FROM table_schema WHERE Creator=%s"%creator)

    # #断开连接
    session.close()
    connection.close()
    return res

#增
def add_Datas(ItemNames,Validitys,IDs):
    engine,connection,table_schema = initConnect('T_Treasure_EvalCustomItem')
    #创建session
    Session = sessionmaker(bind=engine)
    session = Session()

    tasks = table_schema(ItemName=ItemNames,Validity=Validitys,ID=IDs)
    #新增任务
    session.add(tasks)
    session.commit()

    session.close()
    connection.close()
    return tasks



def getAll_DetailDatas(ItemIDS):

    engine,connection,table_schema = initConnect("T_Treasure_EvalCustomItem_Detail")
    #创建session
    Session = sessionmaker(bind=engine)
    session = Session()
    #获取任务详情

    res = session.query(table_schema).filter(table_schema.columns.ItemID==ItemIDS).all()


    #断开连接
    session.close()
    connection.close()
    return res


def getAll_PinLuns(ItemNames,TreasureIDs):
    engine,connection,table_schema = initConnect("V_Treasure_Evaluation")
    #创建session
    Session = sessionmaker(bind=engine)
    session = Session()
    #获取任务详情
    res = session.query(table_schema).filter(and_(table_schema.columns.ItemName==ItemNames,table_schema.columns.TreasureID==TreasureIDs)).all()
    #断开连接
    session.close()
    connection.close()
    return res


#sql
class Mssql:
    def __init__(self):
        self.host = '192.168.1.253:1433'
        self.user = 'bs-prt'
        self.pwd = '123123'
        self.db = 'Collectiondb'

    def __get_connect(self):
        if not self.db:
            raise (NameError, "do not have db information")
        self.conn = pymssql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            database=self.db,
            charset="utf8"
        )
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "Have some Error")
        else:
            return cur

    def exec_query(self, sql):
        """
         the query will return the list, example;
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__get_connect()
        cur.execute(sql)
        res_list = cur.fetchall()

        # the db object must be closed
        self.conn.close()
        return res_list

    def exec_non_query(self, sql):
        """
        execute the query without return list, example：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__get_connect()

        cur.execute(sql)

        self.conn.commit()
        self.conn.close()

    def exec_many_query(self, sql, param):
        """
        execute the query without return list, example：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__get_connect()
        try:
            cur.executemany(sql, param)

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

        self.conn.close()

    def exec_one_by_one_query(self, sql, param):
        """
        execute the query without return list, example：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__get_connect()
        insert_date = dt.today().strftime('%Y-%m-%d %H:%M:%S')

        for i in param:
            sql_text = "insert into T_Treasure_EvalCustomItem_Detail values ('%s','%s','%s','%s','%s','%d','%d','%d','%s','%s','%s','%s','%s','%d','%s','%s','%s','%d','%s','%s','%d','%s','%d','%s','%s','%s','%s','%s')" %\
                       (i[0],i[3],' ',' ',' ',1,1,1,' ',uuid.uuid1(),' ',' ',' ',1,' ',' ',' ',1.0,' ',' ',1.0,' ',1,i[1],insert_date,' ',' ',' ')
            try:
                cur.execute(sql_text)
                self.conn.commit()
            except Exception as e:
                print e
                self.conn.rollback()

        self.conn.close()



def getAll_Data(creator=None):

    conn = Mssql()

    sql_text = "select * from T_Treasure_EvalCustomItem"


    res = conn.exec_query(sql_text)
    if len(res) > 0:
        return res
    else:
        return False


def getAll_DetailData(ItemIDS):

    conn = Mssql()

    sql_text = "select * from T_Treasure_EvalCustomItem_Detail where ItemID='%s'"%(ItemIDS)

    res = conn.exec_query(sql_text)

    return res

def getAll_PinLun(ItemNames,TreasureIDs):

    conn = Mssql()

    sql_text = "select * from V_Treasure_Evaluation where ItemName='%s' and TreasureID='%s' " % (ItemNames.encode('utf-8'),TreasureIDs.encode('utf-8'))

    res = conn.exec_query(sql_text)

    return res


#TODO :XDF 连接mongodb，新数据
#mongodb连接类
class mongodbConns:
    conn = None
    # servers = "mongodb://127.0.0.1:27017"
    servers = "mongodb://192.168.3.172:27017"

    def connect(self):
        self.conn = pymongo.MongoClient(self.servers)
    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn

#获取产品项目所有数据
def getProjectData():
    dbconn = mongodbConns()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.CommentDB.commProjectTB.find({})

    return result

def getProject_DetailData(ItemID):
    dbconn = mongodbConns()
    dbconn.connect()
    conn = dbconn.getConn()
    result = conn.CommentDB.commentCustomItemDetailTB.find({'ItemID':ItemID})

    return result


def insertProAndProDetail(proData,creator,createTime,ItemName):
    dbconn = mongodbConns()
    dbconn.connect()
    conn = dbconn.getConn()

    print len(proData),creator,createTime,ItemName
    ItemID = str(uuid.uuid1())
    conn.CommentDB.commProjectTB.save({'ItemID':ItemID,'Trailer_Tips':'待开启','ModifyTime':createTime,'ItemStatus':0,'Creator':creator,
                                        'ItemName':ItemName,'CreateTime':createTime,'Validity':1,'PollCount':0})

    for i in range(0,len(proData)):
        print '你爸爸的%s'%i
        conn.CommentDB.commentCustomItemDetailTB.save({'MergeGuid':'','GrpName':'','ShopName':'','spuId':'','Shop_Platform':'','CollectionNum':'',
                                                   'EvaluationScores':'','ItemName':ItemName,'ItemID':ItemID,'StyleName':'','ModifyDate':createTime,
                                                   'ShortName':'','TreasureLink':'','IsMerge':'','brand':'','shopID':'','TreasureID':proData[i]['IDs'],'brandId':'',
                                                   'TreasureFileURL':'','Treasure_Status':0,'CategoryId':'','Category_Name':'','ShopURL':'',
                                                   'Monthly_Volume':'','InsertDate':createTime,'rootCatId':'','Url_No':'','TreasureName':''
                                                   })

    # projectData = conn.CommentDB.commProjectTB.find({'ItemName': { '$ne': ItemName},'Trailer_Tips': { '$ne': '已过期'}})
    projectData = conn.CommentDB.commProjectTB.find({'Trailer_Tips': '正在爬取中...'})

    if projectData.count()>0:#表明还有其它正在运行的爬虫，所以新建爬虫暂时不启动
        return False
    return True


#全部评评论内容
def getAllProDetailComment(ItemName,TreasureID):
    dbconn = mongodbConns()
    dbconn.connect()
    conn = dbconn.getConn()
    return conn.CommentDB.commentContentTB.find({'TreasureID':TreasureID,'ItemName':ItemName})

#删除项目及对应的产品数据和评论内容数据
def removeProAndDetailWithComment(ItemIDS):
    dbconn = mongodbConns()
    dbconn.connect()
    conn = dbconn.getConn()

    for i in range(0,len(ItemIDS)):
        print '删除数据---%s----%s'%(ItemIDS[i],type(ItemIDS[i]))
        conn.CommentDB.commProjectTB.remove({'ItemID':ItemIDS[i]})
        conn.CommentDB.commentCustomItemDetailTB.remove({'ItemID':ItemIDS[i]})
        conn.CommentDB.commentContentTB.remove({'ItemID':ItemIDS[i]})

#下载一个项目下的所有产品评论内容
#生成店铺信息excel并导出
def downloadCommentExcel(itemID,path):
    dbconn = mongodbConns()
    dbconn.connect()
    conn = dbconn.getConn()
    curr = conn.CommentDB.commentContentTB.find({'ItemID': itemID},{'_id':0,'ItemName':1,'TreasureID':1,'TreasureName':1,'TreasureLink':1,'ShopName':1,
                                                                    'EvaluationScores':1,'Category_Name':1,'StyleName':1,'auctionSku':1,'rateContent':1,'ImgServiceURL':1
                                                                    })
    df = pd.DataFrame(list(curr))

    df.rename(columns={'ItemName': '项目名称', 'TreasureID': '宝贝ID', 'TreasureName':'宝贝名称', 'TreasureLink':'宝贝链接', 'ShopName':'商店名称',
                       'EvaluationScores':'宝贝评分','Category_Name':'类目','StyleName':'风格','auctionSku':'规格描述','rateContent':'买家评论',
                       'ImgServiceURL':'评论图片'
                       }, inplace=True)
    df.sort_index()
    print '正在下载中。。。。'
    try:
        write = pd.ExcelWriter(path)
        df.to_excel(write,u'评论内容')
        write.save()
        return True
    except Exception as e:
        print 'miss-------%s'%e
        return  False



























