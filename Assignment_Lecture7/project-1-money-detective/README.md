# Project 1: Money Detective

**Problem:** Find hidden spending leaks in personal transaction history — recurring charges, duplicate payments, forgotten subscriptions, and service overlaps.

**AI Tool Used:** Claude (opencode)

## How It Works

The script reads a CSV of transactions (date, description, amount) and:

1. **Verifies** against two known baselines before trusting any findings
2. **Categorizes** spending into custom categories
3. **Finds recurring charges** (3+ months at same amount)
4. **Detects duplicate payments** (same description, same amount, same date)
5. **Flags overlapping services** (similar names, e.g. "Optical Cable TV" vs "Cable TV - Optical")
6. **Identifies new subscriptions** (started in recent months)
7. **Summarizes all leaks** with actionable findings

## Verification

- **Jan total:** -86,050 PKR — matched hand calculation
- **Jan Daraz Grocery total:** -4,300 PKR — matched hand calculation

Both baselines confirmed before findings were trusted.

## Key Findings

| Finding | Amount |
|---------|--------|
| Duplicate SHOQ PTCL charge (Mar 28) | Paid 1,000 instead of 500 |
| Claude Subscription (started Apr) | 16,800 YTD — still needed? |
| Cable TV - Optical vs Optical Cable TV | Possible duplicate service |
| School Fee (6 months) | 51,000 YTD |
| Old Gym Membership (restarted Apr) | 6,000 YTD after dormant Feb |

## Usage

```bash
# Edit transactions.csv with your data, then:
python money_detective.py
```
