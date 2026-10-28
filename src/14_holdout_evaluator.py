
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# 读取人工标准答案
with open(ROOT / "eval" / "semantic_holdout_gold.json", encoding="utf-8") as f:
    gold = json.load(f)

# 读取 LLM 实际预测
with open(ROOT / "eval" / "holdout_predictions_v1.json", encoding="utf-8") as f:
    predictions = json.load(f)

gold_df = pd.DataFrame(gold)
pred_df = pd.DataFrame(predictions)

# 检查 ID 是否完整、唯一
assert gold_df["id"].is_unique
assert pred_df["id"].is_unique
assert set(gold_df["id"]) == set(pred_df["id"])

# 按 ID 对齐，不依赖文件中的顺序
result = gold_df[["id", "expected", "error_type"]].merge(
    pred_df[["id", "predicted", "reason"]],
    on="id",
    validate="one_to_one"
)

# 检查标签有效性
assert result["predicted"].isin(["pass", "fail"]).all()

result["correct"] = result["expected"] == result["predicted"]

# fail 为正类（需要拦截的错误报告）
tp = ((result["expected"] == "fail") &
      (result["predicted"] == "fail")).sum()

fp = ((result["expected"] == "pass") &
      (result["predicted"] == "fail")).sum()

fn = ((result["expected"] == "fail") &
      (result["predicted"] == "pass")).sum()

tn = ((result["expected"] == "pass") &
      (result["predicted"] == "pass")).sum()

accuracy = result["correct"].mean()

def safe_div(a, b):
    return a / b if b else float("nan")

precision = safe_div(tp, tp + fp)
recall = safe_div(tp, tp + fn)
fpr = safe_div(fp, fp + tn)

print(result.to_string(index=False))

print(f"\nTP={tp}, FP={fp}, FN={fn}, TN={tn}")
print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"FPR: {fpr:.2%}")

# 单独输出判断错误的案例
errors = result[~result["correct"]]

print("\n误判案例：")
if errors.empty:
    print("当前测试集未发现误判")
else:
    print(errors.to_string(index=False))

# 保存评估结果
output = ROOT / "output"
output.mkdir(exist_ok=True)

result.to_csv(
    output / "holdout_eval_v1.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nJudge evaluation saved.")
