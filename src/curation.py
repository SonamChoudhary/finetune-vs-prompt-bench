"""Curate a subset of the xlam-function-calling-60k dataset for fine-tuning."""

import json
import random
from pathlib import Path

from datasets import load_dataset

TRAIN_PATH = Path("data/curated_train.json")
EVAL_PATH = Path("data/eval/golden_eval.json")
SEED = 42


def load_and_parse(hf_token: str | None = None) -> list[dict]:
    """Load the dataset and parse the JSON-encoded tools/answers fields."""
    ds = load_dataset(
        "Salesforce/xlam-function-calling-60k", split="train", token=hf_token
    )

    parsed = []
    skipped = 0
    for row in ds:
        try:
            tools = json.loads(row["tools"])
            answers = json.loads(row["answers"])
        except (json.JSONDecodeError, TypeError):
            skipped += 1
            continue
        parsed.append(
            {
                "id": row["id"],
                "query": row["query"],
                "tools": tools,
                "answers": answers,
            }
        )

    print(f"Parsed {len(parsed)} examples, skipped {skipped} malformed rows")
    return parsed


def curate(train_size: int = 350, eval_size: int = 50, hf_token: str | None = None):
    """Sample a non-overlapping train/eval split and save both to disk."""
    examples = load_and_parse(hf_token)

    rng = random.Random(SEED)
    rng.shuffle(examples)

    train_set = examples[:train_size]
    eval_set = examples[train_size : train_size + eval_size]

    TRAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVAL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(TRAIN_PATH, "w") as f:
        json.dump(train_set, f, indent=2)
    with open(EVAL_PATH, "w") as f:
        json.dump(eval_set, f, indent=2)

    print(f"Saved {len(train_set)} training examples to {TRAIN_PATH}")
    print(f"Saved {len(eval_set)} eval examples to {EVAL_PATH}")

def validate_example(example: dict) -> bool:
    """Check that every answer references a real tool and has required arguments."""
    tool_params = {}
    for tool in example["tools"]:
        required = [
            name for name, spec in tool["parameters"].items()
            if spec.get("required", False)
            or ("default" not in spec and "optional" not in str(spec.get("type", "")))
        ]
        tool_params[tool["name"]] = required

    for ans in example["answers"]:
        if ans["name"] not in tool_params:
            return False
        if tool_params[ans["name"]] and not ans["arguments"]:
            return False
    return True