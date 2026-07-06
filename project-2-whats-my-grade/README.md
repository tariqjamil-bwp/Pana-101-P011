# Project 2: What's My Grade, Really

**Problem:** Calculate true current grade using a teacher's specific grading rules (weighted categories, dropped lowest scores), and determine what score is needed on the final exam to reach a target grade.

**AI Tool Used:** Claude (opencode)

## Grading Policy

| Category | Weight | Rules |
|----------|--------|-------|
| Assignments | 25% | Drop lowest 1 |
| Quizzes | 15% | Drop lowest 1 |
| Midterm | 20% | — |
| Final Project | 25% | — |
| Final Exam | 15% | — |

## Result

- **Current grade:** 81.5% (B-)
- **To get B (83%):** Need 91.4% on final
- Already secured B- regardless of final exam score

## Verification

Calculated by hand: Assignments (no drop): (90+75+95+70+100+85+60)/7 = 82.1%.
Drop lowest (60): (90+75+95+70+100+85)/6 = 85.8%. Matches.

## Usage

```bash
# Edit scores.csv with your data, then:
python grade_calculator.py
```
