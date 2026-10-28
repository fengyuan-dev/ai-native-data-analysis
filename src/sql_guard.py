import sqlglot
from sqlglot import exp


def validate_sql(sql):
    statements = sqlglot.parse(sql, read="duckdb")

    if len(statements) != 1 or statements[0] is None:
        raise ValueError("只允许一条 SQL")

    query = statements[0]

    if not isinstance(query, exp.Select):
        raise ValueError("只允许 SELECT 查询")

    # 当前版本不支持子查询和 CTE
    selects = list(query.find_all(exp.Select))
    if len(selects) != 1:
        raise ValueError("暂不允许嵌套查询")

    if query.args.get("with_"):
        raise ValueError("暂不允许 CTE")

    # 只允许访问指定的业务表
    allowed_tables = {"orders", "users"}

    for table in query.find_all(exp.Table):
        if (
            table.name.lower() not in allowed_tables
            or table.db
            or table.catalog
        ):
            raise ValueError(f"禁止访问表：{table.sql()}")

    # 禁止 SELECT *，避免直接输出全部字段
    if any(isinstance(node, exp.Star) for node in query.walk()):
        raise ValueError("不允许 SELECT *")

    # 禁止未识别的通用函数
    if any(isinstance(node, exp.Anonymous) for node in query.walk()):
        raise ValueError("包含未授权函数")

    # 只允许本次任务需要的字段
    allowed_columns = {
        ("o", "user_id"),
        ("o", "amount"),
        ("o", "status"),
        ("o", "order_date"),
        ("u", "user_id"),
        ("u", "acquisition_channel"),
        ("", "revenue"),
    }

    for column in query.find_all(exp.Column):
        item = (column.table.lower(), column.name.lower())

        if item not in allowed_columns:
            raise ValueError(f"禁止访问字段：{column.sql()}")

    print("SQL 结构检查通过")
    return sql