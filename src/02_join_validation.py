from pathlib import Path
import duckdb

# 项目根目录
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# 连接 DuckDB
con = duckdb.connect()

# 加载三张 CSV 表
for table in ["orders", "users", "products"]:
    file_path = (DATA / f"{table}.csv").as_posix()

    con.execute(
        f"""
        CREATE TABLE {table} AS
        SELECT *
        FROM read_csv_auto(?)
        """,
        [file_path]
    )

print("三张表加载成功！")
# 检查三张表的行数
sql = """
SELECT 'orders' AS table_name, COUNT(*) AS row_count
FROM orders

UNION ALL

SELECT 'users', COUNT(*)
FROM users

UNION ALL

SELECT 'products', COUNT(*)
FROM products;
"""

result = con.execute(sql).df()

print("\n三张表的行数：")
print(result.to_string(index=False))
# 三表 JOIN 粒度检查
join_sql = """
SELECT
    COUNT(*) AS joined_rows,
    COUNT(DISTINCT o.order_id) AS unique_orders
FROM orders o
LEFT JOIN users u
    ON o.user_id = u.user_id
LEFT JOIN products p
    ON o.product_id = p.product_id;
"""

join_result = con.execute(join_sql).df()

print("\nJOIN 检查结果：")
print(join_result.to_string(index=False))

# 检查未匹配的用户和产品
unmatched_sql = """
SELECT
    COUNT(*) FILTER (
        WHERE u.user_id IS NULL
    ) AS unmatched_users,

    COUNT(*) FILTER (
        WHERE p.product_id IS NULL
    ) AS unmatched_products

FROM orders o
LEFT JOIN users u
    ON o.user_id = u.user_id
LEFT JOIN products p
    ON o.product_id = p.product_id
"""

unmatched_result = con.execute(unmatched_sql).df()

print("\n未匹配检查结果：")
print(unmatched_result.to_string(index=False))

assert unmatched_result.loc[0, "unmatched_users"] == 0
assert unmatched_result.loc[0, "unmatched_products"] == 0

print("Unmatched checks passed.")