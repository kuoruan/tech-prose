#!/usr/bin/env python3
"""Validate the skill repository layout.

Checks, without third-party dependencies:
  1. every skills/*/SKILL.md has the required frontmatter and a name matching its folder
  2. every file path referenced from a skill's markdown exists inside that skill
  3. no absolute paths leak into skill content
  4. every bundled Python script compiles

Exit code 0 when all checks pass, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Relative paths that must resolve inside the skill folder when mentioned.
REF_RE = re.compile(
    r"(?:references/)?(?:carriers|languages|tasks)/[A-Za-z0-9_.\-]+\.md"
    r"|scripts/[A-Za-z0-9_.\-]+\.py"
)
# Bare file names, written as `en.md` or `ui-copy.md` inside another reference.
BARE_REF = re.compile(r"`([A-Za-z0-9_.\-]+\.(?:md|py))`")
# Names that may refer to files outside this skill.
GENERIC_REF = {"AGENTS.md", "CLAUDE.md", "README.md", "README.en.md", "CHANGELOG.md", "SKILL.md"}
ABS_RE = re.compile(r"(?<![\w.])/(?:home|Users|root)/\S+")


def read_text(path: Path) -> str | None:
    """Read a file as UTF-8, or return None when it cannot be read."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def line_of(text: str, position: int) -> int:
    return text[:position].count("\n") + 1


def refs_in(text: str) -> list[tuple[str, int]]:
    """Every reference in a markdown file, with its offset."""
    found = [(m.group(0), m.start()) for m in REF_RE.finditer(text)]
    found += [(m.group(1), m.start()) for m in BARE_REF.finditer(text)]
    return found


def ref_resolves(skill_dir: Path, md: Path, ref: str) -> bool:
    """Resolve a reference the way the reader would.

    A ref containing a slash is resolved from the skill root; a bare file
    name is resolved from the directory of the file that mentions it.
    """
    if "/" not in ref and ref in GENERIC_REF:
        return True
    if "/" in ref:
        return (skill_dir / ref).is_file()
    return (md.parent / ref).is_file()


def frontmatter(text: str) -> dict[str, str] | None:
    """Parse simple `key: value` frontmatter. Block scalars are not handled."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
    return fields


def check_skill(skill_dir: Path, errors: list[str]) -> None:
    rel = skill_dir.relative_to(ROOT)
    skill_md = skill_dir / "SKILL.md"
    text = read_text(skill_md)
    if text is None:
        errors.append(f"{rel}: 缺少或无法读取 SKILL.md")
        return

    fields = frontmatter(text)
    if fields is None:
        errors.append(f"{rel}/SKILL.md: 缺少 YAML frontmatter")
    else:
        for key in ("name", "description"):
            if not fields.get(key):
                errors.append(f"{rel}/SKILL.md: frontmatter 缺少 {key}")
        name = fields.get("name", "")
        if name and not NAME_RE.match(name):
            errors.append(f"{rel}/SKILL.md: name `{name}` 不符合小写连字符格式")
        if name and name != skill_dir.name:
            errors.append(f"{rel}: name `{name}` 与目录名 `{skill_dir.name}` 不一致")

    for md in sorted(skill_dir.rglob("*.md")):
        body = read_text(md)
        if body is None:
            errors.append(f"{md.relative_to(ROOT)}: 无法按 UTF-8 读取")
            continue
        reported: set[str] = set()
        for ref, position in refs_in(body):
            if ref in reported or ref_resolves(skill_dir, md, ref):
                continue
            reported.add(ref)
            errors.append(f"{md.relative_to(ROOT)}:{line_of(body, position)}: 引用不存在 `{ref}`")
        for match in ABS_RE.finditer(body):
            line = line_of(body, match.start())
            errors.append(f"{md.relative_to(ROOT)}:{line}: 出现绝对路径 `{match.group(0)}`")

    for script in sorted(skill_dir.rglob("*.py")):
        source = read_text(script)
        if source is None:
            errors.append(f"{script.relative_to(ROOT)}: 无法按 UTF-8 读取")
            continue
        try:
            compile(source, str(script), "exec")
        except SyntaxError as exc:
            errors.append(f"{script.relative_to(ROOT)}: 无法编译: {exc.msg}")


def main() -> int:
    skills_dir = ROOT / "skills"
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    if not skill_dirs:
        print("FAIL: skills/ 下没有技能目录")
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        check_skill(skill_dir, errors)

    for err in errors:
        print(f"FAIL {err}")
    if errors:
        return 1
    print(f"PASS {len(skill_dirs)} 个技能，引用与脚本检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
