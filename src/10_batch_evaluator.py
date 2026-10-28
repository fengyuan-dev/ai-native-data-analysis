import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# 读取测试案例
with open(ROOT / "eval" / "eval_cases.json", encoding="utf-8") as f:
    cases = json.load(f)

# 读取真实渠道收入
df = pd.read_csv(ROOT / "output" / "channel_revenue.csv")

total = df["revenue"].sum()

results = []

for case in cases:

    # 暂时跳过语义测试
    if case["type"] != "numeric":
        continue

    channel = case["channel"]
    actual_revenue = case["revenue"]
    actual_percentage = case["percentage"]

    matched = df.loc[
    df["acquisition_channel"] == channel,
    "revenue"
    ]

    if len(matched) != 1:
        is_valid = False
    else:
        expected_revenue = matched.iloc[0]
        expected_percentage = expected_revenue / total * 100

        is_valid = (
            abs(actual_revenue - expected_revenue) < 0.01
            and abs(actual_percentage - expected_percentage) < 0.01
        )
    predicted = "pass" if is_valid else "fail"

    results.append({
        "id": case["id"],
        "expected": case["expected"],
        "predicted": predicted,
        "correct": predicted == case["expected"]
    })

result_df = pd.DataFrame(results)

print(result_df.to_string(index=False))

accuracy = result_df["correct"].mean()

print(f"\nAccuracy: {accuracy:.2%}")

# 将 fail 视为正类
tp = ((result_df["expected"] == "fail") &
      (result_df["predicted"] == "fail")).sum()

fp = ((result_df["expected"] == "pass") &
      (result_df["predicted"] == "fail")).sum()

fn = ((result_df["expected"] == "fail") &
      (result_df["predicted"] == "pass")).sum()

tn = ((result_df["expected"] == "pass") &
      (result_df["predicted"] == "pass")).sum()

precision = tp / (tp + fp) if tp + fp > 0 else 0
recall = tp / (tp + fn) if tp + fn > 0 else 0
fpr = fp / (fp + tn) if fp + tn > 0 else 0

print(f"\nTP={tp}, FP={fp}, FN={fn}, TN={tn}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"FPR: {fpr:.2%}")

output_dir = ROOT / "output"
output_dir.mkdir(exist_ok=True)

result_df.to_csv(
    output_dir / "numeric_eval_results.csv",
    index=False,
    encoding="utf-8-sig"
)

print("数值评估结果已保存")