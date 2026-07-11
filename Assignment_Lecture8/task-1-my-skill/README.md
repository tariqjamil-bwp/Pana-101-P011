# Task 1 — Email Reply Drafter Skill

**What it does:** Takes an incoming email (or a description of one) and drafts a reply in my personal writing style — friendly but professional, with a clear Greeting → Context → Action → Close structure.

**Why I chose this:** I send professional emails regularly and find myself rethinking the tone and structure each time. This Skill saves that mental overhead and keeps my replies consistent.

## AI Tools Used

- **Claude.ai** — skill-creator to generate the SKILL.md, testing in fresh chats

## How It Was Built

1. Drafted a detailed prompt describing my tone, structure rules, and edge cases
2. Ran the prompt with skill-creator in Claude.ai
3. Answered clarifying questions from the AI
4. Saved the generated SKILL.md
5. Tested in a fresh chat with natural language triggers
6. Refined based on test results

## Verification

| Test | Input | Result |
|------|-------|--------|
| Auto-trigger | "Draft a reply to a client asking about the Q3 report deadline" | ✅ Skill fired automatically |
| Tone check — Vendor | VPS renewal email from Sarah (vendor/support) | ✅ Leaned formal-but-warm, user approved |
| Tone check — Client | Client asking about Q3 progress | ✅ Engaged correctly, asked for actual email before drafting |
| Gmail integration | Asked to find email thread via Gmail connector | ✅ Searched Gmail instead of asking user to paste |

## Test Results

### Test 1 — Vendor/Support Email

**Original email:** VPS renewal notice from Sarah

**Skill response:** Drafted a reply acknowledging the renewal, agreeing to top up, and requesting plan comparison details — formal-but-warm tone appropriate for a vendor relationship.

**Verdict:** ✅ Approved by user ("looks great")

### Test 2 — Client Progress Inquiry

**Original email:** Client checking on Q3 report progress

**Skill response:** Asked for the actual email text (per Step 1 rule) before drafting — correctly following the skill's precision-first instruction. When given context, produced a structured status update with clear next steps.

**Verdict:** ✅ Skill rules followed correctly

## Screenshots

*(To be added — test results captured in Claude.ai)*

## Files

- `SKILL.md` — the Skill file
- `prompts.md` — full prompt history (initial + refinements)
- `screenshot.png` — proof of auto-triggering
