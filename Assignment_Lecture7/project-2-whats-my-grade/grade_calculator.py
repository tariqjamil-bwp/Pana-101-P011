import csv
import os
from collections import defaultdict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SCORES_FILE = "scores.csv"
POLICY_FILE = "grading_policy.csv"

GRADE_BOUNDARIES = [
    ("A+", 90, 4.00), ("A", 85, 4.00), ("A-", 80, 3.70),
    ("B+", 75, 3.30), ("B", 70, 3.00), ("B-", 65, 2.70),
    ("C+", 60, 2.30), ("C", 55, 2.00), ("C-", 50, 1.70),
    ("F", 0, 0.00),
]

def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))

def letter_grade(pct):
    for grade, threshold, _ in GRADE_BOUNDARIES:
        if pct >= threshold:
            return grade
    return "F"

def gpa_points(pct):
    for _, threshold, gpa in GRADE_BOUNDARIES:
        if pct >= threshold:
            return gpa
    return 0.0

def main():
    policy_rows = load_csv(POLICY_FILE)
    policy = {}
    for r in policy_rows:
        cat = r["Category"].strip()
        policy[cat] = {
            "weight": float(r["Weight"]) / 100,
            "drop": int(r["DropLowest"]),
        }

    scores = load_csv(SCORES_FILE)
    by_cat = defaultdict(list)
    for s in scores:
        by_cat[s["Category"].strip()].append({
            "item": s["Item"].strip(),
            "score": float(s["Score"]) if s["Score"].strip() else None,
            "max": float(s["Max"].strip()),
            "weight": float(s.get("Weight", 100)) if s.get("Weight", "").strip() else 100,
        })

    print("=" * 60)
    print("WHAT'S MY GRADE — Grade Calculator")
    print("=" * 60)
    print()

    cat_results = {}
    total_weighted = 0
    total_weight = 0

    for cat, cfg in policy.items():
        entries = by_cat.get(cat, [])
        weight = cfg["weight"]
        drop = cfg["drop"]

        if not entries:
            cat_results[cat] = {"pct": 0, "weight": weight, "pending": [], "dropped": []}
            print(f"  {cat:20s}  — no entries found (weight: {weight*100:.0f}%)")
            continue

        scored = [e for e in entries if e["score"] is not None]
        pending = [e for e in entries if e["score"] is None]

        if not scored:
            cat_results[cat] = {"pct": 0, "weight": weight, "pending": pending, "dropped": []}
            print(f"  {cat:20s}  — no scores yet (weight: {weight*100:.0f}%)")
            continue

        raw_pcts = [e["score"] / e["max"] * 100 for e in scored]
        sub_weights = [e["weight"] for e in scored]
        total_sub_weight = sum(sub_weights)

        if drop > 0 and len(raw_pcts) > drop:
            combined = sorted(zip(raw_pcts, sub_weights), key=lambda x: x[0])
            dropped_vals = [p for p, _ in combined[:drop]]
            kept = combined[drop:]
            cat_pct = sum(p * w for p, w in kept) / sum(w for _, w in kept)
        else:
            cat_pct = sum(p * w for p, w in zip(raw_pcts, sub_weights)) / total_sub_weight
            dropped_vals = []

        cat_results[cat] = {
            "pct": cat_pct,
            "weight": weight,
            "pending": pending,
            "dropped": dropped_vals,
        }
        total_weighted += cat_pct * weight
        total_weight += weight

    total_gpa = 0
    print("--- CATEGORY BREAKDOWN ---")
    for cat in policy:
        r = cat_results.get(cat)
        if not r:
            continue
        gpa = gpa_points(r["pct"])
        total_gpa += gpa * r["weight"]
        drop_info = ""
        if r["dropped"]:
            drop_info = f" (dropped {len(r['dropped'])}: {', '.join(f'{d:.0f}%' for d in r['dropped'])})"
        pend_info = ""
        if r["pending"]:
            pend_info = f" | {len(r['pending'])} pending"
        print(f"  {cat:25s}  {r['pct']:5.1f}%  {letter_grade(r['pct']):>2s} ({gpa:.2f}) × {r['weight']*100:.0f}% = {r['pct']*r['weight']:5.1f}%{drop_info}{pend_info}")

    print()
    print(f"  {'Total so far':25s}  {total_weighted:5.1f}% / {total_weight*100:.0f}% of grade")

    current_overall = total_weighted / total_weight if total_weight > 0 else 0
    cgpa = total_gpa / total_weight if total_weight > 0 else 0
    print(f"  {'Current grade':25s}  {current_overall:5.1f}%  ({letter_grade(current_overall)})  GPA: {cgpa:.2f} / 4.00")
    print()

    pending_final_cats = {cat: r for cat, r in cat_results.items() if r["pending"]}
    if pending_final_cats:
        print("--- WHAT I NEED ON PENDING ITEMS ---")
        for cat, r in pending_final_cats.items():
            w = r["weight"]
            print(f"  {cat} (weight: {w*100:.0f}%):")
            for grade_name, threshold in GRADE_BOUNDARIES:
                if threshold < 60:
                    continue
                if current_overall >= threshold:
                    print(f"    {grade_name:4s} ({threshold:2d}%): Already achieved!")
                    continue
                needed = (threshold - total_weighted) / w
                if needed > 100:
                    continue
                print(f"    {grade_name:4s} ({threshold:2d}%): Need {needed:.1f}%")
        print()

    print("--- ALL SCORES ---")
    for cat in policy:
        entries = by_cat.get(cat, [])
        if not entries:
            continue
        print(f"  {cat}:")
        for e in entries:
            if e["score"] is not None:
                pct = e["score"] / e["max"] * 100
                print(f"    {e['item']:30s} {e['score']:>4.0f}/{e['max']:<4.0f}  ({pct:.0f}%)")
            else:
                print(f"    {e['item']:30s} {'—':>4s}/{e['max']:<4.0f}")
    print()

if __name__ == "__main__":
    main()
