---
name: au:stack-mr
description: Splits the current branch into a stack of smaller MRs, each targeting the previous one. Call manually when a branch is too large for one MR.
allowed-tools: Bash(git *:*), Bash(glab *:*)
id: abe139bacea8a1f871377a3921429ea0
---

# au:stack-mr

Turns a single branch with multiple logical units of work into a chain of MRs where each targets the previous one. By default all commits stay on their current hashes — the skill only creates new branch pointers and MRs. For branches that are one feature plus review iterations (where the seam runs across files, not commit boundaries), it offers an opt-in **file-based rewrite mode** (step 4b) that rebuilds the commits from the final tree with a mandatory integrity check.

## Arguments

None. Operates on the current branch.

---

## Phase 1: Pre-flight checks

### 1. Check git state

```bash
git branch --show-current
```

If on `main`, `master`, or `staging`: STOP. Tell the user this skill must be run from a feature branch.

```bash
git status --porcelain
```

If there are uncommitted changes: STOP. Ask the user to commit or stash them first.

### 2. Find the merge base

```bash
git merge-base HEAD main
```

Store the result as `$BASE`.

```bash
git log $BASE..HEAD --oneline --reverse
```

Show the output to the user. These are all the commits that will be distributed across the stack, listed oldest-first with their short hashes and subjects.

If there is only 1 commit: STOP. A single-commit branch does not need stacking.

Store the commit list as ordered pairs of `(short_hash, subject)`.

---

## Phase 2: Analyse and propose

### 3. Measure the diff

Get line-level stats for every file changed since `$BASE`:

```bash
git diff $BASE..HEAD --numstat
```

This outputs `added  removed  filepath` per file. Classify each file:

- **Test file**: path matches `*.test.*`, `*.spec.*`, `**/__tests__/**`, `**/test/**`, or `**_test.*`
- **Logic file**: everything else (source, config, migrations, docs, etc.)

Sum up:
- `LOGIC_LINES` = added + removed across all logic files
- `TEST_LINES` = added + removed across all test files

Also classify each commit by what it primarily touches. For each commit hash in the list:

```bash
git show --numstat --format='' <hash>
```

Label the commit with its dominant category:
- **schema/model**: touches migration files, `*.schema.*`, `**/models/**`, type definition files
- **feature-flag**: commit subject or files contain `featureFlag`, `feature_flag`, `isEnabled`, `ff_`
- **logic**: primary application code (components, services, handlers, utils)
- **tests**: only or mostly test files
- **docs**: only `.md`, `.txt`, or similar documentation files
- **config/infra**: CI files, `Dockerfile`, `*.json` config, build scripts
- **mixed**: touches multiple categories roughly equally

### 4. Recommend: stack or not

**If `LOGIC_LINES` <= 300:**

Tell the user:

> "This branch has `LOGIC_LINES` lines of logic changed (`TEST_LINES` lines of tests). That's within the ~200-300 line target for a single MR - stacking is not needed."

STOP. Do not proceed to naming or branch creation unless the user explicitly overrides and asks to stack anyway.

**If `LOGIC_LINES` > 300:**

First, decide *what kind of branch this is* — it determines whether the seam runs along commit boundaries or across files.

**Are the commits distinct layers, or iterations of one feature?**

Inspect the commit subjects and the file overlap between commits:
- **Layered** — each commit introduces a distinct unit and later commits mostly touch *different* files (schema commit, then handler commit, then UI commit). The seam runs along commit boundaries → use the commit-boundary logic below.
- **Iterated** — commits are one feature plus revisions: subjects like "address feedback", "fix review", "wip", "fixup", "pr comments", and the later commits re-edit the *same files* as the first. Confirm by checking file overlap:

  ```bash
  # For each pair of adjacent commits, do they touch the same files?
  for h in <hash1> <hash2> <hash3>; do echo "== $h =="; git show --numstat --format='' $h | awk '{print $3}'; done
  ```

  If the commits heavily re-edit the same files, **commit-boundary splitting will not work** — splitting there makes Layer 1 an outdated draft that Layer 2 rewrites. The real seam is *by file at the final tree state* (e.g. foundation/plumbing files vs. the feature that consumes them). Go to **step 4b: file-based rewrite mode**.

For **layered** branches, look for independently reviewable seams in the commit sequence. A seam exists at a commit boundary when:
- The commit type changes (e.g. schema → logic, feature-flag → logic)
- A commit introduces something that the next commit consumes (a type before its usage, a flag before its consumer, a wrapper before its caller)
- A commit is self-contained and reviewable without the commits that follow it

Apply the rules when proposing groups:
- Tests travel with the feature they cover. Never put tests in a separate layer from the code they exercise. A layer with 200 lines of code + 300 lines of tests is fine.
- Model/schema changes, feature flag setup, and infrastructure changes are good candidates for their own layer when subsequent commits depend on them.
- Docs can be a separate layer or paired with whichever layer is most relevant.
- Each layer must be independently reviewable and make sense to a reviewer who hasn't seen the rest of the stack.

**If no clean commit-boundary seams exist** (all commits are tightly coupled logic with no natural split point):

Check whether a **by-file** seam exists at the final tree state — a set of files that is independently reviewable and consumed by the rest (foundation/plumbing vs. the feature). If so, offer **step 4b: file-based rewrite mode**.

If there is neither a commit-boundary seam nor a by-file seam, tell the user:

> "This branch is `LOGIC_LINES` lines of logic, but I can't find clean seams to split it along — not at commit boundaries, and not by file at the final tree. All changes appear tightly coupled. Consider splitting the work before committing if you want a stack, or proceed as a single MR."

STOP unless the user wants to define split points manually.

**If clean seams exist**, propose a grouping:

```
This branch has <LOGIC_LINES> lines of logic across <N> commits. I'd suggest splitting it into <M> MRs:

Layer 1 (<n> commits, ~<lines> logic lines): <rationale — e.g. "schema and type changes that layer 2 depends on">
  - <commit hash> <subject>
  - <commit hash> <subject>

Layer 2 (<n> commits, ~<lines> logic lines + <lines> test lines): <rationale>
  - <commit hash> <subject>
  ...

Does this grouping make sense, or would you like to adjust the split points?
```

Wait for the user to confirm or describe adjustments. If they adjust, update the grouping and show it again before continuing. Repeat until confirmed.

**If the user wants to define split points manually** (either because no seams were found, or they reject the proposal):

Show the numbered commit list and ask:

> "Paste the short hash (or commit number) where each layer ends. The last layer automatically gets the remaining commits.
>
> Example for 3 layers: `abc1234, def5678` (2 split points for 3 layers)"

Accept: short hashes, full hashes, or 1-based commit position numbers (e.g. `2, 4` means commits 1-2 are layer 1, commits 3-4 are layer 2, rest are layer 3).

Validate:
- Split points must be in strictly ascending order
- Each hash must exist in the commit list
- Every layer must have at least one commit

Show the grouping with per-layer line counts and wait for confirmation.

### 4b. File-based rewrite mode (for iterated branches)

Use this **only** when commit-boundary splitting can't work — the branch is one feature plus review iterations, and the real seam runs across *files* at the final tree state.

This mode **rewrites history**: instead of pointing branches at existing commits, it builds new commits (one per layer) from the final tree (`HEAD`), partitioned by file. This is a deliberate exception to the "branch pointers only" rule. Because it rewrites, it MUST:

1. **Get explicit confirmation first.** Tell the user plainly that this rewrites the branch's commits (they stay recoverable via `git reflog`, and the original branch pointer is left untouched as a recovery point). Ask before proceeding.
2. **Partition every changed file into exactly one layer.** List the changed files (`git diff $BASE..HEAD --name-only`) and assign each to a layer. Foundation/plumbing files that later layers consume go in earlier layers. Ask the user to confirm the partition.
3. **Watch for shared files.** A fixture, helper, or type used by more than one layer's files must live in the *earliest* layer that needs it, or that layer won't be self-consistent. Grep for cross-layer usage before finalizing the partition.

Build the commits from the final tree, oldest layer first:

```bash
ORIG_HEAD=$(git rev-parse HEAD)      # recovery point — the original branch still points here
BASE=$(git merge-base HEAD main)

# Layer 1: branch at base, check out ONLY this layer's files from the original HEAD
git checkout -b <layer-1-branch> $BASE
git checkout $ORIG_HEAD -- <layer-1-file-1> <layer-1-file-2> ...
git commit -m "<layer-1 message>"    # scope the message per step 5

# Layer 2: branch on top of layer 1, add this layer's files
git checkout -b <layer-2-branch>
git checkout $ORIG_HEAD -- <layer-2-file-1> ...
git commit -m "<layer-2 message>"
# ...repeat for remaining layers
```

**Never use `git add -A` / `git add .`** — it would sweep in untracked files that aren't part of the branch. Stage only the named paths (`git checkout $ORIG_HEAD -- <paths>` stages them for you).

**Mandatory integrity check** — the top layer's tree MUST be byte-for-byte identical to the original HEAD tree, proving no content was lost or altered:

```bash
TOP_TREE=$(git rev-parse <top-layer-branch>^{tree})
ORIG_TREE=$(git rev-parse $ORIG_HEAD^{tree})
[ "$TOP_TREE" = "$ORIG_TREE" ] && echo "OK: layers reproduce original tree exactly" || echo "MISMATCH"
```

If the trees differ, **STOP and do not push.** Show the user `git diff <top-layer-branch> $ORIG_HEAD --stat` to reveal what was dropped or added (commonly: a file missing from the partition, or an untracked file that got staged), fix the partition, and rebuild.

Once the trees match, proceed to step 5. In this mode the last layer is a *new* branch (not the current branch pointer) — the original branch is intentionally left in place as a recovery point, so do not skip creating the top layer's branch.

### 5. Name the layers

Extract the ticket number from the current branch name. Pattern: leading `[A-Z]+-[0-9]+` segment (e.g. `COSUB-123` from `COSUB-123-refactor-auth`). If no ticket number is found, use the full current branch name as the prefix.

For each layer, propose a branch name using the pattern:

`<ticket-number>-layer-<i>-<short-description>`

Where `<short-description>` is a 2-4 word kebab-case summary derived from the layer's commit subjects or the rationale used when proposing the split. Keep it under 30 characters total after the prefix.

Example: `COSUB-123-layer-1-schema-changes`, `COSUB-123-layer-2-api-handler`, `COSUB-123-layer-3-ui-integration`

The last layer keeps the current branch name unchanged.

Also propose an MR title for each layer. Derive from the commit subjects in that layer:
- Single commit: use the commit subject directly
- Multiple commits: use the common theme or the last commit subject

Prefix every MR title with the ticket key and the layer marker: `[<TICKET>] [Layer i/N] <subject>`. The ticket-in-title matters — many orgs run a CI job (e.g. `zapier/jira`) that **fails the pipeline if the ticket key is absent from the MR title**; putting it only in the description is not enough. If no ticket key was found in the branch name, omit the `[<TICKET>]` prefix.

Show all proposed branch names and MR titles, then ask the user to confirm or override any of them.

---

## Phase 3: Create the stack

### 6. Create branch pointers

For each layer i from 1 to N:

```bash
# Get the full hash of the last commit in this layer
git rev-parse <last_commit_hash>

# Create the branch pointing at that commit
git branch <layer-i-branch-name> <full_hash>
```

The last layer's branch is the current branch (already exists at HEAD). Skip creating it.

If any branch already exists: STOP on that layer, tell the user, ask whether to delete and recreate or abort.

### 7. Push all branches

For each layer branch (including the current branch as the last layer):

```bash
git push origin <branch-name>
```

If push fails for any branch: STOP, report which branch failed and the error. Do not continue to MR creation until all pushes succeed.

---

## Phase 4: Create MRs

### 8. Create one MR per layer

Process layers in order from 1 to N.

For layer 1, target `main`. For layer i > 1, target layer i-1's branch.

```bash
glab mr create \
  --source-branch <layer-i-branch> \
  --target-branch <target-branch> \
  --title "[<TICKET>] [Layer i/N] <subject>" \
  --description "<body>" \
  --squash-before-merge \
  --remove-source-branch \
  --yes
```

**MR body template:**

```markdown
## Summary

[1-2 sentences describing what this layer does]

## Stack

This MR is part of a stack:
- Layer 1: <title> — <MR URL or "this MR"> 
- Layer 2: <title> — <MR URL or "this MR">
...
- Layer N: <title> — <MR URL or "this MR">

> Merge in order. Do not merge a layer until its predecessor is merged and its target branch has been updated to main.

## Commits

<list of commit subjects in this layer>
```

Fill in known MR URLs as each is created. For layers not yet created, mark as `(pending)` - go back and note each URL once available. After all MRs are created, output the final stack table with all URLs.

If `glab mr create` fails for a layer: report the error and continue to the next layer. List any failures at the end.

---

## Phase 5: Report

### 9. Print stack summary

```
Stack created:

  Layer 1: <branch>  →  main       <MR URL>
  Layer 2: <branch>  →  <layer-1>  <MR URL>
  ...
  Layer N: <branch>  →  <layer-N-1> <MR URL>

Merge order: Layer 1 first, then rebase each subsequent layer onto main as predecessors land.
```

If any MR creation failed, list them separately with a note to create them manually using `glab mr create`.

---

## Phase 6: Iterating on a pushed layer (CI fixes)

If a layer's pipeline fails after the stack is pushed (formatting, lint, a small fix), you'll need to update an already-pushed branch. This is allowed — the "never force-push" rule is about *reorganizing the stack*, not about fixing a single layer.

1. Check out the failing layer's branch and make the fix. Keep the fix scoped to files that belong to that layer.
2. Prefer **amend + force-with-lease** to keep "one commit per layer":

   ```bash
   git commit --amend --no-edit        # or -m "..." to reword
   git push --force-with-lease origin <layer-branch>
   ```

   `--force-with-lease` refuses the push if the remote moved unexpectedly (someone else pushed) — always use it instead of a bare `--force`. If the user prefers preserving history, add a separate fixup commit and regular-push instead; `--squash-before-merge` collapses it on merge either way.
3. Confirm the new pipeline is running on the amended SHA. Prefer the **pipeline URL printed by `git push`** — it's the most reliable pointer. `glab ci status -b <branch>` and `glab ci list --branch <branch>` are unreliable (the `-b` value can be misparsed as a date, or the flag may be unrecognized); if you use `glab ci status`, verify the reported SHA matches your amended commit.

---

## Rules

- Default to branch pointers only — do not rewrite commits or rebase. The one exception is **file-based rewrite mode (step 4b)**, which is only for iterated branches, requires explicit user confirmation, and must pass the tree-equality integrity check.
- Never force-push to *reorganize the stack*. Amending an already-pushed layer to fix CI is different — see Phase 6 — and uses `--force-with-lease`, never a bare `--force`.
- In branch-pointer mode the last layer is the current branch - do not create a new branch for it. In file-based rewrite mode (step 4b) the last layer is a new branch and the original branch is left as a recovery point.
- If the user is unhappy with the grouping at any checkpoint, restart from step 4.
- Do not create MRs until all branches are pushed successfully.
- Do not recommend stacking when logic lines are within ~300. Stacking has overhead; only do it when the size or seam structure genuinely justifies it.
- Tests always travel with the code they cover. Never split tests into their own layer.
- Never split on line count alone - there must be a reviewable seam. A 500-line MR with clear cohesion is better than two 250-line MRs where layer 1 is incomplete without layer 2.
