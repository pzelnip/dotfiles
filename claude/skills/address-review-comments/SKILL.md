---
name: address-review-comments
description: Fetch, address, and resolve code-review comments on a GitLab MR (or GitHub PR) with a verify-before-resolve workflow. Use when the user asks to address/action/incorporate review feedback on an MR/PR and resolve the threads.
---

# Address Review Comments

Drive an MR/PR's review threads from "open with feedback" to "addressed, pushed, and resolved"
without the two failure modes that cause rework: **resolving threads before the change is live**,
and **misreading a comment's intent**.

## Core principles (read first)

- **Resolve only after the change is live on the remote.** The order is strict:
  apply → verify → commit → push → confirm the change is in the pushed diff → resolve.
  Resolving a thread whose change is still local (or wrong) is the #1 mistake this skill exists to
  prevent. "Edited locally" ≠ "done."
- **Interpret by intent, not literally.** Restate each comment as the reviewer's goal before
  editing. Literal wording can mislead (e.g. "remove the asterisk" meant the `*,` keyword-only
  marker in a signature; "reuse the existing fixture" was answered by creating a *new* one). When a
  comment anchors to a line, read that exact line in the committed diff to decode it.
- **"Throughout / everywhere / same pattern" = a sweep.** Grep every candidate site and verify each;
  don't only fix the one form shown.
- **Verify subagent edits.** If you delegate fixes, a subagent's "APPLIED" is a claim, not evidence.
  Diff its actual change against the comment intent before relaying or resolving.
- **If a suggestion is a bad idea or infeasible, don't apply it.** Leave the thread open and, when
  reporting back, recap why. Don't silently skip it.

## Workflow

### Step 1: Identify the MR/PR

Use the MR/PR from the invoking message (URL, number, or "current" for the checked-out branch). Do
not reuse a number from earlier context. For GitLab/current branch: `glab mr view`.

### Step 2: Fetch unresolved threads

GitLab (threads carry `resolvable`/`resolved`; note the **discussion id** — needed to resolve):

```bash
glab api "projects/:id/merge_requests/<IID>/discussions?per_page=100" > /tmp/mr_disc.json
jq -r '.[] | select(.notes[0].resolvable == true) | .notes[0] as $n
  | select($n.resolved==false)
  | "DISCUSSION:\(.id)\n  \($n.author.username) | \($n.position.new_path // "n/a"):\($n.position.new_line // $n.position.old_line // "n/a")\n  \($n.body)\n"' /tmp/mr_disc.json
```

Comment line numbers come from the diff version they were left on — they may be stale. Locate the
target by **content**, not the reported line number. If a comment is cryptic, read the exact
anchored line in the committed blob: `git show <head_sha>:<path> | sed -n '<line>p'`.

### Step 3: For each comment — restate intent, then apply

For every unresolved comment:

1. **Restate the intent** in one line (what the reviewer wants achieved).
2. If literal text and intent diverge, go with intent; plan to note the interpretation in the reply.
3. If it says "throughout/everywhere," `grep` all candidate sites and handle each (verify each is
   actually the case — e.g. a variable is genuinely unused — don't assume from the form).
4. Apply the change, matching surrounding code style and the user's known conventions.
5. If you decide **not** to apply (bad idea / infeasible), leave it and record the reason.

Delegating to subagents (for many comments, split by file to avoid edit conflicts): instruct each
to report APPLIED / NOT-APPLIED-because per comment — then **you diff their output against the
comments yourself**. Do not trust the self-report. Subagents must not touch config files
(`.coveragerc`, `pytest.ini`, `pyproject.toml`); verify with `git status` after.

### Step 4: Verify

Run the project's linters and the affected tests. A source change can strand an existing test
(e.g. removing behavior a test asserted) — reconcile those before proceeding. Fix until green.

### Step 5: Commit & push

Commit the addressed changes and push. (Respect repo commit conventions — e.g. a
`prepare-commit-msg` hook may already prepend a ticket key; don't duplicate it.) Only commit/push
when the user has asked you to, or has an established pattern of wanting it for this task.

### Step 6: Confirm changes are live

Before resolving anything, confirm the pushed diff actually contains the changes:

```bash
git log origin/<branch>..HEAD --oneline   # empty = local and remote in sync
```

Optionally spot-check a specific edit is present in the remote diff. **This gate is the point of
the skill** — never skip from "applied" to "resolved."

### Step 7: Reply, then resolve (only what you fixed)

For each thread you addressed, post a short reply noting what changed (and the commit), then resolve
it. GitLab (no dedicated subcommand for resolving a discussion — `glab api` is correct here):

```bash
# reply
glab api --method POST "projects/:id/merge_requests/<IID>/discussions/<DID>/notes" \
  --field "body=Applied in <sha>: <one-line what changed>"
# resolve
glab api --method PUT "projects/:id/merge_requests/<IID>/discussions/<DID>?resolved=true"
```

For threads you did **not** fix: leave them open (do not resolve). Optionally reply explaining why.

### Step 8: Recap to the user

Report: which comments were applied, which were not (and why), the commit(s) pushed, and which
threads were resolved vs left open. Surface anything that lost coverage or that you interpreted
non-literally.

## Anti-patterns (do not do)

- Resolving threads while changes are uncommitted/unpushed.
- Relaying a subagent's "APPLIED" without diffing the actual edit.
- Fixing only the literal line when the comment said "throughout."
- Applying a suggestion literally when the intent was clearly different.
- Silently skipping a suggestion you disagree with instead of leaving it open and explaining.
