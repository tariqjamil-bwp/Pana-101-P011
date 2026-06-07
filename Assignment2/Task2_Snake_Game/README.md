# Task 2 — AI Generated Snake Game

**Deployed Game:** https://tariqjamil-bwp.github.io/Pana-101-P011/
**GitHub Repo:** https://github.com/tariqjamil-bwp/Pana-101-P011

---

## Prompt Iterations

### Iteration 1 — Initial Version (`snake_v1.html`)
**Prompt technique:** Goal / Input / Output pattern (from Lab Exercise 9)

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
- Restart was click-based instead of Space key (prompt said Space but model used click)
- No speed increase — game stayed at same speed forever
- No high score tracking
- Simple square for food, not styled

---

### Iteration 2 — Feature Enhancements (`snake_v2.html`)
**Prompt technique:** Provide existing code + specific change requests

> [Provided full current code]
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
- Game area looked slightly plain

---

### Iteration 3 — Polish & Mobile (`snake_v3.html` → `index.html`)
**Prompt technique:** Existing code + new feature requests

> [Provided full current code]
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

---

## Challenges Faced

1. **Prompt specificity matters** — Iteration 1 missed the Space restart because the prompt listed it among other rules instead of emphasizing it. In Iteration 2, explicitly calling it out as a fix worked.

2. **Providing existing code** — For iterations 2 and 3, including the full current code in the prompt was essential. The model needed to see the complete context to make surgical changes without breaking anything.

3. **Browser audio policy** — The Web Audio API requires a user gesture before creating an AudioContext. The workaround was to initialize audio on the first keyboard/touch interaction.

4. **Touch controls sensitivity** — Swipe detection needed a minimum distance threshold to avoid accidental direction changes. The model handled this with `Math.abs(deltaX) > 30` threshold.

---

## What Improved the Final Output

- **Iterative prompting** — Each iteration built on the previous one without regressions
- **Providing full context** — Including the entire current code in each iteration prompt ensured the model didn't hallucinate or break existing features
- **Specific, actionable requests** — Instead of "make it better," each change was a concrete, testable requirement
- **Goal/Input/Output structure** — The initial prompt used the lab's GIO pattern, which produced a working game on first try

## Final Game Features
- Classic Snake gameplay with arrow keys and touch/swipe
- Score, high score, speed level, and food count display
- Speed increases every 5 food eaten
- Pause/Resume with P key
- Wall wrapping mode
- Apple food with leaf design
- Sound effects (eat + game over)
- Grid pattern for retro feel
- Dark arcade theme
- Responsive canvas
