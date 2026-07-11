# Lecture 8 — Skills & Connectors

**Student:** Tariq Jamil
**Course:** Pana-101-P011
**Topic:** Teach AI Once, Connect It to Your Apps

## Projects Overview

| Task | Project | Description | Status |
|------|---------|-------------|--------|
| 1 | Email Reply Drafter Skill | Builds a reusable Skill that drafts email replies in my personal tone — friendly but professional, with a clear Greeting → Context → Body → Next Step → Sign-off structure | ✅ Complete |
| 2 | Connect Gmail (Read-Only) | Connects Gmail to Claude.ai via the Connectors directory with read-only permission — can search and read emails but cannot send, delete, or modify | ✅ Complete |
| 3 | Skill + Connector | Wires the Email Reply Drafter Skill and Gmail Connector into one workflow — a single sentence fetches live email data and formats a reply automatically | ✅ Complete |
| 4 | Portable / Handoff | Loads the Skill into Claude Code (CLI) — a second surface — and confirms it works without re-explanation, including Gmail connector integration | ✅ Complete |
| 5 | Skill Audit | Audits the MCP Server Development Guide from the official directory — assesses safety, credential handling, data flow, and external connections | ✅ Complete |

## AI Tools Used

- **Claude.ai (web)** — skill-creator to build the Skill, Gmail connector setup, testing, skill audit
- **Claude Code (CLI)** — portability test (Task 4)
- **opencode** — project scaffolding and documentation

## Repository Structure

```
Assignment_Lecture8/
├── README.md                           # This file
├── task-1-my-skill/
│   ├── SKILL.md                        # The Email Reply Drafter Skill
│   ├── README.md                       # What it does, tests, verification
│   ├── prompts.md                      # Full prompt history
│   └── screenshot.png                  # [Pending] Proof of auto-triggering
├── task-2-connect-app/
│   ├── README.md                       # Gmail connection details, permission note
│   └── screenshot.png                  # [Pending] Connector working with private details blurred
├── task-3-skill-plus-connector/
│   ├── README.md                       # Combined workflow description and verification
│   └── screenshot.png                  # [Pending] Formatted live result
├── task-4-portable-handoff/
│   ├── README.md                       # Portability proof in Claude Code
│   └── proof.png                       # [Pending] Claude Code session showing Skill working
└── task-5-skill-audit/
    ├── README.md                       # Safety assessment and verdict
    └── screenshot.png                  # [Pending] The audited Skill in the directory
```

## Remaining To-Do

- [ ] Add screenshots for each task (private details blurred where applicable)
- [ ] Push to GitHub
