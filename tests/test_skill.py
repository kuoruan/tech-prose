"""Regression tests for the skill's two bundled checkers.

Run with: python3 -m unittest discover -s tests
"""

import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "skills" / "tech-prose" / "scripts" / "check_rewrite.py"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "tech-prose" / "scripts"))
import check_rewrite  # noqa: E402
import validate  # noqa: E402


def write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, body in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body.encode("utf-8") if isinstance(body, str) else body)


def run_check(original: str, rewritten: str, ext: str = ".md") -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        a = Path(tmp, "a" + ext)
        b = Path(tmp, "b" + ext)
        a.write_text(original, encoding="utf-8")
        b.write_text(rewritten, encoding="utf-8")
        done = subprocess.run(
            [sys.executable, str(CHECK), str(a), str(b)],
            capture_output=True,
            text=True,
        )
    return done.returncode, done.stdout


class CheckRewriteTest(unittest.TestCase):
    def test_identical_text_passes(self):
        code, out = run_check("上限 500 条。", "上限 500 条。")
        self.assertEqual(code, 0, out)

    def test_weakened_modality_is_flagged(self):
        code, out = run_check("Callers must retry.", "Callers should retry.")
        self.assertEqual(code, 1, out)
        self.assertIn("normativity", out)

    def test_modal_case_change_is_not_flagged(self):
        code, out = run_check("Callers MUST retry.", "Callers must retry.")
        self.assertEqual(code, 0, out)

    def test_changed_limit_is_flagged(self):
        code, out = run_check("上限 500 条。", "上限 5000 条。")
        self.assertEqual(code, 1, out)
        self.assertNotIn("500", check_rewrite.facts("上限 5000 条。"))
        self.assertIn("500", check_rewrite.facts("上限 500 条。"))

    def test_chinese_numeral_replaced_is_flagged(self):
        code, out = run_check("重试次数不能超过三次。", "重试次数最多 5 次。")
        self.assertEqual(code, 1, out)
        self.assertIn("三", check_rewrite.facts("重试次数不能超过三次。"))
        self.assertNotIn("三", check_rewrite.facts("重试次数最多 5 次。"))

    def test_determiner_is_not_a_numeral(self):
        code, out = run_check("每一个模块都必须登记。", "每个模块都必须登记。")
        self.assertEqual(code, 0, out)

    def test_reduced_hedging_is_flagged(self):
        code, out = run_check("可能失败。可能延迟。可能重试。", "可能失败。")
        self.assertEqual(code, 1, out)
        self.assertIn("lost=['可能']", out)

    def test_ordinary_words_are_not_hedging(self):
        self.assertEqual(check_rewrite.uncertainty("并发约束：最多 4 个连接。"), {})
        self.assertEqual(check_rewrite.uncertainty("等待中，需要重试。"), {})

    def test_english_hedge_forms_are_recognised(self):
        code, out = run_check("It is assumed that the lock is held.", "The lock is held.")
        self.assertEqual(code, 1, out)
        self.assertIn("uncertainty", out)

    def test_fabricated_name_is_flagged(self):
        code, out = run_check("It fails with an error.", "It fails with a ValueError.")
        self.assertEqual(code, 1, out)
        self.assertIn("ValueError", out)

    def test_language_switch_is_flagged(self):
        code, out = run_check(
            "部署说明：服务重启需要 30 秒。",
            "Deployment notes: the service restarts in 30 seconds.",
        )
        self.assertEqual(code, 1, out)
        self.assertIn("LANGUAGE SWITCHED", out)

    def test_comment_only_change_keeps_code_identity(self):
        code, out = run_check(
            "def f():\n    return 1  # 旧注释\n", "def f():\n    return 1  # 新注释\n", ".py"
        )
        self.assertEqual(code, 0, out)
        self.assertIn("UNCHANGED", out)

    def test_changed_code_is_flagged(self):
        code, out = run_check("def f():\n    return 1\n", "def f():\n    return 2\n", ".py")
        self.assertEqual(code, 1, out)
        self.assertIn("CHANGED", out)

    def test_unparsable_output_is_flagged(self):
        code, out = run_check("def f():\n    return 1\n", "def f(:\n", ".py")
        self.assertEqual(code, 1, out)
        self.assertIn("DOES NOT PARSE", out)

    def test_wrong_usage_exits_with_2(self):
        done = subprocess.run([sys.executable, str(CHECK)], capture_output=True, text=True)
        self.assertEqual(done.returncode, 2, done.stderr)
        self.assertIn("Usage:", done.stderr)

    def test_unreadable_input_exits_with_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp, "missing.md")
            done = subprocess.run(
                [sys.executable, str(CHECK), str(missing), str(missing)],
                capture_output=True,
                text=True,
            )
        self.assertEqual(done.returncode, 2, done.stderr)
        self.assertIn("cannot read input", done.stderr)


class ReferenceResolutionTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "skill"
        write_tree(
            self.root,
            {
                "references/carriers/ui-copy.md": "x",
                "references/languages/en.md": "x",
            },
        )
        self.carrier = self.root / "references" / "carriers" / "documentation.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_bare_name_resolves_in_same_directory(self):
        self.assertTrue(validate.ref_resolves(self.root, self.carrier, "ui-copy.md"))

    def test_bare_name_in_another_directory_does_not_resolve(self):
        self.assertFalse(validate.ref_resolves(self.root, self.carrier, "en.md"))

    def test_full_path_resolves_from_skill_root(self):
        self.assertTrue(
            validate.ref_resolves(self.root, self.carrier, "references/languages/en.md")
        )

    def test_missing_target_does_not_resolve(self):
        self.assertFalse(validate.ref_resolves(self.root, self.carrier, "ui-copy-missing.md"))
        self.assertFalse(
            validate.ref_resolves(self.root, self.carrier, "references/languages/missing.md")
        )

    def test_generic_name_is_skipped(self):
        self.assertTrue(validate.ref_resolves(self.root, self.carrier, "AGENTS.md"))

    def test_full_path_does_not_fall_back_to_references(self):
        (self.root / "references" / "languages" / "en.md").unlink()
        write_tree(self.root, {"references/references/languages/en.md": "x"})
        self.assertFalse(
            validate.ref_resolves(self.root, self.carrier, "references/languages/en.md")
        )

    def test_directory_with_reference_name_is_not_a_target(self):
        (self.root / "references" / "carriers" / "missing.md").mkdir()
        self.assertFalse(validate.ref_resolves(self.root, self.carrier, "missing.md"))


class CheckSkillTest(unittest.TestCase):
    def check(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(root / "demo", files)
            errors: list[str] = []
            with unittest.mock.patch.object(validate, "ROOT", root):
                validate.check_skill(root / "demo", errors)
        return errors

    def test_broken_bare_reference_is_reported(self):
        errors = self.check(
            {
                "SKILL.md": "---\nname: demo\ndescription: demo skill\n---\n\nbody\n",
                "references/carriers/documentation.md": "错误信息见 `ui-copy-NOPE.md`。\n",
            }
        )
        self.assertTrue(errors)
        self.assertIn("ui-copy-NOPE.md", errors[0])

    def test_broken_prefixed_reference_is_reported(self):
        errors = self.check(
            {
                "SKILL.md": "---\nname: demo\ndescription: demo skill\n---\n\nbody\n",
                "references/carriers/documentation.md": "见 `references/carriers/nope.md`。\n",
            }
        )
        self.assertTrue(any("nope.md" in e for e in errors), errors)

    def test_missing_skill_file_is_reported(self):
        errors = self.check({"references/carriers/documentation.md": "正文\n"})
        self.assertTrue(errors)
        self.assertIn("SKILL.md", errors[0])

    def test_missing_frontmatter_is_reported(self):
        errors = self.check({"SKILL.md": "# demo\n"})
        self.assertTrue(any("frontmatter" in e for e in errors), errors)

    def test_name_mismatch_is_reported(self):
        errors = self.check({"SKILL.md": "---\nname: other\ndescription: d\n---\n"})
        self.assertTrue(any("目录名" in e for e in errors), errors)

    def test_absolute_path_is_reported(self):
        errors = self.check(
            {
                "SKILL.md": "---\nname: demo\ndescription: demo skill\n---\n",
                "references/carriers/documentation.md": "见 /home/someone/notes.md。\n",
            }
        )
        self.assertTrue(any("绝对路径" in e for e in errors), errors)

    def test_unparsable_script_is_reported(self):
        errors = self.check(
            {
                "SKILL.md": "---\nname: demo\ndescription: demo skill\n---\n",
                "scripts/broken.py": "def f(:\n",
            }
        )
        self.assertTrue(any("无法编译" in e for e in errors), errors)

    def test_unreadable_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "demo"
            write_tree(skill, {"SKILL.md": "---\nname: demo\ndescription: d\n---\n"})
            (skill / "references").mkdir()
            (skill / "references" / "bad.md").write_bytes(b"\xff\xfe")
            errors: list[str] = []
            with unittest.mock.patch.object(validate, "ROOT", root):
                validate.check_skill(skill, errors)
        self.assertTrue(any("无法按 UTF-8 读取" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
