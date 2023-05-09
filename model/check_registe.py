from templates.config import get_connection

def add_user(username, password):
    try:
        # 获取数据库连接
        conn = get_connection()
        # 创建游标对象
        cur = conn.cursor()
        # 执行 SQL 命令
        sql = "INSERT INTO user(username, password) VALUES (%s, %s)"
        cur.execute(sql, (username, password))
        # 提交到数据库
        conn.commit()
    except Exception as e:
        # 处理异常情况
        print(f"Error: {e}")
        conn.rollback()
    finally:
        # 关闭游标和连接
        cur.close()
        conn.close()
