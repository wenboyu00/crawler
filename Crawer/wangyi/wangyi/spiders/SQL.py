import pymysql

# 初始化数据库信息
db = pymysql.connect(host='118.89.159.211',
                     user='hive',
                     password='hive',
                     port=3306,
                     database='spiderman',
                     charset='utf8')

# 初始化光标
cursor = db.cursor()


class Sql:

    @classmethod
    def inserdata(cls, data, table):

        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        # 构造SQL语句其实是插入语句
        # ON DUPLICATE KEY UPDATE，如果主键已经存在，那就执行更新
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table, keys=keys,
                                                                                              values=values)  # UPDATE 后面要加空格
        update = ','.join(["{key} = %s".format(key=key)
                           for key in data])  # join结果id = %s, name = %s, time = %s
        sql += update

        # try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            print('Inser_All Successful')
            db.commit()
        else:
        # except Exception:
            print("Inser_All Failed")
            db.rollback()

    @classmethod
    def closeDB(cls):
        db.close()

    @classmethod
    def inser_editor(cls, data, table):
        sql = 'INSERT INTO {table}(Editor, Source, Times, Comments) VALUES (%(Editor)s,%(Source)s,%(Times)s,%(Comments)s)'.format(table=table)
        try:
            if cursor.execute(sql, data):
                print('Inser_editor Successful')
                db.commit()
        except Exception:
            print("Inser_editor Failed")
            db.rollback()

    @classmethod
    def inser_source(cls, data, table):
        sql = 'INSERT INTO {table}(Source, Times, Comments) VALUES (%(Source)s,%(Times)s,%(Comments)s)'.format(
            table=table)
        try:
            if cursor.execute(sql, data):
                print('inser_source Successful')
                db.commit()
        except Exception:
            print("inser_source Failed")
            db.rollback()
