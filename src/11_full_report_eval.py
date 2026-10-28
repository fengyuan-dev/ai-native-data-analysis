from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "output" / "channel_revenue.csv")
total = df["revenue"].sum()

pattern = r"^\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|\s*([\d.]+)%\s*\|$"


def evaluate_report(report):
    rows = {}

    for line in report.splitlines():
        match = re.match(pattern, line.strip())

        if match:
            channel, amount, percentage = match.groups()

            if channel == "合计":
                continue

            if channel in rows:
                return False

            rows[channel] = (
                float(amount.replace(",", "")),
                float(percentage)
            )

    # 检查渠道是否完整
    expected_channels = set(df["acquisition_channel"])

    if set(rows) != expected_channels:
        return False

    # 检查各渠道金额及占比
    for _, row in df.iterrows():
        channel = row["acquisition_channel"]
        expected_revenue = row["revenue"]
        expected_percentage = expected_revenue / total * 100

        actual_revenue, actual_percentage = rows[channel]

        if abs(actual_revenue - expected_revenue) >= 0.01:
            return False

        if abs(actual_percentage - expected_percentage) >= 0.01:
            return False

    return True

correct_report = """
| 渠道 | 收入 | 收入占比 |
|---|---:|---:|
| 广告 | 13,656 | 43.64% |
| 自然搜索 | 8,071 | 25.79% |
| 推荐 | 5,579 | 17.83% |
| 直接访问 | 3,986 | 12.74% |
"""

tests = {
    "R01": correct_report,

    "R02": correct_report.replace(
        "| 推荐 | 5,579 | 17.83% |", ""
    ),

    "R03": correct_report +
        "\n| 广告 | 13,656 | 43.64% |",

    "R04": correct_report.replace(
        "43.64%", "53.64%"
    ),

    "R05": correct_report.replace(
        "13,656", "15,656"
    )
}

expected = {
    "R01": True,
    "R02": False,
    "R03": False,
    "R04": False,
    "R05": False
}

for name, report in tests.items():
    predicted = evaluate_report(report)
    correct = predicted == expected[name]

    print(
        name,
        "predicted =", "pass" if predicted else "fail",
        "correct =", correct
    )