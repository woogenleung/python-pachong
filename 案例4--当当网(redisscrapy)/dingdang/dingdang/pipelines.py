# -*- coding: utf-8 -*-


import pymysql
from twisted.enterprise import adbapi


class DingdangPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            # 游标设置
            cursorclass=pymysql.cursors.DictCursor,
            # 设置编码是否使用Unicode
            use_unicode=True
        )
        # 通过Twisted框架提供的容器链接数据库,MySQLdb是数据库模名
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted异步将item数据插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)


    def do_insert(self, cursor, item):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        print(data)
        insert_sql = "insert into dangdang (%s) values (%s)" % (keys, values)

        cursor.execute(insert_sql, tuple(data.values()))

    def handle_error(self, failure, item, spider):
        print(failure)
