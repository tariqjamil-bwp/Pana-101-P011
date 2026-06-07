# AI Prompting Lab — All 13 Concepts
**Exercise Log**
Started: 2026-06-08

---

## Exercise 1: Novice vs Power User
**Same question, two ways. The briefing changes everything.**

### Step A — Novice Prompts (no context)
**"Which phone should I buy?"** — Both models gave generic, questionnaire-style responses.
**"How do I write a good email?"** — Both models gave full-length generic guides.

### Step B — Power-User Prompts (with context)
**Phone (budget $300, kids photos, battery dies, small hands):**
- DeepSeek V3.2: Google Pixel 6a — great camera for moving subjects, compact, good battery.
- Qwen 3 235B: Samsung Galaxy A15 — 5000mAh battery, 50MP camera, manageable size.

**Email (move Friday meeting to Monday, doctor appt, friendly):**
- Both models gave a ready-to-send email with subject line, polite tone, and specific request.

### ✍ Observation
When there is a context, the reply is to the point, and mostly the user gets what he wants in very few prompts.

### Takeaway
AI is like a smart new coworker — it only knows what you tell it.

---

## Exercise 2: Knows vs Guesses
**A confident tone is not the same as a correct answer.**

### Step A — Topics AI knows well
**"Why do onions make you cry?"** — Both models gave confident, accurate scientific answers (syn-propanethial-S-oxide, defense mechanism).
**"CV vs Cover Letter?"** — Both gave clear, accurate distinctions.

### Step B — Topics AI may NOT know
**"News headlines in my city today"** — Both models honestly said they don't have real-time/local access. No guessing.
**"Minimum notice period in my country"** — Both asked for the country and cited general principles rather than making up specific numbers.

### ✍ Observation
Both models handled the uncertainty well — they admitted they didn't have real-time/local data instead of guessing. This shows that adding "if you cannot be sure, say so clearly" makes the AI cautious rather than confidently wrong.

### Takeaway
Always ask "How would the AI even know this?" For recent, local, or private facts, make it search or admit uncertainty.

---

## Exercise 3: The 3 Retrieval Modes
**Steer pretrained / search / research by wording alone.**

### Mode 1 — Pretrained (from memory)
**"Summarize Romeo and Juliet in 4 sentences"** — Both models gave instant, accurate summaries from memory.

### Mode 2 — Web search
**Weather / AI developments** — Neither model had real-time search access via API. Both asked for city on weather, and relied on training data for AI developments.

### Mode 3 — Deep research
**"Remote work impact on productivity — structured report"** — Both produced well-structured reports with comparison tables, 3 key points, and open questions. But all sources were from training data, not live search.

### ✍ Observation
None of the prompts actually made the AI search the web — all answers came from training data. I could tell because the weather prompt resulted in asking for my city rather than fetching it, the AI developments response referenced dates far in the past, and the deep research report used pre-2024 sources without any real-time verification.

### Takeaway
You don't click a mode — your wording picks it. Name your sources and ask for citations to keep web answers honest.

---

## Exercise 4: Context Is Everything
**Brief it like a colleague — load context up front.**

### Daily — Dinner planning
Both models gave 3 specific meal options using chicken, rice, onions, and yogurt — no extra commentary, exactly as requested.

### Work — Team status update
Both gave concise 4-line bullet updates, friendly tone, highlighting the survey completion and pending tasks.

### ✍ Observation
The "What I want back" specification shaped the output format the most — without it, the AI tends to add extra commentary and explanations. Telling it exactly what structure to return made the answers concise and immediately useful.

### Takeaway
Five lines of good context beats five paragraphs of clever wording. When the topic changes, start a new chat.

---

## Exercise 5: Think Hard
**Invoke reasoning mode for structured output.**

### Without "Think Hard" (Daily)
Both models gave broad advice covering ergonomics, lighting, organization — many options but scattered.

### With "Think Hard" (Daily)
Both gave 3 prioritized upgrades with reasoning, a clear "do this first" justification, and a specific "what NOT to waste money on."

### With "Think Hard" (Work)
Both reasoned through job offer trade-offs against the user's values (learning, family time), with conditions for when the answer flips.

### ✍ Observation
"Think hard" produced a more deliberate, prioritized answer. Without it, the AI gave a broad list of options. With it, the AI reasoned about trade-offs, identified the single most important first step, and explicitly called out what to avoid — which was far more useful for decision-making.

### Takeaway
Save thinking mode for multi-trade-off questions you would want a human to take their time on — not quick lookups.

---

## Exercise 6: Stop the Flattery
**Notice how leading questions make AI agree with you.**

### Step A — Bait Prompts
**"Don't you think mornings are obviously the best time to exercise?"** — Both models initially acknowledged the morning case but then balanced it with evening benefits.
**"Don't you agree WFH is clearly better?"** — Both gave balanced pros/cons rather than fully agreeing.

### Step B — Neutral Prompts
**"Compare morning vs evening. Don't tell me which to pick."** — Pure side-by-side, no slant.
**"Compare WFH vs office. Strongest arguments for each."** — Thoroughly balanced.

### ✍ Observation
Step B gave reasons I had not consciously considered — like evening exercise aligning with peak body temperature for better physical performance, and the "geographic freedom" argument for remote work opening up a wider talent pool regardless of location. The neutral framing made the AI explore both sides genuinely rather than reinforcing my implied bias.

### Takeaway
Verbs like find, prove, defend, confirm hand the AI your answer. Use compare, evaluate, list both sides instead.

---

## Exercise 7: The Brainstorm–Iterate Loop
**Never accept the first answer. The value is in the back-and-forth.**

### Round 1 — Options
Both models gave 5 one-line ideas (hobbies / email versions) — quick and unrefined.

### Round 2 — Feedback
After saying "I like option 1 but want it more physically active" / "I like version 2 but want it warmer," both models generated 5 new, more targeted options.

### Round 3 — Expand Winner
The chosen idea was expanded into a full actionable plan (weekly stretching routine / polished email with closing line).

### ✍ Observation
Yes — the final idea was much better than Round 1. Round 1 gave one-line ideas too abstract to act on. The iteration narrowed it to what I actually wanted (physically active, no materials), and the final expanded plan gave a concrete day-by-day routine I could follow immediately. The value was in the back-and-forth, not the first answer.

### Takeaway
Load context → ask for options → give feedback → repeat → expand. The value isn't the first answer; it is the loop.

---

## Exercise 13: Models Checking Models
**Get honest feedback from two different models on the same draft.**

### Scoring the AI Prompting Course Draft
| Criteria | DeepSeek V3.2 | Qwen 3 235B |
|---|---|---|
| Clarity | 9/10 | 9/10 |
| Structure | 7/10 | 8/10 |
| Evidence | 5/10 | 5/10 |
| What's Missing | Low purpose/audience | No concrete examples |
| Single Best Fix | Add specific example of improved task | Add example with measurable result |

### ✍ Observation
Both models agreed on the draft's strengths (clear, logical) and its main weakness (no evidence). The single change they both recommended was the same: add a concrete example. This shows that using AI to review your work can give consistent, useful feedback — and when two independent models flag the same issue, you can trust it is a real problem worth fixing.

### Takeaway
Use models to check each other for better feedback.

---

## Exercise 8: Multimodal — Image & Audio
**Practice handing AI something that is not text. (Bonus only — no image upload via API.)**

### Bonus — Image Generation Prompt
Both models wrote detailed, structured image prompts for "a cozy watercolor illustration of a cat reading a book by a window" — specifying style, color palette, lighting, composition, and greeting-card layout.

### ✍ Observation
The AI produced highly specific, usable image prompts with technical detail (watercolor texture, paper grain, warm amber and cream palette, space for greeting card text). The prompts were complete enough to paste directly into Midjourney or DALL-E.

### Takeaway
AI does the boring 90% so you focus on the careful 10%.

---

## Exercise 9: Build a Small App
**Use Goal / Input / Output shape to build working code.**

### Round 1 — Tip Calculator
DeepSeek generated a complete HTML/CSS/JS tip calculator with bill input, tip % selection, people count, and results display. Included pre-set tip buttons (10%-30%), gradient header, and responsive design.

### Round 2 — Iterate
DeepSeek updated the theme to calm blue (#3b82f6), increased button sizes, added a reset button, improved error validation, and added fade-in animation for results.

### ✍ Observation
Yes, it worked first try — the AI produced a complete HTML document with all requested features. In the iterate step, I changed the color theme from gradient to calm blue, increased button sizes, and added a dedicated reset button plus error validation — all while the AI preserved the existing structure and just modified the UI elements.

### Takeaway
The skill isn't coding — it is writing a clear brief (Goal / Input / Output) and iterating. Small one-screen tools work great.

---

## Exercise 10: Data Analysis
**Learn to make the AI actually run code — and verify that it did.**

### Round 1 — The Trap (no code mention)
DeepSeek calculated median (65.5), average (~61.61), and outliers (none) by manual step-by-step arithmetic — no code was run.

### Round 2 — Force code
DeepSeek wrote complete Python code using numpy for calculations, but could not execute it (no code sandbox via API).

### ✍ Observation
Round 1 did not run code — it calculated manually step by step. I could tell because there was no code block, just arithmetic written out in text. The numbers were correct but the method was unreliable. Round 2 generated actual Python code but could not execute it — in a tool with code execution (like ChatGPT Code Interpreter), the code would actually run and show verified output.

### Takeaway
Always say "write and run code, show me the code." No code block = it probably guessed.

---

## Exercise 11: Desktop Apps & Permissions
**Practice the "plan, don't act" habit.**

### Safe Workflow
DeepSeek proposed a 12-step safe workflow: backup → inventory → propose structure → get approval → work on copies → verify integrity → archive originals.

### 3 Things to NEVER Allow
1. Permanently delete originals without explicit consent
2. Auto-rename files using AI guesses
3. Process files outside the designated folder

### ✍ Observation
I would never grant an AI app permission to delete files or modify originals without a confirmed backup first. Deleted files often skip the recycle bin when an AI tool handles them, and once they are gone, there is no recovery.

### Takeaway
Deleted files often skip the recycle bin; edits overwrite. Scope permissions tight; grow them with track record, not trust in the brand.

---

## Exercise 12: Which Model When
**Same prompt, two different models — compare the difference.**

### Daily — Saturday Plan
- **DeepSeek V3.2:** Themed narrative ("Slow City Living"), flowing prose, poetic tone
- **Qwen 3 235B:** Structured timed blocks, bullet points, cost estimates included

### Work — LinkedIn Post
- **DeepSeek V3.2:** Short, punchy, hashtag-heavy, direct
- **Qwen 3 235B:** More reflective, warmer tone, slightly longer

### ✍ Observation
DeepSeek's answers felt more concise and direct, while Qwen was more structured and thorough. DeepSeek gave the Saturday plan as a flowing narrative with a theme, while Qwen broke it into timed blocks with cost notes. For the LinkedIn post, DeepSeek was punchier and more hashtag-heavy, while Qwen was warmer and more reflective. This shows that model choice affects tone and structure even with the same prompt.

---

## Conclusion — Overall Learnings

### What I Learned from the Lab
The lab taught that AI prompting is fundamentally about context management. The single rule — "get the right context in, keep the wrong context out" — played out across all 13 exercises. AI is like a smart new coworker: it only knows what you tell it, and it sounds confident even when unsure.

### How My Prompting Improved
I started with vague, no-context questions and progressively learned to:
- Provide structured context upfront (Exercise 4 template)
- Specify exact output format ("What I want back")
- Use "think hard" for complex decisions
- Frame questions neutrally instead of leading the AI
- Iterate through feedback loops instead of accepting the first answer
- Force code execution and verify results

### Most Helpful Techniques
1. **The Context Template** (Exercise 4) — "I need help with... Here is what you need to know... What I want back" was the single most impactful format.
2. **The Brainstorm–Iterate Loop** (Exercise 7) — Never accept the first answer; the value is in the back-and-forth.
3. **Neutral Framing** (Exercise 6) — Using "compare/evaluate/list both sides" instead of leading verbs like "prove/defend."
4. **Think Hard** (Exercise 5) — Essential for multi-trade-off decisions.
5. **Model Cross-Checking** (Exercises 12-13) — Running the same prompt on different models reveals blind spots and gives better feedback.

### Challenges Faced
- **No web search via API** — The models could not actually search the web; all answers came from training data. In a real scenario with ChatGPT/Claude web search, this would work differently.
- **No code execution** — The API could generate code but not run it. A tool with Code Interpreter would execute and verify.
- **No image input** — Exercise 8's transcription task required a photo upload which the API does not support.
- **Model differences** — DeepSeek and Qwen produced different tones and structures for the same prompts, which was useful for comparison but meant results were not perfectly consistent.
