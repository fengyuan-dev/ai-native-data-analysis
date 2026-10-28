from sql_guard import validate_sql


tests = [
    ("正常查询", "SELECT o.amount FROM orders o"),
    ("删除表", "DROP TABLE users"),
    ("读取外部文件", "SELECT * FROM read_csv('secret.csv')"),
    ("未授权字段", "SELECT u.password FROM users u"),
]

for name, sql in tests:
    try:
        validate_sql(sql)
        print(name, "允许")
    except ValueError as e:
        print(name, "已拦截：", e)