# GradFast ⚡

**Graduate faster than they think you can.**

---

## The Problem

I came to Stanford as an international student with almost no credits. No AP advantage, no older siblings who knew the system, no advisor who gave me more than the standard answer. I graduated in 3 years with both a bachelor's and a master's in Computer Science — by learning how universities actually work from the inside.

Most students don't know about double-counting rules, course substitution petitions, or which community college courses their university has accepted before. They don't know their STEM extension window, or that taking the right elective in the wrong quarter costs them a full term. GradFast exists so that information isn't locked behind years of trial and error.

---

## What It Does

GradFast is a three-step AI-powered graduation planner:

**1. Intake — 6 questions, ~2 minutes**

Name, university, major, year, target graduation, and prior credits. University and major use real-time search dropdowns with 100+ options.

**2. Plan Generation — AI builds your full schedule**

GPT-4o-mini generates a complete quarter-by-quarter or semester-by-semester plan using the real course codes, unit counts, and graduation requirements for your specific university. Not generic advice — real course codes like CS106A, AUCORE-100, or 18.01.

**3. Live Advisor Chat — tell it anything, it updates the calendar**

Say "move CS106B to Spring 2026" and it moves. Say "I want to study abroad Winter junior year" and it rearranges the affected courses and shows you what changes. Say "can I graduate early?" and it does the unit math and gives you a specific revised timeline.

---

## Architecture

```
User input (6 questions)
        │
        ▼
generatePlan() ──► OpenRouter API (GPT-4o-mini)
        │           System prompt: real university requirements,
        │           correct course codes, unit counts, calendar type
        │
        ▼
PlanData (JSON)
  - terms[]         ◄── quarter/semester columns
  - courses[]       ◄── color-coded cards (hard / flexible / completed)
  - alternatives[]  ◄── specific substitutes per requirement
  - transferOptions ◄── real CC courses accepted at this university
  - loopholes[]     ◄── double-counting, petition processes
        │
        ▼
Planner UI (React + Tailwind)
  ┌─────────────────────────────┬──────────────────┐
  │  Scrollable term grid       │  Advisor chat    │
  │  Red  = hard requirement    │  Streaming LLM   │
  │  Yellow = flexible (click)  │  responses       │
  │  Green = completed          │                  │
  │                             │  applyMove()     │
  │  ◄── applyMove() updates    │  ← frontend      │
  │      calendar in real time  │    course logic  │
  └─────────────────────────────┴──────────────────┘
```

**Course move logic runs in the frontend — not the LLM.** The advisor returns a course code and destination term. `applyMove()` handles the actual array manipulation. This makes moves instant and reliable regardless of model output quality.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript + Vite |
| Styling | Tailwind CSS v4 + shadcn/ui |
| Routing | React Router v7 |
| LLM | GPT-4o-mini via OpenRouter API |
| Plan generation | Single-shot JSON generation (8k tokens) |
| Advisor chat | Stateful chat with full plan context |
| Course moves | Frontend `applyMove()` function |
| PDF parsing | N/A — browser-native |

---

## Setup

```bash
git clone https://github.com/nesibmu/GradFast.git
cd GradFast
npm install
```

Create a `.env` file:

```
VITE_OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Run:

```bash
npm run dev
```

Opens at http://localhost:5173

---

## Evaluation

Tested across 5 different student profiles:

| University | Major | Year | Result |
|---|---|---|---|
| Stanford | Computer Science | Incoming freshman | 12 quarters, 180 units, real CS course codes |
| MIT | Mathematics | Sophomore | 8 remaining semesters, GIR structure correct |
| UC Berkeley | Economics | Junior | Breadth requirements, correct semester format |
| American University | Political Science | Freshman | AU Core requirements, correct 120-credit total |
| Carnegie Mellon | Computer Science | Sophomore | SCS core requirements, correct unit structure |

**Key validation criteria:**
- Does the plan use real course codes for that university?
- Do the units add up to the correct total for that school and major?
- Are hard requirements correctly marked as non-substitutable?
- Does the advisor chat update the calendar when asked to move a course?
- Are transfer credit recommendations specific and real (not generic)?

**User feedback:** Tested with 4 Stanford students and 2 students from other universities. All confirmed the course codes and requirement structures matched their actual degree audits. The course-move feature worked correctly in all test cases.

---

## What's Next

- **Live course catalog integration** — pull the actual requirements page from a university's registrar website and ground the plan in real-time data rather than training knowledge
- **Crowdsourced transfer database** — let students submit successful credit transfers so the system learns which CC courses each university actually accepts
- **Degree audit import** — connect to student portal APIs to import a real transcript and mark completed courses automatically
- **Petition templates** — auto-generate the email or form needed to petition for a course substitution or waiver at a specific university
- **Study abroad course matching** — for each study abroad program, map the available courses to the home university's requirements automatically

---

## AI Usage Disclosure

Built for CS 153: Frontier Systems — Stanford University, Spring 2026.

**At runtime:** Every graduation plan and advisor response is generated by GPT-4o-mini via the OpenRouter API. The system prompts encode knowledge of US university systems, course structures, transfer policies, and requirement types. No plan is cached or pre-generated — every student gets a fresh plan based on their specific inputs.

**During development:** Claude (Anthropic) was used for architecture review, code iteration, debugging, and README drafting. All commits are in the repo history showing the progression from initial scaffolding to final product.

The Figma design was generated using Figma's AI make tool and served as the UI foundation. All React component logic, API integration, course-move functionality, and prompt engineering were written from scratch on top of that base.

---

## Project Track

**Application / Product** — a deployed AI-native tool that solves a real, specific problem for a large underserved user group: students who want to graduate faster but don't have access to the institutional knowledge to do it.
