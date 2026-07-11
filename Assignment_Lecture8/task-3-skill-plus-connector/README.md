# Task 3 — Skill + Connector Together

**What I did:** Wired the Email Reply Drafter Skill and the Gmail Connector into a single workflow — one sentence fetched live data and formatted it automatically.

## The Single Sentence

```
Find the latest email from [someone in your inbox, who may require 
a return response, figure out yourself] and draft a reply using my 
email-reply style.
```

## What Happened

1. **Gmail Connector fired** — searched the inbox, filtered out automated emails (job alerts, newsletters, billing receipts), identified the only human correspondence thread: an exchange with Laiba Rashid at Seeqlo (AI education app) from September 2025.

2. **Claude analyzed the thread** — determined it was a closed thread (last message was Laiba's polite close: "Thank you for your email. No problem at all."), and asked whether to reopen it, look further back, or try something else.

3. **Email Reply Drafter Skill fired** — when instructed to proceed, the skill loaded and produced a reply in Tariq's voice:
   - ✅ Correct tone: formal-but-warm (external partner/business contact)
   - ✅ Correct structure: Greeting → Context → Body → Next Step → Sign-off
   - ✅ Short paragraphs (2-4 sentences)
   - ✅ No exclamation marks
   - ✅ No placeholder text — signed as "Tariq Jamil"
   - ✅ Relationship-appropriate formality

## The Result

**Original thread found:** Laiba Rashid, Seeqlo — Sep 2025 discussion about an AI education app and subscription costs

**Drafted reply (via Skill):**

> Dear Laiba,
>
> I hope you and the Seeqlo team have been doing well. It has been a while since we last spoke about the app, and I wanted to reconnect.
>
> At the time, the subscription cost was a barrier for me to actively pursue market opportunities on Seeqlo's behalf. Since then, I have continued to work in AI education and research, and I would welcome an update on where things stand with Seeqlo, particularly around pricing or partnership options that might work better for exploring the Pakistani market.
>
> If it is still relevant on your end, I would be glad to set up a short call to discuss how I might help going forward. Please let me know what works for you.
>
> Best regards,
> Tariq Jamil

## Verification

| Check | Result |
|-------|--------|
| Connector fetched live data | ✅ Found real Laiba/Seeqlo thread in Gmail |
| Skill fired automatically | ✅ Yes — loaded without being named explicitly |
| Output matches skill rules | ✅ Tone, structure, formality, sign-off all correct |
| Spot-check against source | ✅ Thread content verified — draft accurately references the old discussion |

## Screenshots

*(To be added — the full conversation showing Gmail search + Skill-formatted reply)*
