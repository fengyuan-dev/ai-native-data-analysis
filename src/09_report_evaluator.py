from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parents[1]

# 读取真实数据和 AI 报告
df = pd.read_csv(ROOT / "output" / "channel_revenue.csv")
report = (ROOT / "output" / "channel_report.md").read_text(
    encoding="utf-8"
)

# SQL 查询结果作为标准答案
total = df["revenue"].sum()

assert abs(total - 31292) < 0.01

# 解析 Markdown 表格
pattern = r"^\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|\s*([\d.]+)%\s*\|$"

rows = {}

for line in report.splitlines():
    match = re.match(pattern, line.strip())

    if match:
        channel, amount, percentage = match.groups()

        if channel not in ["渠道", "合计"]:
            if channel in rows:
                raise AssertionError(f"重复渠道：{channel}")

            rows[channel] = (
                float(amount.replace(",", "")),
                float(percentage)
            )

# 检查渠道是否完整
assert set(rows) == set(df["acquisition_channel"])

# 检查金额及占比
for _, row in df.iterrows():
    channel = row["acquisition_channel"]
    expected_revenue = row["revenue"]
    expected_percentage = expected_revenue / total * 100

    actual_revenue, actual_percentage = rows[channel]

    assert abs(actual_revenue - expected_revenue) < 0.01
    assert abs(actual_percentage - expected_percentage) < 0.01

print("金额检查通过")
print("占比检查通过")
print("渠道完整性检查通过")
print("Report numeric validation passed!")