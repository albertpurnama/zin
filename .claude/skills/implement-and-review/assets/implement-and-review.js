export const meta = {
	name: "implement-and-review",
	description:
		"Implement a task, then subject the diff to adversarial review before applying fixes",
	whenToUse:
		"A single-dev-machine version of the loop-engineering pattern from Jared Sumner's Bun-in-Rust rewrite: one implementer plus N adversarial reviewers that see only the diff, not the implementer's reasoning, optionally on a different model per role.",
	phases: [{ title: "Implement" }, { title: "Review" }, { title: "Fix" }],
};

// Usage: Workflow({ name: "implement-and-review", args: { task: "..." } })
// Optional args: reviewerCount (default 2), implementerModel, reviewerModel

const REVIEW_SCHEMA = {
	type: "object",
	properties: {
		findings: {
			type: "array",
			items: {
				type: "object",
				properties: {
					file: { type: "string" },
					summary: { type: "string" },
					severity: { type: "string", enum: ["blocker", "major", "minor"] },
				},
				required: ["file", "summary", "severity"],
			},
		},
	},
	required: ["findings"],
};

const task = args?.task;
if (!task) throw new Error("Pass the task via args.task");

const reviewerCount = args?.reviewerCount ?? 2;
const implementerModel = args?.implementerModel;
const reviewerModel = args?.reviewerModel;

phase("Implement");
await agent(
	`Implement the following task in this repository. Make the smallest correct change and nothing more. Task: ${task}`,
	{ label: "implement", model: implementerModel },
);

const diff = await agent(
	"Run `git diff` in the repository root and return the complete raw output verbatim. Do not summarize or truncate it.",
	{ label: "capture-diff" },
);

phase("Review");
const reviews = await parallel(
	Array.from(
		{ length: reviewerCount },
		(_, i) => () =>
			agent(
				`You are an adversarial code reviewer. You did not write this diff and don't know why any individual choice was made beyond the stated task below. Assume the diff is wrong until proven otherwise — find bugs, missed edge cases, and reasons it could fail. Do not comment on style.\n\nStated task: ${task}\n\nDiff:\n${diff}`,
				{
					label: `review-${i + 1}`,
					phase: "Review",
					model: reviewerModel,
					schema: REVIEW_SCHEMA,
				},
			),
	),
);

const findings = reviews
	.filter(Boolean)
	.flatMap((r) => r.findings)
	.filter((f) => f.severity !== "minor");

phase("Fix");
if (findings.length) {
	log(`${findings.length} reviewer finding(s) to address`);
	await agent(
		`Resolve the following adversarial review findings against the current working tree diff. Only change what's necessary to fix real issues; skip anything already handled or a nitpick. Findings:\n${JSON.stringify(findings, null, 2)}`,
		{ label: "fix", model: implementerModel },
	);
} else {
	log("No blocking findings — implementation accepted as-is");
}

return { task, reviewerCount, findings };
