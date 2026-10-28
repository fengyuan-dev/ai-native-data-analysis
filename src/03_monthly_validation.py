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

orders_df = pd.read_csv(DATA / "orders.csv")

orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

sql = """
SELECT
    strftime('%Y-%m', order_date)          AS month,
    COUNT(*)                               AS paid_orders,
    SUM(amount)                            AS total_revenue,
    COUNT(DISTINCT user_id)                AS paying_users,
    ROUND(SUM(amount) / COUNT(DISTINCT user_id), 2) AS arppu
FROM orders
WHERE status = 'paid'
GROUP BY month
ORDER BY month
"""
sql_result = con.execute(sql).df()

df_paid = orders_df[orders_df["status"] == "paid"].copy()
df_paid["month"] = df_paid["order_date"].dt.strftime("%Y-%m")
pandas_result = (
    df_paid.groupby("month")
    .agg(
        paid_orders=("order_id", "count"),
        total_revenue=("amount", "sum"),
        paying_users=("user_id", "nunique"),
    )
    .assign(arppu=lambda d: (d["total_revenue"] / d["paying_users"]).round(2))
    .reset_index()
)

pd.testing.assert_frame_equal(
    sql_result.sort_values("month").reset_index(drop=True),
    pandas_result.sort_values("month").reset_index(drop=True),
    check_dtype=False,
    atol=0.01,
)
print("SQL/Pandas validation passed!")