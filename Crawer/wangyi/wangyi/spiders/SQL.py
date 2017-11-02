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
        sql = 'INSERT INTO {table}(Editor, Source, Times, Comments) VALUES (%(Editor)s,%(Source)s,%(Times)s,%(Comments)s)'.format(
            table=table)
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

    @classmethod
    def reach_Template(cls, keys):
        # 传入SQL中 =等号右边的需要是字符串，SQL命令在python中本身也是字符串。需要在等号右边字符串外面添加引号" "，再用format格式化 动态赋值
        sql = "SELECT Website_title,Website_author,Website_pubtime,Website_content,Website_source" \
              " FROM Website_info WHERE Website_name='{key}'".format(key=keys)

        # 提取出字段名和值，并存入到定义的字典当中
        template = {}
        try:
            cursor.execute(sql)
            results = cursor.fetchall()  # 得到值,结果的第一个信息为模板的值
            cols = []  # 定义保存字段名的list
            for col in cursor.description:
                cols.append(col[0])
            # zip()函数：将两个序列合并，返回zip对象，可强制转换为列表或字典
            for (row, col) in zip(results[0], cols):
                template[col] = row

            # zip结果字典，将results[0]和cols合并，然后类型转换为dict
            dict_data = zip(results[0], cols)
            dict_data = dict(dict_data)
            return template
        except Exception:
            print('Select Error')
