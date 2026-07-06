# Prompts Used — Project 1: Money Detective

## Initial Prompt

```
I have a CSV of my personal transactions with columns: Date, Description, Amount.
Write a Python script that:

1. Reads the CSV
2. Categorizes spending into meaningful categories
3. Finds recurring charges (same description, same amount, appearing monthly)
4. Detects duplicate payments (same description, amount, and date)
5. Flags possible forgotten subscriptions
6. Verifies output against a known baseline before trusting findings
7. Prints a clear summary of all leaks found

Categories I care about: Utilities, Groceries, Transport, Subscriptions,
Education, Medical, Dining Out, Fitness, Shopping, Other.
```

## Refinement Prompt 1

```
The script has hardcoded action items that reference old entries
(Spotify, AutoCAD) that no longer exist in my CSV. Make all findings
dynamic — derive them purely from whatever data the CSV contains.
```

## Refinement Prompt 2

```
The "similar services" detection is too noisy — it flags things like
"Claude Subscription" and "Netflix Subscription" just because both
contain the word "Subscription". Fix it to only catch genuine overlaps
where the name words are a subset of each other (e.g. "Cable TV - Optical"
vs "Optical Cable TV").
```

## Final Prompt

```
Add a second verification baseline. The script should check two known
figures (January total and January Daraz total) and only print findings
if both match.
```
