from pathlib import Path
import duckdb

DATA = Path(__file__).resolve().parents[1] / "data"

con = duckdb.connect()

for table in ["orders", "users", "products"]:
    path = (DATA / f"{table}.csv").as_posix()

    con.execute(
        f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto(?)",
        [path]
    )

    print(f"\n=== {table} ===")
    print(con.execute(f"DESCRIBE {table}").df().to_string(index=False))