---
name: implement-and-review
description: Run the "loop engineering" pattern via the Workflow tool — one implementer agent, then N adversarial reviewers who see only the diff (not the implementer's reasoning), then a fix pass. Use when the user asks to run an implement-and-review loop, an adversarial review loop, "loop engineer" a task, or references Jared Sumner's Bun-in-Rust workflow pattern.
argument-hint: <task description> [--reviewers N] [--implementer-model X] [--reviewer-model Y]
allowed-tools: Workflow, Bash, Read, Write
---

# Implement and Review

A single-dev-machine version of the loop-engineering pattern from Jared Sumner's
Bun-in-Rust rewrite: one implementer, N adversarial reviewers, one fix pass.
Reference: https://bun.com/blog/bun-in-rust#loops-that-write-review-code

## When to trigger

- "run the implement-and-review loop"
- "loop engineer this" / "loop engineering"
- "adversarial review loop"
- any request to implement something with adversarial review built in before
  it's considered done

## How to run it

The Workflow tool is gated — only call it when the user has explicitly opted
into multi-agent orchestration (see the Workflow tool's own rules). If they
haven't, describe what this would do and ask first instead of calling it.

Once opted in:

1. Check whether the target repo already has
   `.claude/workflows/implement-and-review.js`.
   - If yes, run it by name:
     `Workflow({ name: "implement-and-review", args: { task, reviewerCount, implementerModel, reviewerModel } })`
   - If no, copy `assets/implement-and-review.js` (next to this file) into the
     target repo at `.claude/workflows/implement-and-review.js` and run it the
     same way. If the target repo has no `.claude/workflows/` convention at
     all, skip installing it and instead pass the asset's contents inline via
     `Workflow({ script, args })`.

2. Required: `args.task` — plain description of what to implement.
   Optional: `args.reviewerCount` (default 2), `args.implementerModel`
   (default `"sonnet"`), `args.reviewerModel` (default `"opus"`). The reviewer
   defaults to the bigger model on purpose: writing a straightforward diff is
   cheap work, but catching the subtle bugs a reviewer is supposed to find
   benefits more from extra capability, so the stronger model earns its keep
   on the harder side of the loop.

## What the workflow does

- **Implement**: one agent makes the smallest correct change for `task`.
- **Capture diff**: `git diff` is captured verbatim.
- **Review**: `reviewerCount` reviewers run in parallel, each seeing only the
  stated task and the diff — never the implementer's reasoning — instructed
  to assume the code is wrong and find bugs or missed edge cases, not style
  nitpicks.
- **Fix**: any non-minor finding is resolved in a follow-up pass. Returns
  `{ task, reviewerCount, findings }`.

## Notes

- The original Bun rewrite used one model (a pre-release Fable 5) for every
  role — the adversarial effect came purely from withholding the
  implementer's reasoning from reviewers, not from model diversity. This
  script adds optional per-role model overrides, and defaults them
  asymmetrically (bigger model on review) as an extension beyond what the
  article describes.
- Source PR that introduced this workflow:
  https://github.com/promptingcompany/costarena/pull/2

## Task
$ARGUMENTS
