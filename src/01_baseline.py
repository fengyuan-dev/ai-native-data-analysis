from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

con = duckdb.connect()

orders_path = (DATA / "orders.csv").as_posix()

con.execute(
    """
    CREATE TABLE orders AS
    SELECT *
    FROM read_csv_auto(?)
    """,
    [orders_path]
)

result = con.execute(
    """
    SELECT
        COUNT(*) AS paid_orders,
        SUM(amount) AS total_revenue,
        COUNT(DISTINCT user_id) AS paying_users
    FROM orders
    WHERE status = 'paid'
    """
).df()

print(result.to_string(index=False))

assert result.loc[0, "paid_orders"] == 184
assert result.loc[0, "total_revenue"] == 64471
assert result.loc[0, "paying_users"] == 72

print("Baseline checks passed.")