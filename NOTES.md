# Working Notes

## Dataset: Salesforce xlam-function-calling-60k

60k synthetic function-calling examples across 21 domains, generated via
Salesforce's APIGen pipeline with multi-stage quality filtering (format,
executable, semantic). Gated dataset - requires HF account + access request
+ token.

Known issue (per HF dataset discussion #8): ~472 of 60k rows (0.8%) have
invalid function names or missing required arguments. Verified all 400
curated examples (350 train + 50 eval, seed=42) against this specific
check - zero invalid examples in our sample.

Confirmed zero ID overlap between train and eval sets - no data leakage
for the fine-tuned model evaluation.

Examples range from single function calls to up to 4 calls in one query -
real difficulty variation, not uniformly simple.