
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

scripts = [
    "01_baseline.py",
    "02_join_validation.py",
    "03_monthly_validation.py",
    "05_ai_sql_runner.py",
    "10_batch_evaluator.py",
    "11_full_report_eval.py",
    "13_judge_evaluator.py",
    "14_holdout_evaluator.py",
]

for script in scripts:
    print(f"\n{'=' * 50}")
    print(f"正在执行：{script}")
    print("=" * 50, flush=True)

    result = subprocess.run(
        [sys.executable, str(ROOT / "src" / script)],
        cwd=ROOT
    )

    if result.returncode != 0:
        print(f"\n运行失败：{script}")
        sys.exit(1)

print("\n所有项目检查已完成！")
