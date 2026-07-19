---
name: full-test-coverage
description: This skill should be used when the user runs "/full_test_coverage" or asks to "get to 100% test coverage", "cover every uncovered branch", "fill in missing test coverage", or "prune dead branches and cover the rest". It drives a project to 100% test coverage by deleting unneeded branches and adding tests for the rest, then consolidating the resulting tests.
---

# Full Test Coverage

## Overview

Bring the project to 100% test coverage by examining every uncovered branch,
removing the ones that aren't needed and testing the ones that are, then tidying
the resulting tests.

## How to run it

Run the work in a subagent on **sonnet** (skills cannot set a model directly, so
delegate). Invoke the `Agent` tool with `model: "sonnet"` and pass the task
below as the prompt. Prefer a synchronous run so the results come back in the
same turn (`run_in_background: false`). Relay the subagent's final summary to the
user.

## Task prompt to give the subagent

> This project isn't at 100% test coverage. Bring it to 100% by working through
> every uncovered branch:
>
> 1. Generate a fresh coverage report to find uncovered branches, using the
>    project's standard test command (check CLAUDE.md / README — e.g.
>    `uv run python -m pytest --cov`, run from the correct directory).
> 2. For each uncovered branch, decide whether the branch is actually needed:
>    - If it is NOT needed (dead, unreachable, or redundant), delete it.
>    - If it IS needed, add or update a test that genuinely exercises the
>      branch — do not paper over the coverage number.
> 3. Re-run coverage and repeat until it reports 100%.
> 4. Once coverage is complete, review the test changes you made against the
>    existing suite for opportunities to simplify or condense related tests into
>    parameterized tests. Value readability over conciseness — do not
>    parameterize if it makes the tests harder to follow.
>
> Follow the repository's testing conventions throughout (see CLAUDE.md if
> present). End with a summary: branches deleted, tests added/updated, and any
> simplifications made.

## Notes

- If the project has no coverage tooling configured, set it up (or ask the user)
  before proceeding.
- Keep the user's stated preference in mind: readability wins over conciseness.
