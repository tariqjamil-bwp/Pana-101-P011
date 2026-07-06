import csv
import json
import re
import os
from difflib import SequenceMatcher

RECORDS_FILE = "records.csv"
KNOWN_FILE = "known_totals.csv"
RULES_FILE = "rules.json"

def slurp_csv(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return rows

def find_column(rows, hints):
    """Find first column whose name contains any of the hint strings (case-insensitive)."""
    if not rows:
        return None
    keys = list(rows[0].keys())
    for hint in hints:
        for k in keys:
            if hint.lower() in k.lower():
                return k
    return keys[0]

def normalize(s):
    return re.sub(r"[^a-z0-9\s]", "", s.lower()).strip()

def normalize_alpha(s):
    return re.sub(r"[^a-z\s]", "", s.lower()).strip()

def auto_generate_rules(records, known_names):
    """Try to match each record sender to a known contributor."""
    rules = {"name_mapping": {}, "known_contributors": known_names}
    norm_known = {normalize(n): n for n in known_names}

    for r in records:
        sender = r.get("sender_raw", "").strip()
        if not sender:
            continue

        sender_lower = sender.lower()
        sender_norm = normalize(sender)

        # 1. Exact match after normalization
        if sender_norm in norm_known:
            rules["name_mapping"][sender_lower] = norm_known[sender_norm]
            continue

        # 2. Try stripping digits and re-check
        sender_alpha = normalize_alpha(sender)
        candidates = [sender_norm]
        if sender_alpha != sender_norm:
            candidates.append(sender_alpha)

        matched = False
        for c in candidates:
            for kn, original in norm_known.items():
                if c in kn or kn in c:
                    rules["name_mapping"][sender_lower] = original
                    matched = True
                    break
            if matched:
                break

        if matched:
            continue

        # 3. Character-level fuzzy match
        best_match = None
        best_score = 0
        for known in known_names:
            score = SequenceMatcher(None, sender_norm, normalize(known)).ratio()
            if score > best_score:
                best_score = score
                best_match = known

        rules["name_mapping"][sender_lower] = best_match if best_score >= 0.5 else None

    return rules

def main():
    records_raw = slurp_csv(RECORDS_FILE)
    known_raw = slurp_csv(KNOWN_FILE)

    if not records_raw or not known_raw:
        print("ERROR: Could not read records.csv or known_totals.csv")
        return

    sender_col = find_column(records_raw, ["sender", "from", "name", "person", "payer"])
    amount_col = find_column(records_raw, ["amount", "amt", "value", "total"])
    memo_col = find_column(records_raw, ["memo", "note", "description", "desc", "reference"])
    name_col = find_column(known_raw, ["person", "name", "contributor"])
    expected_col = find_column(known_raw, ["expected", "amount", "total", "value"])

    known_names = [r[name_col].strip() for r in known_raw]
    known = {r[name_col].strip(): float(r[expected_col]) for r in known_raw}
    known_total = sum(known.values())

    records = []
    for r in records_raw:
        records.append({
            "sender_raw": r[sender_col].strip(),
            "amount": float(r[amount_col]),
            "memo": r[memo_col].strip() if memo_col else "",
        })

    if not os.path.exists(RULES_FILE):
        print(f"  Generating {RULES_FILE} from data...")
        rules = auto_generate_rules(records, known_names)

        unsure = {k: v for k, v in rules["name_mapping"].items() if v is None}
        if unsure:
            print(f"\n  WARNING: Could not confidently match these senders:")
            for s in unsure:
                print(f"    \"{s}\" — no match found")

        with open(RULES_FILE, "w") as f:
            json.dump(rules, f, indent=2)
        print(f"  Saved to {RULES_FILE}. Review and edit if needed, then re-run.")
        print()
        return

    with open(RULES_FILE) as f:
        rules = json.load(f)

    name_map = {k.lower().strip(): v for k, v in rules["name_mapping"].items()}
    known_contributors = rules.get("known_contributors", known_names)

    mapped = {}
    unmatched = []
    for r in records:
        key = r["sender_raw"].lower().strip()
        person = name_map.get(key)
        if person:
            mapped.setdefault(person, []).append(r)
        else:
            unmatched.append(r)

    raw_total = sum(r["amount"] for r in records)
    gap = raw_total - known_total

    print("=" * 60)
    print("THE BOOKS DON'T MATCH — Reconciliation")
    print("=" * 60)

    print(f"\n  You counted:       {known_total:>8.0f} PKR")
    print(f"  Records show:      {raw_total:>8.0f} PKR")
    print(f"  Gap:               {gap:>+8.0f} PKR")
    print()

    problem_people = []
    ok_count = 0

    for person in known:
        paid = sum(r["amount"] for r in mapped.get(person, []))
        diff = paid - known[person]
        if abs(diff) < 1:
            ok_count += 1
        else:
            problem_people.append((person, known[person], paid, diff, mapped.get(person, [])))

    if problem_people:
        print("--- NEEDS FOLLOW-UP ---")
        for person, expected, paid, diff, entries in problem_people:
            if diff > 0 and len(entries) > 1:
                print(f"  [{person}] Expected {expected:.0f}, got {paid:.0f} ({diff:+.0f})")
                for e in entries:
                    print(f"     → \"{e['sender_raw']}\" {e['amount']:.0f}")
                print(f"     ⚠ Possible duplicate — check with {person}")
            elif diff > 0:
                print(f"  [{person}] Expected {expected:.0f}, got {paid:.0f} ({diff:+.0f}) — overpayment")
            else:
                print(f"  [{person}] Expected {expected:.0f}, got {paid:.0f} ({diff:+.0f}) — short by {abs(diff):.0f}")

    if unmatched:
        print(f"\n--- UNKNOWN SENDERS ---")
        for r in unmatched:
            print(f"  \"{r['sender_raw']}\"  {r['amount']:.0f}  ({r['memo']}) — find out who this is")

    print(f"\n  {ok_count} of {len(known)} people match perfectly.")
    print()

if __name__ == "__main__":
    main()
