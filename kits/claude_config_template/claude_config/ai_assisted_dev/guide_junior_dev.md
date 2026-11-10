---
tags: [ai, dev, guide, junior]
---

# AI-Assisted Development: A Guide for Junior Developers

> This guide exists because the most dangerous version of AI coding is the one that feels productive. Read it before you write a single line with an AI assistant.

---

## The Core Problem: Comprehension Debt

AI can generate an entire working application in minutes. This feels like a superpower. It is also a trap.

**Comprehension Debt** is the gap between the code that exists in your project and the code you actually understand. It accumulates silently. You don't notice it until something breaks and you have no idea where to start — because you never built a mental model of the system in the first place.

"Vibe coding" is how comprehension debt grows: you give the AI a vague instruction, copy the output, ask it to fix errors when they appear, repeat until it works. The code ships. You understand nothing.

This is not a productivity strategy. It is a liability you are deferring.

---

## Your Actual Job

You are not a typist. You are not a prompt engineer. You are a software architect.

The AI is a fast, tireless intern with zero knowledge of your project. It will generate plausible-looking code based on the statistical average of everything it was trained on — which is not your codebase, not your constraints, and not your users.

Your job:
- Define the problem clearly before any code is written
- Design the solution at a structural level
- Provide the AI with bounded, specific tasks
- Verify that what it produced is correct, safe, and maintainable

If you are not doing those four things, you are not using AI — AI is using you.

---

## The Spec-Driven Workflow

### Step 1: Prime the Context

Before writing a single prompt, create a `memory.md` file in your project root. This is the AI's briefing document. It must contain:

- Language and runtime version
- Frameworks and libraries in use (with versions)
- Architectural patterns (e.g. "all DB access goes through repository classes, never directly in route handlers")
- What is explicitly out of scope (e.g. "no external databases — use local JSON only")
- Naming conventions
- Testing philosophy

Without this, the AI defaults to generic internet-average patterns. With it, the AI's output is constrained to your actual system.

Update `memory.md` every time a meaningful architectural decision is made.

### Step 2: Plan Before You Build

Never ask the AI to write code as the first step. Ask it to write a plan.

Prompt structure:
> "I want to add [feature]. Here is the current system context: [paste relevant section of memory.md]. Draft a step-by-step implementation plan. Do not write any code yet."

Read the plan. Correct it. Reject suggestions that violate your architecture. Only when the plan is right do you proceed.

This step is where you catch the AI's assumptions before they become your bugs.

### Step 3: Prompt with Guardrails

When you ask for code, use a three-part structure:

1. **The task** — one specific, testable action. Not "make the edit button work." Instead: "Add a boolean `editable` field to the `users` table and update the User model to include it."

2. **Background** — reference exact files, paste relevant schemas, attach screenshots if needed. The AI cannot read your codebase unless you show it.

3. **The "Do Not" section** — explicit list of what must not change. "Do not modify the authentication middleware. Do not alter the existing migration files. Do not change the API response shape."

The "Do Not" section is not optional. Without it, the AI will refactor things you didn't ask it to touch.

### Step 4: Verify, Don't Trust

Never mark a task done because the AI said it's done.

Give the AI the tools to test its own output:
- Provide compiler or type-check commands: "Run `tsc --noEmit` after writing the code and fix any errors before showing me the result."
- Provide test scripts: "Run `pytest tests/test_feature.py` and paste the output."
- Ask it to describe what it changed and why.

If the AI cannot explain why it made a specific choice, that choice is suspect.

---

## Keeping Your Own Skills Sharp

### The Interview Rule

Only let the AI write code you already know how to write. If a problem is genuinely new to you, write it yourself first. Struggling through an unfamiliar problem is how you build a mental model. Skipping that step means you will never be able to debug it later.

### Tutor Mode

When learning a new concept, disable autocomplete. Tell the AI:
> "Explain this concept to me. Do not write the code. Ask me questions to test my understanding."

This produces dramatically better retention than reading AI-generated code.

### Manual Refactoring

Once a month, pick a module the AI wrote and rewrite it entirely by hand. You will find things you didn't understand. Fix your understanding, not just the code.

### The Comprehension Score

Before committing any AI-generated feature, rate your understanding of the code from 1 to 5. If your score is below 4, either demand the AI explain every decision line-by-line until you reach 4, or delete the code and start over.

Do not ship code you cannot explain to another developer.

---

## Project Structure

Use this structure for every project:

```
my-project/
├── memory.md               # AI context file — tech stack, rules, constraints, architecture
├── requirements.md         # High-level goals and feature scope
│
├── src/
│   ├── main/               # Core logic
│   └── utils/              # Helpers
│
├── tests/                  # Tests the AI can run to verify its own output
│   └── test_main.py
│
├── docs/
│   └── architecture.md     # How the system connects — maintained by you, not the AI
│
└── README.md
```

The `memory.md` file is not documentation. It is an operational constraint document. Keep it accurate and current.

---

## Quick Reference

| Vibe Coding | Spec Coding |
|---|---|
| "Build me a login system" | "Add JWT validation to the `/auth` route per the plan in memory.md" |
| Copy output, hope it works | Run tests, read the diff, verify logic |
| Fix errors by re-prompting blindly | Understand the error, tell the AI exactly what to fix |
| Ship when it stops throwing exceptions | Ship when you understand what it does and why |

---

## The Mindset in One Sentence

You are responsible for every line of code in your repository — the AI does not take ownership of bugs, security holes, or architectural mistakes. You do.

Use AI to go faster. Not to go without understanding.
