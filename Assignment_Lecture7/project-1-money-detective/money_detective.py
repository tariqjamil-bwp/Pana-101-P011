import csv
import os
from collections import defaultdict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CSV_FILE = "transactions.csv"

def load_transactions(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            date = r.get("Date", "").strip()
            desc = r.get("Description", "").strip()
            try:
                amount = float(r.get("Amount", "").strip())
            except (ValueError, TypeError):
                continue
            if not date or not desc:
                continue
            rows.append({"date": date, "desc": desc, "amount": amount})
    return rows

def get_month(date_str):
    return date_str[:7]

def categorize(desc):
    d = desc.lower()
    if any(k in d for k in ("k-electric", "ssgc", "water bill", "internet", "ptcl", "mobile top-up", "cable tv", "optical", "shoq ptcl")):
        return "Utilities & Subscriptions"
    if any(k in d for k in ("imtiaz", "daraz", "grocery", "bakery")):
        return "Groceries"
    if any(k in d for k in ("fuel", "pso", "car wash", "car maintenance", "oil change", "ac repair")):
        return "Transport & Vehicle"
    if any(k in d for k in ("netflix", "claude", "medium", "subscription")):
        return "Digital Subscriptions"
    if any(k in d for k in ("school fee", "panaversity")):
        return "Education"
    if any(k in d for k in ("medical", "pharmacy", "blood", "eye", "clinic")):
        return "Medical"
    if any(k in d for k in ("restaurant", "dawat", "salt")):
        return "Dining Out"
    if any(k in d for k in ("gym",)):
        return "Fitness"
    if any(k in d for k in ("eid", "gul ahmed", "shoe")):
        return "Shopping"
    return "Other"

def find_duplicates(rows):
    seen = defaultdict(list)
    for r in rows:
        seen[(r["date"], r["desc"], r["amount"])].append(r)
    return [(k, v) for k, v in seen.items() if len(v) > 1]

def find_recurring(rows, min_months=3):
    monthly = defaultdict(set)
    for r in rows:
        if r["amount"] < 0:
            monthly[(r["desc"], r["amount"])].add(get_month(r["date"]))
    return {k: sorted(v) for k, v in monthly.items() if len(v) >= min_months}

STOP_WORDS = {"-", "the", "a", "an", "and", "or", "of", "for", "in"}

def word_set(name):
    return {w for w in name.lower().replace("-", " ").split() if w not in STOP_WORDS}

def find_similar_services(rows):
    services = sorted(set(r["desc"] for r in rows), key=str.lower)
    pairs = []
    for i, a in enumerate(services):
        wa = word_set(a)
        for b in services[i+1:]:
            wb = word_set(b)
            smaller, larger = (wa, wb) if len(wa) <= len(wb) else (wb, wa)
            if len(smaller) >= 2 and smaller <= larger:
                pairs.append((a, b))
    return pairs

def find_recent_subs(rows):
    all_descs = set(r["desc"] for r in rows)
    subs = [d for d in all_descs if any(k in d.lower() for k in ("subscription", "netflix", "claude", "medium", "gym", "spotify", "shoq"))]
    findings = []
    for s in subs:
        entries = [r for r in rows if r["desc"] == s]
        first_month = min(get_month(r["date"]) for r in entries)
        total = sum(r["amount"] for r in entries)
        count = len(entries)
        findings.append((s, count, total, first_month))
    return sorted(findings, key=lambda x: x[2])

def monthly_trend(rows):
    by_month = defaultdict(float)
    for r in rows:
        by_month[get_month(r["date"])] += r["amount"]
    return dict(sorted(by_month.items()))

def find_billing_anomalies(rows):
    all_months = sorted(set(get_month(r["date"]) for r in rows))
    desc_months = defaultdict(lambda: defaultdict(int))
    desc_amounts = defaultdict(list)

    for r in rows:
        m = get_month(r["date"])
        desc_months[r["desc"]][m] += 1
        desc_amounts[r["desc"]].append(r["amount"])

    anomalies = []

    for desc, month_counts in desc_months.items():
        counts = list(month_counts.values())
        median_count = sorted(counts)[len(counts) // 2]

        for m, cnt in sorted(month_counts.items()):
            if cnt > median_count + 1:
                total_extra = sum(
                    r["amount"] for r in rows
                    if r["desc"] == desc and get_month(r["date"]) == m
                )
                anomalies.append({
                    "type": "extra_charge",
                    "desc": desc,
                    "month": m,
                    "count": cnt,
                    "expected": median_count,
                    "total": total_extra,
                })

    for desc in desc_months:
        months_present = sorted(desc_months[desc].keys())
        if len(months_present) < 2:
            continue
        for i in range(len(months_present) - 1):
            curr = months_present[i]
            next_m = months_present[i + 1]
            ci = all_months.index(curr)
            ni = all_months.index(next_m)
            if ni - ci > 1:
                gap_months = all_months[ci + 1:ni]
                anomalies.append({
                    "type": "gap",
                    "desc": desc,
                    "gap_start": curr,
                    "gap_end": next_m,
                    "gap_months": gap_months,
                })

    return anomalies

def main():
    rows = load_transactions(CSV_FILE)

    all_months = sorted(set(get_month(r["date"]) for r in rows))
    year = all_months[0][:4] if all_months else "20XX"
    jan_prefix = f"{year}-01"
    q2_cutoff = f"{year}-04"

    print("=" * 60)
    print("MONEY DETECTIVE — Spending Leak Finder")
    print("=" * 60)

    jan_total = sum(r["amount"] for r in rows if r["date"].startswith(jan_prefix))
    jan_daraz = sum(r["amount"] for r in rows if r["date"].startswith(jan_prefix) and "Daraz" in r["desc"])

    print(f"\n--- VERIFICATION (known baselines) ---")
    print(f"  Jan {year} total:              {jan_total:>8.0f}  (user said -86050, match: {abs(jan_total - (-86050)) < 1})")
    print(f"  Jan {year} Daraz Grocery total:     {jan_daraz:>8.0f}  (user said -4300, match: {abs(jan_daraz - (-4300)) < 1})")
    print()

    print("=== SPENDING BY CATEGORY ===")
    cats = defaultdict(float)
    for r in rows:
        cats[categorize(r["desc"])] += r["amount"]
    for cat, total in sorted(cats.items(), key=lambda x: x[1]):
        print(f"  {cat:25s} {total:>10.0f}")

    print("\n=== MONTHLY TREND ===")
    for m, t in monthly_trend(rows).items():
        print(f"  {m}: {t:>8.0f}")

    dupes = find_duplicates(rows)
    if dupes:
        print("\n=== DUPLICATE PAYMENTS ===")
        for (date, desc, amt), entries in dupes:
            print(f"  {date}  {desc:40s}  {amt:>8.0f}  x{len(entries)}")

    recurring = find_recurring(rows)
    print("\n=== RECURRING CHARGES (3+ months) ===")
    for (desc, amt), months in sorted(recurring.items(), key=lambda x: -abs(x[0][1])):
        print(f"  {desc:40s} {amt:>8.0f}  — {len(months)} months")

    similar_services = find_similar_services(rows)
    if similar_services:
        print("\n=== SIMILAR SERVICES (possible overlap) ===")
        for a, b in similar_services:
            print(f"  \"{a}\"  ↔  \"{b}\"")

    recent = find_recent_subs(rows)
    print("\n=== SUBSCRIPTIONS OVERVIEW ===")
    for name, count, total, first in recent:
        label = "NEW" if first >= q2_cutoff else "  "
        print(f"  [{label}] {name:35s} {count:>2}x  total: {total:>7.0f}  (since {first})")

    anomalies = find_billing_anomalies(rows)

    print()

    has_leaks = (
        bool(dupes)
        or any(first >= q2_cutoff for _, _, _, first in recent)
        or bool(similar_services)
        or bool(anomalies)
    )

    if has_leaks:
        print("=" * 60)
        print("LEAKS AND ANOMALIES — review / action required")
        print("=" * 60)

    for (date, desc, amt), entries in dupes:
        print(f"  • DUPLICATE CHARGE: \"{desc}\" charged {amt:.0f} x{len(entries)} on {date} — you paid {abs(amt)*(len(entries)):.0f} instead of {abs(amt):.0f}")

    for a in anomalies:
        if a["type"] == "extra_charge":
            print(f"  • EXTRA CHARGE: \"{a['desc']}\" charged {a['count']}x in {a['month']} (normally {a['expected']}x/mo) — total {abs(a['total']):.0f}")
        elif a["type"] == "gap":
            print(f"  • GAP: \"{a['desc']}\" stopped after {a['gap_start']}, restarted {a['gap_end']} — dormant {len(a['gap_months'])} month(s)")

    for name, count, total, first in recent:
        if first >= q2_cutoff:
            print(f"  • NEW SUB: \"{name}\" started {first} — {abs(total):.0f} so far. Still needed?")

    for a, b in similar_services:
        a_total = sum(r["amount"] for r in rows if r["desc"] == a)
        b_total = sum(r["amount"] for r in rows if r["desc"] == b)
        print(f"  • OVERLAP: \"{a}\" ({abs(a_total):.0f}) and \"{b}\" ({abs(b_total):.0f}) may be duplicate services")

    if not has_leaks:
        print("  No leaks found — every charge looks intentional.")

    print()

if __name__ == "__main__":
    main()
