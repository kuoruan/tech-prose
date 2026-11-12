#!/usr/bin/env python3
"""Compare an original text/code sample against a rewritten version.

Flags potential rewrite regressions for human review:
  1. concrete facts   - digits, Chinese numerals with a counter, identifiers
  2. normativity      - MUST/SHOULD/MAY, must/should/may, 必须/建议/允许/可以/不得/禁止
  3. uncertainty      - hedges, unverified markers, ranges
  4. code identity    - for .py, AST unchanged after dropping docstrings (comments ignored)
  5. similarity       - descriptive only, never affects the exit code
  6. fabricated names - exception types and API names absent from the original
  7. language drift   - a substantial change in CJK/Latin mix, not proof of translation

Usage: python3 check_rewrite.py <original> <rewritten>
Exit code 0 = no check flagged anything, 1 = at least one did,
2 = the script was called with wrong arguments or an unreadable file.

KNOWN LIMITS - this is a filter for human review, not a verdict:
  - Normativity counts words case-insensitively, so a legitimate translation
    of MUST into 必须 reads as a loss, and a narrator phrase like 我们可以发现
    reads as a normative 可以 that went missing. Confirm each hit by hand.
    Other modal phrasing (is required to, can) does not count. The same
    matching makes the month May look like a permission.
  - Chinese numerals are recognised only in front of a counter (次, 秒, 个,
    ...), and not after a determiner such as 每, 另 or 某. Normalising
    三次 to 3 次, or inserting a space before the counter, is therefore
    reported as a lost fact.
  - Uncertainty is compared as a count, so a rewrite that keeps one 可能
    while deleting four is flagged. Only a reduction of a known marker is
    caught: adding a hedge is not checked, and swapping one hedge for
    another may be reported as the original marker going missing.
    The patterns are deliberate phrases (待确认, 需要压测, 约 5) rather than
    bare 待/约/需要, because those characters occur inside ordinary words
    (约束, 约定, 等待).
  - Facts are compared as a set of tokens, so the check does not know which
    number belongs to which subject, nor how many times a number repeats;
    swapping 500 between two sentences, or dropping a duplicate 3, passes.
    Backtick matching can span lines and fence delimiters, treating prose as
    an identifier. Review those matches manually.
  - Fabricated names flags recognised name patterns found only in the rewrite.
    A legitimate name may be flagged if its original mention did not match
    those patterns. A hit means "check whether this was invented", not
    "this is a lie".
  - Similarity is descriptive only. A low score is not a defect and a high
    score is not a pass; light touch is correct on text that was already fine.
  - Numeric grouping is not understood: 1,000 becomes the tokens 1 and 000,
    so a rewrite that writes 1000 is reported as two lost facts.
  - Nothing here judges prose quality. These checks flag selected signs of
    lost or invented information; they do not cover every kind of change.
"""
import ast
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

NUM = re.compile(r"\d+(?:\.\d+)*%?")
CJK_NUM = re.compile(
    r"(?<![每另某统同任哪])[一二三四五六七八九十百千万零两]+"
    r"(?=次|秒|分钟|小时|天|周|月|年|条|个|项|人|台|页|级|MB|GB|KB|%)"
)
IDENT = re.compile(r"`([^`]+)`")
# names a rewrite can fabricate: exception types, sphinx roles, API names
CLAIM = re.compile(r"(?::(?:class|exc|raises|rtype):\s*`?([A-Za-z_][\w.]*))|\b([A-Z][A-Za-z]*(?:Error|Exception))\b")
CJK = re.compile(r"[\u4e00-\u9fff]")
NORMATIVE = [
    "must", "should", "may",
    "必须", "建议", "允许", "可以", "不得", "禁止",
]
UNCERTAIN = [
    "可能", "尚未", "未验证", "未测量", "初步", "大致", "通常",
    "待确认", "待定", "需要确认", "需要压测",
    r"约\s*\d",
    "usually", "can still", "advisory", "may", "might", "expected",
    "assume", "assumes", "assumed", "assuming", "assumption", "assumptions",
    "not measured", "not verified",
]


def count(text: str, term: str) -> int:
    if term.isascii():
        return len(re.findall(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", text, re.I))
    return len(re.findall(term, text))


def facts(text):
    return set(NUM.findall(text)) | set(CJK_NUM.findall(text)) | set(IDENT.findall(text))


def normativity(text):
    counts = {}
    for term in NORMATIVE:
        n = count(text, term)
        if n:
            counts[term.lower() if term.isascii() else term] = n
    return counts


def uncertainty(text):
    return {w: n for w in UNCERTAIN if (n := count(text, w))}


def claims(text):
    return {a or b for a, b in CLAIM.findall(text)}


def lang_mix(text):
    letters = sum(1 for ch in text if ch.isalpha())
    return len(CJK.findall(text)) / letters if letters else 0.0


def code_shape(path):
    src = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        # drop docstrings, keep everything else
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    if hasattr(ast, "unparse"):
        return ast.unparse(tree)
    return ast.dump(tree)


def main():
    if len(sys.argv) != 3:
        print("Usage: check_rewrite.py <original> <rewritten>", file=sys.stderr)
        return 2
    orig_p, out_p = sys.argv[1], sys.argv[2]
    try:
        orig = Path(orig_p).read_text(encoding="utf-8")
        out = Path(out_p).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"cannot read input: {e}", file=sys.stderr)
        return 2
    ok = True

    f_orig, f_out = facts(orig), facts(out)
    lost = sorted(f_orig - f_out)
    print(f"[1] facts: {len(f_orig)} in original, lost={lost or 'NONE'}")
    if lost:
        ok = False

    n_orig, n_out = normativity(orig), normativity(out)
    print(f"[2] normativity orig={n_orig} out={n_out}")
    if n_orig != n_out:
        ok = False

    u_orig, u_out = uncertainty(orig), uncertainty(out)
    lost_u = sorted(w for w, n in u_orig.items() if u_out.get(w, 0) < n)
    print(f"[3] uncertainty orig={sum(u_orig.values())} out={sum(u_out.values())} lost={lost_u or 'NONE'}")
    if lost_u:
        ok = False

    if orig_p.endswith(".py"):
        try:
            same = code_shape(orig_p) == code_shape(out_p)
        except SyntaxError as e:
            print(f"[4] code identity: OUTPUT DOES NOT PARSE ({e})")
            ok = False
        else:
            print(f"[4] code identity (comments ignored): {'UNCHANGED' if same else 'CHANGED'}")
            if not same:
                ok = False
    else:
        print("[4] code identity: n/a")

    ratio = SequenceMatcher(None, orig, out).ratio()
    print(f"[5] similarity: {ratio:.2f}  (descriptive only: high = light touch, low = heavy rewrite)")

    new_c = sorted(claims(out) - claims(orig))
    print(f"[6] fabricated claims: {new_c or 'NONE'}")
    if new_c:
        ok = False

    lo, ln = lang_mix(orig), lang_mix(out)
    drift = abs(lo - ln)
    print(f"[7] language mix: orig CJK={lo:.2f} out={ln:.2f} drift={drift:.2f}"
          f"{'' if drift < 0.2 else '  <-- LANGUAGE SWITCHED'}")
    if drift >= 0.2:
        ok = False

    print(f"\nRESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
