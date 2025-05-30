import pymysql.cursors
# Connect to the database


CONNECTION = pymysql.connect(
    host='localhost',
    user='root',
    password='root123',
    port=3307,
    database='stock',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
