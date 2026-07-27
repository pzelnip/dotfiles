---
name: test-improver
description: This skill should be used when the user runs "/test_improver" or asks to "improve the tests", "clean up the test suite", "find test smells/antipatterns", "refactor these tests", or "review the tests for quality". It audits a Python test suite for antipatterns and smells, then applies the improvements.
---

# Test Improver

## Overview

Audit a Python test suite (pytest, usually with pytest-django / factory_boy) for
antipatterns, smells, and redundancy — then **fix them**. This is a quality pass,
not a coverage pass: it must never reduce what the suite actually verifies. If
the user wants coverage filled in, that's `/full_test_coverage`.

## Scope

Default to the tests touched on the current branch (`git diff main...HEAD --stat`)
when there are any; otherwise the whole test suite. If the user names files or a
directory in the invocation args, use exactly that. When a whole large suite is
in scope, work file by file rather than trying to hold it all at once.

## Workflow

1. **Establish a baseline.** Run the project's test command (check CLAUDE.md /
   README / Makefile — e.g. `make test` or `python -m pytest` from the right
   directory) and record pass/fail counts. Also capture coverage if the project
   has it configured; it's the guardrail for step 4.
2. **Read the suite's own conventions first.** Existing factories
   (`factories.py`), fixtures (`conftest.py`), helpers, naming style, and any
   testing guidance in CLAUDE.md. Improvements must move tests *toward* the
   project's conventions, not toward a generic ideal.
3. **Audit** against the catalogue below. Note each finding with file:line.
4. **Apply the fixes**, then re-run the suite. Coverage must not drop and the
   pass count must not drop except where you deliberately deleted a test — call
   those out explicitly.
5. **Run the project's formatter/linter** (e.g. `make format ; make lint`).
6. **Summarize**: tests deleted (and why), tests restructured, helpers replaced
   by factories, and anything you spotted but deliberately left alone.

## Antipattern catalogue

### 1. Tests that assert nothing meaningful — delete them

A test whose subject is a literal constant, or which merely restates the
implementation, has no defect-detecting power.

```python
AVATAR_PRESETS = [f"avatar-{i:02d}" for i in range(1, 17)]

def test_presets_are_sixteen_unique_keys():   # delete
    assert len(AVATAR_PRESETS) == 16
    assert len(set(AVATAR_PRESETS)) == 16
```

Also in this family: tests that only assert a mock was called with the arguments
the test itself just passed; tests asserting a Django field's `max_length` or
`verbose_name` (that's testing Django); `assert result is not None` as the sole
assertion.

**Care:** a constant-shape test is only pointless when the constant is derived
in the same breath. If the constant encodes a contract with something external
(a wire format, a DB column, a fixture file), keep it.

### 2. Assertions inside loops — parameterize

```python
def test_default_avatar_preset_is_deterministic_and_in_set():
    for seed in (0, 1, 15, 16, 12345):
        assert default_avatar_preset(seed) in AVATAR_PRESETS
```

```python
@pytest.mark.parametrize("seed", [0, 1, 15, 16, 12345])
def test_default_avatar_preset_is_deterministic_and_in_set(seed):
    assert default_avatar_preset(seed) in AVATAR_PRESETS
```

A loop gives one failure for N cases and stops at the first; parameterizing
names each case and reports them independently. Same treatment for a run of
near-identical test functions differing only in input/expected value — collapse
them into one parameterized test, using `pytest.param(..., id="...")` when the
default id is unreadable.

**Care:** don't parameterize when the cases need genuinely different setup or
assertions — a `parametrize` whose body is full of `if`s is worse than the
separate tests. Readability beats conciseness.

### 3. Ad-hoc `_make_x(**kw)` helpers — replace with factories

```python
def _ad(**kw):
    defaults = {"title": "This is my title", "city": "victoria", ...}
    defaults.update(kw)
    return ManualAd.objects.create(**defaults)
```

```python
class ManualAdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ManualAd

    title = "This is my title"
    city = "victoria"
    date_posted = factory.LazyFunction(timezone.now)
```

Factories give sequences for unique fields, `SubFactory` for relations,
`LazyFunction` for anything that must be evaluated per-instance (mutable
defaults and `timezone.now()` are the classic bugs in hand-rolled helpers), and
`build()` when no DB row is needed. Put them where the project already keeps
them; if there's no factory module yet, create one alongside the tests.

### 4. Redundant fields passed to a factory — pass only what you assert on

Every argument in a factory call is a claim that the value matters. Noise fields
send the reader hunting for a relevance that isn't there.

```python
def test_browse_manual_card_respects_city(client):
    ManualAdFactory(city="nanaimo", title="Nanaimo only", name="Abby")  # name is noise
```

And when *nothing* about the values matters, take the defaults and assert
against the instance:

```python
def test_ad_page_renders_content(plain_static_storage):
    ad = ManualAdFactory()
    body = Client().get(f"/ad/{ad.uuid}").content.decode()
    assert ad.title in body
    assert ad.description in body
```

**Care:** `assert ad.title in body` is only safe when the factory default is
distinctive enough to fail if the field were dropped. A default of `""` or `"x"`
makes the assertion vacuous — keep an explicit literal in that case.

### 5. `override_settings` as a context manager wrapping the whole body

```python
def test_x(client):
    with override_settings(DEBUG=True, LEOLIST_FIXTURE_DIR=str(FIXTURES)):
        ...
```

```python
@override_settings(DEBUG=True, LEOLIST_FIXTURE_DIR=str(FIXTURES))
def test_x(client):
    ...
```

The decorator form reads as a precondition rather than as control flow. Use the
context-manager form only when the override must apply to *part* of the body
(e.g. asserting behavior differs inside vs. outside). If the same override
appears on most tests in a file, promote it to a fixture or
`pytestmark = pytest.mark.django_db` -style module-level marker.

### 6. Over-mocking

Mocking the very thing under test, or patching internals so thoroughly that the
test passes against a broken implementation. Mock at the process boundary
(network, clock, filesystem, third-party SDK) and let the real code run inside
it. A test that patches a pure function to return its expected output is
testing `unittest.mock`.

### 7. Multiple unrelated behaviors in one test

A test named `test_ad_page` that checks rendering, then permissions, then the
404 path, fails as one unit and hides the other two. Split by behavior. The
counterpart smell is a name that doesn't say what's being verified
(`test_it_works`, `test_case_2`) — rename to `test_<subject>_<condition>_<expectation>`.

### 8. Interdependent or order-dependent tests

Shared module-level mutable state, tests that rely on an earlier test's DB rows,
missing `django_db` transaction isolation. Verify with `pytest -p no:randomly`
off vs on, or by running a single test file alone.

### 9. Assertions that can't fail, and swallowed failures

`assert True`, `assert x == x`, an `except Exception: pass` around the act step,
`pytest.raises` with no `match=` on a broad exception type (it passes on the
wrong error), and tests whose assertions live after an early `return`.

### 10. Fragile coupling to incidental detail

Asserting on whole rendered HTML blobs, exact log strings, dict ordering, or
`datetime.now()` without freezing time. These fail on unrelated changes and
train people to ignore red. Assert on the semantic thing (a parsed element, a
field value) instead.

### 11. Copy-pasted setup that should be a fixture

Four tests that each build the same three objects want a fixture (or a factory
with a trait). Conversely: a giant `conftest.py` fixture used by two tests is
misplaced indirection — push it back down to the file that needs it.

## Rules

- **Never weaken a test to make it pass.** If a test is failing before you
  start, report it; don't fold it into the refactor.
- **Deletions need a stated reason** in the summary. When unsure whether a test
  earns its keep, leave it and flag it rather than deleting silently.
- **Preserve behavior coverage.** Re-run coverage after the pass and compare.
- **Match the project.** Existing style and CLAUDE.md conventions outrank this
  catalogue where they conflict.
- **Readability over cleverness** — the point is tests that a reader trusts.
