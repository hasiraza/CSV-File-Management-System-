# Skill: summarize
# Generates human-readable run summaries from pipeline results

## Purpose
After the pipeline completes, this skill formats the result dict
into a readable console report and a JSON memory file.

## Function: `summarize_run(result: dict) → str`

```python
import json, os
from datetime import datetime

def summarize_run(result: dict, save_path: str = None) -> str:
    lines = [
        "=" * 50,
        "  CSV FILE MANAGEMENT AGENT — RUN SUMMARY",
        "=" * 50,
        f"  Status         : {result.get('status', 'unknown').upper()}",
        f"  Steps Done     : {result.get('steps_completed', '?')} / 7",
        f"  Rows Updated   : {result.get('total_rows_updated', '?')} / 100",
        f"  Duration       : {result.get('duration_seconds', '?')}s",
        f"  Timestamp      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 50,
    ]
    if result.get("errors"):
        lines.append("  ERRORS:")
        for e in result["errors"]:
            lines.append(f"    • {e}")
        lines.append("=" * 50)

    summary = "\n".join(lines)
    print(summary)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as f:
            json.dump(result, f, indent=2)

    return summary
```

## Usage
```python
result = {
    "status": "success",
    "steps_completed": 7,
    "total_rows_updated": 100,
    "duration_seconds": 1.38,
    "errors": []
}
summarize_run(result, save_path="data/memories/last_run.json")
```