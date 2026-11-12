[简体中文](README.md) | **English**

# Tech Prose

An agent skill that reviews, edits and drafts technical writing. It covers documentation, code comments and docstrings, interface and CLI copy, commit messages and PR descriptions, changelogs and release notes, and AI instruction files. It works in Chinese and English.

By default it changes only the wording, never the facts: numbers, versions, limits, identifiers, paths, and normative strength (`MUST` / `SHOULD` / `MAY`) are preserved verbatim. Structural problems are raised as suggestions; acting on them requires an explicit request.

## Installation

Requires Node.js 22.20 or later.

```bash
npx skills add kuoruan/tech-prose           # choose target agents interactively
npx skills add kuoruan/tech-prose -g        # install globally, for all projects
npx skills add kuoruan/tech-prose --skill tech-prose -a claude-code
```

Install paths follow the `skills` CLI conventions: Claude Code writes to `.claude/skills/`; Codex, Cursor, Pi and others write to `.agents/skills/`. Add `-g` to write into your user directory instead. For other agents, see the [skills CLI agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

To try it without installing:

```bash
npx skills use kuoruan/tech-prose@tech-prose
```

## How to use it

Once installed, describe what you want. The output depends on the request.

A review lists problems and changes no files:

```text
Look over this deployment doc and tell me what's wrong with it. Don't change anything yet.
```

The output is `path:line` plus the problem, the evidence and a suggestion.

An edit returns rewritten text:

```text
Tighten this installation section. Leave the numbers and versions alone.
```

With no source text, a drafting request returns the text itself:

```text
Write the API reference for this endpoint, following the code as it stands.
```

The `description` in `SKILL.md` limits the skill to requests that explicitly ask for reviewing, editing, trimming or drafting technical writing; ordinary coding, debugging and refactoring are outside it. Whether it triggers automatically depends on the agent you use.

## What it fixes

| Problem | What the skill does |
| --- | --- |
| AI voice: filler openers, “not X but Y”, triads, vague praise, invented significance | Removes what carries no information, or replaces it with the actual fact or condition |
| Semantic links broken while rewording: condition scope, negation scope, causality, referents | Checks that all four survive the rewrite |
| Fact drift: numbers, versions, `MUST`/`SHOULD` strength, hedging quietly turned into certainty | Keeps them verbatim; an optional script flags what a reviewer must re-check |
| Overreach: reading “too long”, “trim it” or “make it readable” as permission to move sections | Changes wording only, and lists structural issues as suggestions |

## Example rewrite

This pair was written by hand, not produced by a model run. The defects sit in two framing sentences (the Chinese version also drops one nominalized phrase); the sentences carrying the technical facts are unchanged.

Before:

> As the business has grown, the cache layer has become a critical pillar that simply cannot be ignored. It isn't just a cache — it's the foundation of stability. To improve reliability, we recommend optimizing the existing invalidation strategy: when no fallback is configured, a cache miss causes the request to fail; only when a fallback is configured does the service degrade. Retries must not exceed 3.

After:

> To improve reliability, we recommend optimizing the existing invalidation strategy: when no fallback is configured, a cache miss causes the request to fail; only when a fallback is configured does the service degrade. Retries must not exceed 3.

Removed: two framing sentences — a staged opener carrying `cannot be ignored`, and the “It isn't just a cache — it's the foundation of stability” foil.

Everything else is unchanged: the purpose, both conditions, the “only when” link between them, and the limit of 3.

`check_rewrite.py` reports `RESULT: PASS` for this pair. It flags items for human review; it does not judge semantic equivalence.

## What it won't do

- Refactor code or change a public API contract; trimming a comment is not a refactor.
- Switch languages on its own. Optimising the English half of a mixed document does not translate it into Chinese.
- Invent missing details: if the exception type, concurrency guarantee or boundary behaviour is not in the source material, the detail becomes a listed gap.
- Drop limitations, prerequisites, exceptions or rollback steps.
- Reorder sections or split a document unless you ask for it.

## Layout

```
skills/tech-prose/
├── SKILL.md                    Entry point: action selection, protected boundaries, on-demand loading, self-check
├── references/
│   ├── carriers/               Carrier rules: documentation / comments / UI copy / CLI output / AI instructions / commit messages / changelogs and release notes
│   ├── languages/              Language rules: Chinese / English
│   └── tasks/structure.md      Structural changes (on explicit request only)
└── scripts/check_rewrite.py    Flags 7 categories for review: facts, normative strength, hedging, code consistency and more
```

The repository root also holds `scripts/validate.py`, `tests/`, `evals/`, `.claude-plugin/` and `.github/workflows/`.

The carrier rules focus on what to write; the language rules focus on how. `SKILL.md` holds only the criteria shared across carriers, and each carrier file documents just its differences.

## Updates

```bash
npx skills check    # check for a new version
npx skills update   # update installed skills
```

## Development

```bash
python3 scripts/validate.py                    # validate frontmatter, reference paths, leaked absolute paths, script compilation
python3 skills/tech-prose/scripts/check_rewrite.py <original> <rewritten>
python3 -m unittest discover -s tests -v       # regression tests for both checkers
```

For manual behavior and trigger evaluations, see [evals/README.md](evals/README.md) (in Chinese). Run results are recorded separately from the cases. Passing checker tests does not validate model behavior; the manual evaluations are not part of CI.

When bumping the version, change `metadata.version` in `SKILL.md` and `.claude-plugin/marketplace.json` together.

Before changing a rule, read the “three checks before editing” section in `skills/tech-prose/SKILL.md`, and keep paths inside `references/` relative to `SKILL.md`. CI runs the same validation on every push and pull request.

## License

MIT
