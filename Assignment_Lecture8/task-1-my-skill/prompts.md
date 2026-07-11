# Prompts Used — Task 1: Email Reply Drafter Skill

## Initial Prompt (for skill-creator)

Copy this into Claude.ai with the skill-creator skill enabled:

```
Use the skill-creator skill to help me build a skill.

The skill drafts email replies in my personal writing style. I use
a friendly-but-professional tone — warm and personable, but never
slangy or overly casual.

Whenever I say something like "draft a reply to [person] about
[topic]" or "reply to this email" or "write back to [name]", the
skill should:

1. Greet the recipient appropriately based on our relationship
   (colleague vs client vs manager vs friend).

2. Open with a brief context sentence acknowledging their message
   ("Thanks for your note about...", "Good to hear from you...").

3. Address the key points from their message in a clear, friendly
   tone — use paragraph form, not bullets.

4. End with a clear next step or call to action ("Let me know what
   you think", "I'll follow up on Friday", "Please send over the
   document when you have a moment").

5. Close with a professional sign-off ("Best regards", "Thanks",
   "Looking forward to hearing from you") and my name.

Rules to always follow:
- Spell check and grammar check before outputting.
- Keep paragraphs short (2-4 sentences max).
- Never use exclamation marks.
- If the recipient is a client or external partner, lean more
  formal. If it's a teammate, lean warmer.
- If I don't specify a recipient relationship, default to
  friendly-professional.
- Never include placeholders like [your name here] — use my
  name (Tariq Jamil) or infer from context.
- If the original email contains urgent/emotional language,
  acknowledge it calmly without matching the tone.

Ask me anything you need, then build it.
```

## Refinement Prompts

*(During testing, the skill was refined via the skill-creator's clarify-and-build loop. The AI asked clarifying questions about tone boundaries, relationship categories, and edge cases before generating the final SKILL.md. No additional refinement prompts were needed after the initial build — the first test output was approved.)*
