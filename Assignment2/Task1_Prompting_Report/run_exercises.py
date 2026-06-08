#!/usr/bin/env python3
"""
Panaversity Assignment 2 - Task 1
AI Prompting Lab — All 13 Concepts
Runs all exercises against DeepSeek V3.2 and Qwen 3 235B A22B via OpenRouter.
"""

import os
import json
import sys
from datetime import datetime
from openai import OpenAI

# ── API Key from .bashrc ────────────────────────────────────────────────────
bashrc = os.path.expanduser("~/.bashrc")
API_KEY = os.environ.get("OPENROUTER_API_KEY_tj")
if not API_KEY and os.path.exists(bashrc):
    for line in open(bashrc):
        if "OPENROUTER_API_KEY_tj" in line:
            parts = line.strip().split("=", 1)
            if len(parts) == 2:
                API_KEY = parts[1].strip().strip('"').strip("'")
if not API_KEY:
    print("ERROR: OPENROUTER_API_KEY_tj not found")
    sys.exit(1)

MODEL_A = "deepseek/deepseek-v3.2"
MODEL_B = "qwen/qwen3-235b-a22b"
REPORT_FILE = "exercise_results.md"


def call_model(model, messages):
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)
        resp = client.chat.completions.create(
            model=model, messages=messages, max_tokens=4096, temperature=0.7,
        )
        return resp.choices[0].message.content or "[empty]"
    except Exception as e:
        return f"[ERROR: {e}]"


def run_exercise(number, title, description, prompts_a, prompts_b=None):
    lines = []
    lines.append(f"\n\n## Exercise {number}: {title}")
    lines.append(f"\n**{description}**\n")
    if prompts_b is None:
        prompts_b = prompts_a

    lines.append(f"\n### 🤖 Model A: DeepSeek V3.2\n")
    for p in prompts_a:
        step = p.get("step", "")
        lines.append(f"\n**{step}**\n> {p['prompt']}\n")
        print(f"  [DS] Ex{number} - {step[:30]}...", end=" ", flush=True)
        resp = call_model(MODEL_A, [{"role":"system","content":p.get("system","You are a helpful AI assistant.")}, {"role":"user","content":p["prompt"]}])
        lines.append(f"\n```\n{resp}\n```\n")
        print("OK")

    lines.append(f"\n### 🤖 Model B: Qwen 3 235B A22B\n")
    for p in prompts_b:
        step = p.get("step", "")
        lines.append(f"\n**{step}**\n> {p['prompt']}\n")
        print(f"  [QW] Ex{number} - {step[:30]}...", end=" ", flush=True)
        resp = call_model(MODEL_B, [{"role":"system","content":p.get("system","You are a helpful AI assistant.")}, {"role":"user","content":p["prompt"]}])
        lines.append(f"\n```\n{resp}\n```\n")
        print("OK")

    lines.append(f"\n---\n### ✍ Your Observation\n*What was different between the two answers?*\n\n[OBSERVATION]\n")
    return "\n".join(lines)


def main():
    header = f"""# AI Prompting Lab — All 13 Concepts
**Exercise Log**
Ran on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Models: {MODEL_A} vs {MODEL_B}

---"""
    results = [header]

    # === PART 1: How AI knows things ===
    results.append(run_exercise(1, "Novice vs Power User",
        "Same question, two ways. The briefing changes everything.", [
        {"step":"Step A — Novice (Daily)","prompt":"Which phone should I buy?"},
        {"step":"Step A — Novice (Work)","prompt":"How do I write a good email?"},
        {"step":"Step B — Power (Daily)","prompt":"Help me choose a phone. Context: my budget is about $300, I mostly take photos of my kids and use WhatsApp, my current phone's battery dies by 3pm, and I find big phones hard to hold. Give me 3 options with a one-line reason for each, then tell me which you'd pick and why."},
        {"step":"Step B — Power (Work)","prompt":"Help me write an email. Context: I need to ask my manager to move our Friday team meeting to Monday because I have a doctor's appointment. We have a friendly working relationship. Keep it short and polite. Give me the email, ready to send."},
    ]))

    results.append(run_exercise(2, "Knows vs Guesses",
        "A confident tone is not the same as a correct answer.", [
        {"step":"Step A — Knows (Daily)","prompt":"Why do onions make you cry when you cut them? Answer in 2 short paragraphs."},
        {"step":"Step A — Knows (Work)","prompt":"What is the difference between a CV and a cover letter? Keep it short."},
        {"step":"Step B — May NOT know (Daily)","prompt":"What were the main news headlines in my city today? If you cannot be sure, say so clearly instead of guessing."},
        {"step":"Step B — May NOT know (Work)","prompt":"What is the current minimum notice period an employer must give before changing an employee's contract in my country? Be specific. If you are not sure this is current, say so instead of guessing."},
    ]))

    results.append(run_exercise(3, "The 3 Retrieval Modes",
        "Steer pretrained / search / research by wording alone.", [
        {"step":"Mode 1 — Pretrained (Daily)","prompt":"Summarize the plot of Romeo and Juliet in 4 sentences.","system":"You are a helpful AI assistant."},
        {"step":"Mode 2 — Web search (Daily)","prompt":"What's the weather forecast for my city this weekend? Use a current source and cite it.","system":"You are a helpful AI assistant with web search."},
        {"step":"Mode 2 — Web search (Work)","prompt":"What are the latest developments this month in artificial intelligence? Cite each claim, and mark anything you can't support as 'unverified'.","system":"You are a helpful AI assistant with web search."},
        {"step":"Mode 3 — Deep research (Work)","prompt":"Research the impact of remote work on employee productivity thoroughly. Use reputable sources only (government sites, peer-reviewed studies, official reports — not forums). Produce a structured report with: (1) the 3 most important points, (2) a comparison table, (3) 3 open questions. Cite sources.","system":"You are a helpful AI assistant with web search and deep research."},
    ]))

    # === PART 2: Talking to AI well ===
    results.append(run_exercise(4, "Context Is Everything",
        "Brief it like a colleague — load context up front.", [
        {"step":"Template (Daily)","prompt":"I need help planning dinner for tonight.\nHere is what you need to know:\n- I have chicken, rice, onions, and yogurt in the kitchen\n- I have only 30 minutes\n- One person at the table doesn't eat spicy food\nWhat I want back: 3 simple meal options, no commentary."},
        {"step":"Template (Work)","prompt":"I need help writing a short update for my team.\nHere is what you need to know:\n- We finished the customer survey this week\n- 2 tasks are still pending (the report and the slides)\n- The reader is my team, who like quick bullet points\nWhat I want back: a 4-line status update, friendly tone."},
    ]))

    results.append(run_exercise(5, "Think Hard",
        "Invoke reasoning mode for structured output.", [
        {"step":"Without think hard (Daily)","prompt":"I have $200 to improve my home office and I work from home full time. Give me your best advice."},
        {"step":"With think hard (Daily)","prompt":"I have $200 to improve my home office and I work from home full time. Think hard before answering. Then give me: 1) the 3 upgrades with the biggest impact on comfort and focus, 2) which one you'd do first and why, 3) one thing I should NOT waste money on.","system":"You are a helpful AI assistant. Think hard before each response."},
        {"step":"Think hard (Work)","prompt":"I'm choosing between two job offers. Offer A: higher pay, longer commute, less interesting work. Offer B: lower pay, remote, steeper learning curve. I value learning and time with family. Think hard. Then tell me: 1) the 3 trade-offs that actually matter for me, 2) which you'd pick and why, 3) under what conditions your answer flips.","system":"You are a helpful AI assistant. Think hard before each response."},
    ]))

    results.append(run_exercise(6, "Stop the Flattery",
        "Notice how leading questions make AI agree with you.", [
        {"step":"Step A — Bait (Daily)","prompt":"Don't you think mornings are obviously the best time to exercise?"},
        {"step":"Step A — Bait (Work)","prompt":"Don't you agree that working from home is clearly better than the office?"},
        {"step":"Step B — Neutral (Daily)","prompt":"Compare exercising in the morning versus the evening. List the strongest case for each, and what kind of person each option suits best. Don't tell me which to pick."},
        {"step":"Step B — Neutral (Work)","prompt":"Compare working from home versus working in the office. List the strongest arguments for each. Don't tell me which is better."},
    ]))

    results.append(run_exercise(7, "The Brainstorm–Iterate Loop",
        "Never accept the first answer. The value is in the back-and-forth.", [
        {"step":"R1 — Options (Daily)","prompt":"I want a small hobby that costs almost no money and that I can do for 15 minutes at home. Give me 5 different ideas, one line each. Don't explain any of them yet."},
        {"step":"R2 — Feedback (Daily)","prompt":"I don't like option 3 because it requires materials I don't have. I like option 1 but I want it to be more physically active. Give me 5 NEW ideas based on this feedback."},
        {"step":"R3 — Expand (Daily)","prompt":"I'll go with bodyweight stretching routine. Give me a simple step-by-step plan to start it this week."},
        {"step":"R1 — Options (Work)","prompt":"I need to write a short message asking a coworker to send me a file they keep forgetting to send. I want to sound friendly, not annoyed. Give me 5 different versions, one or two lines each. Don't explain any of them yet."},
        {"step":"R2 — Feedback (Work)","prompt":"I like version 2 but I want it to be slightly warmer and more personal. Give me 5 NEW versions based on this feedback."},
        {"step":"R3 — Expand (Work)","prompt":"I'll go with version 3 from your second set. Now make it slightly warmer and add a friendly closing line, but keep it under 3 sentences."},
    ]))

    # === PART 3: Beyond text ===
    results.append(run_exercise(8, "Multimodal — Image & Audio",
        "NOTE: Image upload not possible via API. Only generating image prompt.", [
        {"step":"Bonus — Image prompt","prompt":"Write me a detailed image-generation prompt for a cozy, watercolor-style illustration of a cat reading a book by a window, suitable for a greeting card."},
    ]))

    results.append(run_exercise(9, "Build a Small App",
        "Use Goal / Input / Output shape to build working code.", [
        {"step":"Tip Calculator (Daily)","prompt":"Build me a tip calculator.\nGoal: split a bill and add a tip.\nInput: I type the total, the tip %, and the number of people.\nOutput: show the tip amount, the grand total, and each person's share. Make it clean and easy to use. Show me the working HTML/CSS/JS code.","system":"You are a helpful AI assistant. Generate complete, working HTML/CSS/JS code."},
        {"step":"Iterate — Tip Calc","prompt":"Make the buttons bigger and change the color theme to calm blue. Add a reset button. Show me the updated HTML/CSS/JS code.","system":"You are a helpful AI assistant. Generate complete, working HTML/CSS/JS code."},
        {"step":"Timer (Work)","prompt":"Build me a simple countdown timer for focused work.\nGoal: 25-minute work sessions with 5-minute breaks.\nInput: I press start.\nOutput: a large timer counting down, a clear sound when each session ends, and a clean layout. Show me the working HTML/CSS/JS code.","system":"You are a helpful AI assistant. Generate complete, working HTML/CSS/JS code."},
        {"step":"Iterate — Timer","prompt":"Add a reset button and change the color theme to calm blue. Show me the updated HTML/CSS/JS code.","system":"You are a helpful AI assistant. Generate complete, working HTML/CSS/JS code."},
    ]))

    results.append(run_exercise(10, "Data Analysis",
        "Learn to make the AI actually run code — and verify.", [
        {"step":"R1 — The trap","prompt":"Here are 18 numbers: 47, 52, 89, 91, 23, 67, 78, 12, 95, 44, 88, 71, 33, 56, 99, 18, 64, 82. What is the median, the average, and which numbers are outliers? Be specific."},
        {"step":"R2 — Force code","prompt":"Now run that calculation again — but this time write and run code to do it, and show me the code you ran.","system":"You are a helpful AI assistant. Write and execute Python code for calculations."},
        {"step":"Bonus — Strategy","prompt":"What's the best way to ask an AI to analyze a CSV file? What exact wording should I use to make sure it actually runs code and doesn't guess?"},
    ]))

    # === PART 4: Working safely & choosing tools ===
    results.append(run_exercise(11, "Desktop Apps & Permissions",
        "Practice the 'plan, don't act' habit.", [
        {"step":"Safe workflow","prompt":"Imagine you are an AI assistant with permission to reorganize a messy folder of 50 personal files (photos, PDFs, receipts). Before doing anything, write me a step-by-step SAFE workflow you would follow so that nothing is lost or wrongly renamed. Then list 3 things I should NEVER let you do."},
    ]))

    results.append(run_exercise(12, "Which Model When",
        "Same prompt, two different models. (Both answer below.)", [
        {"step":"Daily scenario","prompt":"Plan a relaxing Saturday for someone who works hard all week and lives in a city. Give me a simple hour-by-hour plan from 9am to 9pm, with cheap or free activities."},
        {"step":"Work scenario","prompt":"Write a 100-word LinkedIn post announcing that I finished a course on AI prompting and what I learned. Friendly, not boastful."},
    ]))

    results.append(run_exercise(13, "Models Checking Models",
        "Get honest feedback from two different models on the same draft.", [
        {"step":"Grade this draft","prompt":"Score this draft 1-10 on clarity, structure, evidence, and what's missing — one sentence of reasoning per score. Then tell me the single change that would raise the lowest score the most.\n\nDraft:\nI recently completed a course on AI prompting. It taught me how to communicate with AI more effectively. The key insight was that context matters more than clever wording. I learned to be specific about what I want and to provide relevant background information. This has already improved my productivity significantly. I would recommend this training to anyone who works with AI tools regularly."},
    ]))

    # Write report
    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(results))
    print(f"\n✅ Done! Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
