import json
from pathlib import Path

import pytest

TRAIN_PATH = Path("data/curated_train.json")
EVAL_PATH = Path("data/eval/golden_eval.json")

requires_data = pytest.mark.skipif(
    not TRAIN_PATH.exists() or not EVAL_PATH.exists(),
    reason="Curated data not present - run `uv run python -m src.cli curate` first",
)


@requires_data
def test_no_overlap_between_train_and_eval():

    train = json.loads(TRAIN_PATH.read_text())
    eval_set = json.loads(EVAL_PATH.read_text())

    train_ids = {ex["id"] for ex in train}
    eval_ids = {ex["id"] for ex in eval_set}
    assert train_ids.isdisjoint(eval_ids)


@requires_data
def test_all_examples_are_valid():
    from src.curation import validate_example

    train = json.loads(TRAIN_PATH.read_text())
    eval_set = json.loads(EVAL_PATH.read_text())

    invalid = [ex for ex in train + eval_set if not validate_example(ex)]
    assert invalid == []