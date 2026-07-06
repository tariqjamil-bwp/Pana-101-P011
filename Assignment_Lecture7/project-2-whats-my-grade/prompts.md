# Prompts Used — Project 2: What's My Grade

## Initial Prompt

```
I have a CSV of my Post Graduate Diploma in DS-AI scores with columns:
Category, Item, Score, Max, Weight.

The program has 5 courses + ISP:
1. Basics of Python
2. Data Visualization
3. Power BI
4. ML
5. DL
6. ISP (Independent Study Project)

Each course has Midterm (40%) and Final Term (60%).
ISP has a single grade.

Write a Python grade calculator that:
1. Reads scores from a CSV
2. Reads grading policy from a separate CSV (category, weight, drop rules)
3. Calculates weighted percentage per course (midterm 40%, final 60%)
4. Shows letter grade (A+, A, A-, B+, B, B-, etc.) and GPA on 4.00 scale
5. Calculates CGPA across all courses
6. Works with any subjects — no hardcoded categories
```

## Refinement Prompts

- "Adopt to my recent post grad diploma grades — 5 courses + ISP"
- "Convert to GPA on 4.00 scale"
- "Scale includes A+, A, A-, B+, B, B- etc."

## Verification

Hand-check: Python = (96×40 + 94×60)/100 = 94.8% → A+ (4.00). Matches.
