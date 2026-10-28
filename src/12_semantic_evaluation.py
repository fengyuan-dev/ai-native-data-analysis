import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

with open(ROOT / "eval" / "semantic_cases.json", encoding="utf-8") as f:
    cases = json.load(f)

# 第一轮人工审核标签
# 这些是人工给出的预测标签，不是 AI 自动判断
manual_predictions = {
    "S01": "pass",
    "S02": "fail",
    "S03": "pass",
    "S04": "fail"
}

results = []

for case in cases:
    predicted = manual_predictions[case["id"]]

    results.append({
        "id": case["id"],
        "expected": case["expected"],
        "predicted": predicted,
        "correct": predicted == case["expected"],
        "error_type": case["error_type"]
    })

result_df = pd.DataFrame(results)

print(result_df.to_string(index=False))

accuracy = result_df["correct"].mean()
print(f"\nSemantic labeling agreement: {accuracy:.2%}")

# 保存评估记录
output_dir = ROOT / "output"
output_dir.mkdir(exist_ok=True)

result_df.to_csv(
    output_dir / "semantic_eval_results.csv",
    index=False,
    encoding="utf-8-sig"
)

print("语义评估记录已保存")