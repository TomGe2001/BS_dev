import MySQLdb

def get_connection():
    # 连接数据库
    conn = MySQLdb.connect(
        host="localhost",
        user="username",
        password="password",
        database="database_name"
    )
    # 返回连接对象
    return conn
