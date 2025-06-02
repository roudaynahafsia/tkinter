import pymysql.cursors

CONNECTION = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='Rayen2001',
    port=3306,
    database='stock',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
