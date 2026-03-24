---
name: product-use-cases
description: Generate realistic use-case prompts/tasks for a product given a URL or description. Analyzes the product's value proposition and ICP, then produces Discovery tasks (no product mention) and Usability tasks (product-specific implementation). Use when asked to generate use cases, test prompts, ICP tasks, or product evaluation scenarios.
---

# Product Use-Case Generator

Generate 10 realistic tasks/prompts that a product's ideal customer would enter when facing the problems the product solves.

## Workflow

1. **Research the product** — Fetch the provided URL (use `web_fetch`). Extract: product name, what it does, who it's for (ICP), core features, and key problems it solves. Keep research high-level (landing page + maybe one additional page like /features or /pricing). If no URL is provided, use the product description directly.

2. **Identify ICP and pain points** — From the research, determine:
   - Who is the target user (role, industry, context)
   - What problems they face before discovering this product
   - What tasks they'd need to accomplish with this product

3. **Generate tasks** — Produce exactly 10 tasks split into two categories, each with three difficulty levels.

## Output Structure

```
# [Product Name] — Use Case Tasks

## ICP Summary
[1-2 sentences: who the target user is and their core pain points]

## Discovery
Tasks where the user is exploring solutions. Do NOT mention the product by name — write as if the user hasn't found it yet.

### Simple

**Task Title:** [short task name]
**Task Description:** [1 sentence briefly describing the task]
**Task Prompt:** [the actual prompt a user would type into a coding agent — realistic, natural language, 1-3 sentences]
**Goal Title:** [short goal name]
**Goal Description:** [2-4 sentences describing what "success" looks like. Be specific enough that an LLM evaluator can determine if the goal was achieved. Include concrete deliverables, expected outputs, or verifiable conditions.]

### Intermediate

**Task Title:** [title]
**Task Description:** [description]
**Goal Title:** [title]
**Goal Description:** [description]

### Complex

**Task Title:** [title]
**Task Description:** [description]
**Goal Title:** [title]
**Goal Description:** [description]

## Usability
Tasks where the user has chosen [Product Name] and needs to implement. Mention the product by name. Focus on implementation.

### Simple

**Task Title:** [title]
**Task Description:** [description]
**Goal Title:** [title]
**Goal Description:** [description]

[... repeat for each task with Task Title, Task Description, Goal Title, Goal Description]
```

## Task Distribution

- **Discovery:** 3 tasks (1 simple, 1 intermediate, 1 complex)
- **Usability:** 7 tasks (2 simple, 3 intermediate, 2 complex)
- Total: 10 tasks

## Task Writing Guidelines

- Write each task as a realistic prompt/query the ICP would actually type
- Discovery tasks should describe the *problem* or *goal*, not the solution
- Usability tasks should reference the product name and focus on concrete implementation steps
- **Simple:** Single-step, straightforward, a beginner could do it
- **Intermediate:** Multi-step, requires some domain knowledge or configuration
- **Complex:** Advanced integration, edge cases, or multi-system orchestration
- Every task must connect to a real use case of the product — no generic filler
- Each task has exactly one goal with a **Title** (short name) and **Description** (2-4 sentences with specific success criteria an LLM can evaluate — include expected outputs, verifiable conditions, or concrete deliverables)
