from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

con = duckdb.connect()

# 先加载授权订单表
path = (DATA / "orders.csv").as_posix()

con.execute(
    "CREATE TABLE orders AS SELECT * FROM read_csv_auto(?)",
    [path]
)

# 再关闭外部访问
con.execute("SET enable_external_access = false")

# 测试 1：正常读取数据库表
result = con.execute(
    "SELECT COUNT(*) FROM orders"
).fetchone()[0]

assert result == 240
print("正常查询通过")

# 测试 2：尝试从 SQL 读取 CSV
try:
    con.execute(
        "SELECT * FROM read_csv_auto(?)",
        [path]
    ).fetchall()

except duckdb.Error:
    print("外部文件读取已拦截")

else:
    raise AssertionError("安全检查失败：仍然能够读取外部文件")