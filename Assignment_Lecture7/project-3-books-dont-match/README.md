# Project 3: The Books Don't Match

**Problem:** Reconcile a hand-counted total against messy digital payment records with inconsistent names, typos, and ambiguous memos.

**AI Tool Used:** Claude (opencode)

## Files

| File | Purpose |
|------|---------|
| `known_totals.csv` | Expected contributions per person (hand-counted) |
| `records.csv` | Raw digital payment records (uncleaned) |
| `rules.json` | Auto-generated name mappings (review before running) |
| `reconcile.py` | Reconciliation script |

## How It Works

1. **Auto-detects column names** — doesn't care what your CSV headers are
2. **Auto-generates rules.json** — matches messy sender names to known contributors using substring + fuzzy matching
3. **Review rules.json** — fix any wrong mappings
4. **Run reconciliation** — finds gap, flags duplicates/shortages/unknowns

## Result

- **Known total:** 124,500 PKR
- **Records total:** 162,500 PKR
- **Gap:** +38,000 PKR

### Follow-ups
- **Ali Raza** — paid twice (ali raza + ali r.), over by 15,000
- **Usman Khan** — paid twice (usman k + usman123), over by 18,000
- **Hassan Mirza** — short by 10,000
- **ANAS** — 15,000 from unknown sender

## Verification

Known total hand-counted before running. Gap = 38,000 = 15,000 (Ali dup) + 18,000 (Usman dup) + 15,000 (Anas) - 10,000 (Hassan short).

## Usage

```bash
# First run auto-generates rules.json:
python reconcile.py

# Review rules.json, then:
python reconcile.py
```
