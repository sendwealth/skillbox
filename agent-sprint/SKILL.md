---
name: agent-sprint
description: Decide when to use gstack, ruflo, or both — structured sprint flow decision tree for AI agent development.
---

# Agent Sprint

Use this skill when starting a task or feature to decide the right tool combination and sprint approach. It does not teach how to use gstack or ruflo — it tells you **when** to use which.

Core idea: gstack owns the **workflow** (Think → Plan → Build → Review → Test → Ship → Reflect). ruflo owns the **infrastructure** (multi-agent coordination, shared memory, federation). Most projects benefit from both.

## Layer 1: Should You Even Start a Sprint?

```
New task or feature request
│
├── Single file, no architecture impact, under 15 min?
│   └── Use Claude Code directly. No sprint needed.
│
├── Needs structured process (plan → build → review → ship)?
│   └── Start a gstack sprint.
│
├── Needs multi-agent collaboration (parallel tasks, shared memory)?
│   └── Use ruflo Swarm.
│
└── Both structured process AND multi-agent collaboration?
    └── Combined mode. Proceed to Layer 2.
```

Judgment dimensions: **task complexity** × **collaboration need**.

- Simple (< 15 min, single file, no architecture): no tool overhead.
- Process discipline needed: gstack.
- Multi-agent collaboration: ruflo.
- Complex projects: combine both.

## Layer 2: Phase-by-Phase Tool Selection

| Phase | gstack | ruflo | Use | Why |
|-------|--------|-------|-----|-----|
| **Think** | `/office-hours` | — | gstack | Product thinking is gstack's unique strength. 6 forced questions, YC-style. |
| **Plan** | `/plan-ceo-review` `/plan-eng-review` `/plan-design-review` | `/ruflo-goals` | gstack scopes WHAT, ruflo decomposes HOW | gstack finds the 10-star product; ruflo breaks goals into GOAP A* action plans |
| **Build** | Manual coding | Swarm Workers | Single feature → gstack. Parallel features → ruflo | Scale determines the tool |
| **Review** | `/review` + `/codex` | `ruflo-jujutsu` | gstack | Dual-model (Claude + Codex) cross-review catches more blind spots than single-model diff analysis |
| **Test** | `/qa` real browser | `ruflo-testgen` + `ruflo-browser` | gstack for visual QA, ruflo for coverage gaps | gstack is diff-aware and runs real browsers; ruflo generates missing tests |
| **Ship** | `/ship` + `/land-and-deploy` | — | gstack | Release pipeline is gstack-exclusive |
| **Reflect** | `/retro` | SONA self-learning | Both | gstack gives humans a weekly retro; ruflo gives agents persistent learning |

## Layer 3: Composition Modes

### Sequential (start here)

```
gstack Think → gstack Plan → ruflo Build → gstack Review → gstack Test → gstack Ship → Dual Reflect
```

Clean handoffs. Use for most projects.

### Parallel (advanced)

```
gstack Sprint (main feature) + ruflo Swarm (subtasks in parallel) → gstack Review merges results
```

Use when the main feature has independently executable subtasks that don't block each other.

## Trigger Suggestions

After each phase completes, suggest the next:

```
[agent-sprint] Think phase done. Design doc exists.
  Next → Plan phase
    gstack: /plan-eng-review
    ruflo: /ruflo-goals
  Confirm? (y/n)
```

Trigger conditions (recommend, don't auto-advance):

| Transition | Condition |
|-----------|-----------|
| Think → Plan | Design doc output exists |
| Plan → Build | Architecture doc + test plan ready |
| Build → Review | New commits detected |
| Review → Test | No CRITICAL issues |
| Test → Ship | All tests green |
| Ship → Reflect | PR merged or deployed |

## Anti-Patterns

1. **Don't** use Ruflo Swarm for single-agent tasks — overkill, adds latency for no gain.
2. **Don't** skip Think and jump to Plan — the 6 forced questions are where gstack delivers its core value.
3. **Don't** run gstack and ruflo simultaneously in Build phase — two agents editing the same codebase creates conflicts.
4. **Don't** skip Review before Ship — `/review` catches what CI misses: N+1 queries, race conditions, trust boundaries, missing indexes.
5. **Don't** launch a full sprint for tasks under 1 hour — the overhead isn't worth it. Use Claude Code directly.

## Heuristic Learning Connection

This sprint flow is an instance of Heuristic Learning (HL):

- Sprint phases = **structured code iteration** (not gradient descent)
- `/retro` + SONA = **experiment recording and replay** for both humans and agents
- Anti-patterns = **regression tests** against common process mistakes
- Each sprint output feeds the next = **cumulative knowledge without catastrophic forgetting**
