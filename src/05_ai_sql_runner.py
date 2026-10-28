from pathlib import Path
import duckdb

from sql_guard import validate_sql


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

con = duckdb.connect()

# 1. 加载授权数据
for table in ["orders", "users"]:
    path = (DATA / f"{table}.csv").as_posix()

    con.execute(
        f"""
        CREATE TABLE {table} AS
        SELECT * FROM read_csv_auto(?)
        """,
        [path]
    )

# 2. 关闭外部访问并锁定配置
con.execute("SET enable_external_access = false")
con.execute("SET lock_configuration = true")

# 3. AI 生成的 SQL
# 读取 AI 生成的 SQL 文件
sql_path = ROOT / "sql" / "channel_revenue.sql"

sql = sql_path.read_text(encoding="utf-8")

# 4. 校验后再执行
validated_sql = validate_sql(sql)

result = con.execute(validated_sql).df()

print(result.to_string(index=False))

# 5. 结果核验
assert abs(result["revenue"].sum() - 31292) < 0.01

print("Revenue validation passed!")

# 只有通过收入核验后才保存结果
output_dir = ROOT / "output"
output_dir.mkdir(exist_ok=True)

output_path = output_dir / "channel_revenue.csv"

result.to_csv(output_path, index=False, encoding="utf-8-sig")

print("分析结果已保存：", output_path)