# Task 2 — AI Generated Snake Game

**Deployed Game:** https://tariqjamil-bwp.github.io/Pana-101-P011/Assignment2/Task2_Snake_Game/
**GitHub Repo:** https://github.com/tariqjamil-bwp/Pana-101-P011
**Submission:** Assignment 2 — Panaversity Pana-101-P011

---

## Prompt Iterations

### Iteration 1 — Initial Version (`snake_v1.html`)
**Model:** DeepSeek V3.2
**Prompt technique:** Goal / Input / Output pattern (Lab Exercise 9)

> Build me a Snake Game in a single HTML file with embedded CSS and JavaScript.
> Goal: Classic Snake game where the player controls a snake to eat food and grow.
> Input: Arrow keys to control direction. Space to restart after game over.
> Output: A canvas-based game with score display, game over screen, and restart functionality.
> Rules: Snake starts center, food spawns randomly, eating increases score and length,
> game ends on wall/self collision, dark retro theme.

**What worked well:**
- Generated a complete, working 416-line HTML file on first try
- Canvas rendering, grid-based movement, arrow key controls all functional
- Dark retro theme with green accents looked good
- Score display and game over screen worked

**What did not work:**
- Restart was click-based instead of Space key (prompt said Space but model used click button)
- No speed increase — game stayed at same speed forever
- No high score tracking
- Simple square for food, not styled
- Visual design felt very basic ("kiddish" look)

**Prompt improvements for next iteration:** Made each feature request specific and numbered; included the full current code so the model could make surgical changes.

---

### Iteration 2 — Feature Enhancements (`snake_v2.html`)
**Model:** DeepSeek V3.2
**Prompt technique:** Provide existing code + specific numbered change requests

> [Provided full `snake_v1.html` code]
> Changes needed:
> 1. Fix restart: SPACE key to restart (was click-only)
> 2. Add speed increase every 5 food eaten (min 60ms)
> 3. Show current speed level
> 4. Add session high score
> 5. Red apple emoji style food (red circle with green leaf)
> 6. Keep dark retro theme

**What worked well:**
- Space restart now works correctly
- Speed increases every 5 food eaten, displayed as Speed Level
- High score persists during session, shown on game over
- Apple food drawn with red circle and green leaf using canvas arc/shapes
- Model preserved all existing features while adding new ones

**What did not work:**
- No pause functionality
- No mobile support
- No wall wrapping (game over on wall hit)
- No sound effects
- Game still looked plain and unpolished

**Prompt improvements for next iteration:** Continued providing full code context; grouped related features together.

---

### Iteration 3 — Polish & Mobile (`snake_v3.html`)
**Model:** DeepSeek V3.2
**Prompt technique:** Existing code + grouped feature requests

> [Provided full `snake_v2.html` code]
> NEW changes needed:
> 1. P key to pause/unpause with "PAUSED" overlay text
> 2. Mobile touch/swipe controls
> 3. Wall wrapping mode (snake wraps to opposite side)
> 4. Subtle grid pattern on canvas for retro feel
> 5. Ensure SPACE restart works on game over
> 6. Sound effects via Web Audio API (short beep on eat, low tone on game over)

**What worked well:**
- Pause/unpause with P key and overlay works perfectly
- Touch/swipe controls work on mobile browsers
- Wall wrapping makes the game more forgiving and fun
- Grid pattern added subtle retro aesthetic
- Web Audio API sounds work (beep on eat, tone on game over)
- All previous features preserved

**What did not work:**
- Audio requires a user interaction first (browser autoplay policy) — first tap/click initializes it
- Touch controls can be slightly sensitive on very quick swipes
- Visual design still felt dated and amateurish — not suitable for a portfolio

---

### Iteration 4 — Complete Professional Redesign (`index.html`, Built with opencode)

**Approach change:** The three AI-generated versions produced functional but visually unappealing games. Instead of continuing to prompt the AI for visual improvements (which yielded incremental changes at best), the game was rewritten entirely from scratch with a modern, professional design — built entirely through opencode, an AI-native CLI coding tool. Each feature was developed interactively: describing the desired UI/behavior, reviewing the generated code, and iterating until the result matched the vision.

**Design Decisions:**
- **Glassmorphism UI:** Translucent panels with `backdrop-filter: blur()` and subtle borders instead of solid color blocks
- **Gradient background:** Dark purple-blue space theme (`#0f0c29` → `#302b63` → `#24243e`)
- **3 Lives system:** Heart icons (❤) that dim on each life lost, giving the player multiple chances
- **Particle effects:** Burst particles on eating (gold) and on death (red), with gravity and fade
- **Gradient snake body:** Smooth HSL gradient from blue head to teal tail
- **Head glow:** CSS-like shadow glow on the snake's head segment
- **Pupil eyes:** White eyes with dark pupils that shift slightly in the direction of movement
- **Animated mouth:** V-shaped mouth on the leading face that opens wider when near food
- **Golden food:** Radial gradient with glow effect instead of flat red apple
- **Multiple controls:** Arrow keys + WASD + on-screen D-pad + touch swipe
- **Sound design:** Eat double-beep (two quick sine tones), life-lost triangle tone, death sawtooth
- **localStorage:** High score persists across browser sessions
- **Run/Stop toggle:** Button with animated snake SVG icon to start and stop the game
- **Responsive:** CSS `aspect-ratio: 1/1` on canvas container, mobile-friendly touch targets

**What worked well:**
- Complete visual transformation — from retro/basic to modern/professional
- Particle effects added satisfying juice to eating and death
- Lives system made the game more forgiving and fun
- D-pad + swipe made mobile controls intuitive
- All sounds use Web Audio API oscillators (no audio files needed)
- Glassmorphism UI looks polished on both desktop and mobile

**What did not work:**
- Web Audio requires first user interaction (click/touch) before AudioContext creation — handled via one-time `initAudio()` on first interaction
- Canvas does not scale proportionally on very small screens without explicit aspect-ratio CSS

---

## Prompt Logs

All prompts are documented in separate files:
- `prompt_log_v1.txt` — Initial game generation prompt
- `prompt_log_v2.txt` — Feature enhancement changes
- `prompt_log_v3.txt` — Polish, mobile, and final redesign notes

---

## Challenges Faced

1. **Prompt specificity matters** — Iteration 1 missed the Space restart because the prompt listed it among other rules instead of emphasizing it. In Iteration 2, explicitly calling it out as a numbered fix worked.

2. **AI visual design limitations** — The AI consistently produced flat, dated visual designs regardless of how the prompt was phrased. The final version was hand-crafted after three AI iterations failed to achieve a professional look.

3. **Providing existing code** — For iterations 2 and 3, including the full current code in the prompt was essential. The model needed to see the complete context to make surgical changes without breaking anything.

4. **Browser audio policy** — The Web Audio API requires a user gesture before creating an AudioContext. The workaround was to initialize audio on the first keyboard/touch interaction.

5. **Touch controls sensitivity** — Swipe detection needed a minimum distance threshold to avoid accidental direction changes. Implemented with a 20px dead zone.

6. **GitHub Pages deployment** — Jekyll was interfering with the deployment. Added `.nojekyll` file in the repo root to bypass Jekyll processing.

---

## Prompt Engineering Techniques Used

| Technique | Where Applied |
|---|---|
| **Goal / Input / Output pattern** | Iteration 1 — structured the initial request to get a working game first try |
| **Full-code context prompting** | Iterations 2-3 — provided entire existing code so the model made surgical changes without breaking features |
| **Numbered change requests** | Iterations 2-3 — each feature listed as a specific, testable item rather than vague goals |
| **Iterative refinement loop** | Iterations 1→2→3→4 — each cycle built on the previous, with prompt improvements between rounds |
| **Visual design ceiling recognition** | Iteration 4 — recognized when AI output hit its quality limit and switched to hand-crafted code with AI-assisted suggestions |
| **Interactive feature development** | Iteration 4 — used opencode's conversational loop to describe UI/behavior and review generated code in real time |

---

## Learnings

1. **AI is great for rapid prototyping but hits a visual ceiling** — The first three AI iterations were functionally complete but visually unappealing. The biggest improvement came from recognizing this ceiling and hand-crafting the final version.

2. **Full-context prompting prevents regressions** — When asking the AI to add features to existing code, including the entire current file in the prompt ensured no existing features broke.

3. **Specificity beats creativity** — Numbered, testable change requests produced reliable results. Vague requests like "make it look better" produced unpredictable, often worse, outcomes.

4. **Prompt engineering is an iterative skill** — Each iteration taught something new about how to structure requests, what context to provide, and when to use a different approach.

5. **Tool choice matters** — Using opencode for the final version enabled a natural-language, conversational development flow that was faster and more precise than traditional prompting for visual/UI work.

6. **Deployment infrastructure matters** — GitHub Pages required a `.nojekyll` file to bypass Jekyll processing. Small platform-specific details can block delivery if not anticipated.

---

## What Improved the Final Output

- **Iterative prompting** — Each iteration built on the previous one without regressions
- **Providing full context** — Including the entire current code in each iteration prompt ensured the model didn't hallucinate or break existing features
- **Specific, actionable requests** — Instead of "make it better," each change was a concrete, testable requirement
- **Knowing when to stop prompting** — The biggest improvement came from recognizing the AI's visual design ceiling and hand-crafting the final version, using the AI only for targeted feature suggestions and code review

---

## Final Game Features

| Feature | Description |
|---|---|
| Core gameplay | Classic Snake with grid-based movement |
| Controls | Arrow keys, WASD, on-screen D-pad, touch swipe |
| Lives | 3 lives with heart indicators |
| Speed | Gradual speed increase as score grows |
| Scoring | Score + persistent high score (localStorage) |
| Particles | Burst effects on eat and death |
| Sound | Web Audio API (eat, life lost, death) |
| Pause | P key with overlay |
| Run/Stop | Toggle button to start/stop anytime |
| Mouth animation | Head mouth opens wider near food |
| Visual style | Glassmorphism, gradient background, glow effects |
| Responsive | Works on desktop and mobile |
| Deployment | GitHub Pages via course repo |
