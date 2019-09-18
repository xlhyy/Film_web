# _*_ coding: utf-8 _*_
# @time     : 2018/5/11 10:44
# @Author   : liying
# @FileName : MySQLHelper.py
# @Software : PyCharm

import pymysql

class MySQLHelper():
    def __init__(self,host,port,db,user,password,charset):
        self.host = host
        self.port = port
        self.db = db
        self.user =user
        self.password= password
        self.charset= charset

    def getConn(self):
        self.conn=pymysql.connect(host=self.host,port=self.port,db=self.db,user=self.user,password=self.password,charset=self.charset)
        self.cursor= self.conn.cursor()

    def closeConn(self):
        self.cursor.close()
        self.conn.close()

    def query_one(self):
        result = self.cursor.fetchone()
        return result

    def query_all(self):
        result = self.cursor.fetchall()
        return result

    def executeSQL(self,sql,params):
        self.cursor.execute(sql,params)
        self.conn.commit()

    def select(self, sql, params=()):
        self.executeSQL(sql, params)

    def insert(self, sql, params=()):
        self.executeSQL(sql, params)

    def delete(self, sql, params=()):
        self.executeSQL(sql, params)

    def update(self, sql, params=()):
        self.executeSQL(sql, params)
