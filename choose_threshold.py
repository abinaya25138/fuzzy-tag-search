"""
Choose the match threshold from labeled data instead of guessing.

Input: a CSV with columns query, description, same_equipment (1 or 0), where
each row is a query-tag pair labeled by hand. The script scores every pair,
then reports precision, recall and F1 at each candidate threshold and picks
the one with the best F1.

Usage:
    python choose_threshold.py labeled_pairs.csv
"""
import csv
import sys

from matching import match_score


def evaluate(pairs, threshold):
    tp = sum(1 for s, y in pairs if s >= threshold and y == 1)
    fp = sum(1 for s, y in pairs if s >= threshold and y == 0)
    fn = sum(1 for s, y in pairs if s < threshold and y == 1)
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def main(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    pairs = [(match_score(r["query"], r["description"]), int(r["same_equipment"])) for r in rows]
    print(f"{len(pairs)} labeled pairs, {sum(y for _, y in pairs)} same-equipment\n")
    print("threshold  precision  recall  F1")
    candidates = sorted({round(s, 3) for s, _ in pairs})
    best = None
    for t in candidates:
        p, r, f1 = evaluate(pairs, t)
        print(f"{t:9.3f}  {p:9.2f}  {r:6.2f}  {f1:.2f}")
        if best is None or f1 > best[1]:
            best = (t, f1)
    print(f"\nBest threshold: {best[0]:.3f} (F1 {best[1]:.2f})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "examples/labeled_pairs_example.csv")
