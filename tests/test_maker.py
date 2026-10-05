"""outline-maker-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from maker import (  # noqa: E402
    make_rule_outline, make_outline, outline_with_llm, render_text, SECTIONS,
)


class TestRule(unittest.TestCase):
    def test_structure(self):
        out = make_rule_outline("人工智能")
        self.assertEqual(len(out), len(SECTIONS))
        self.assertTrue(all("人工智能" in s["section"] for s in out))
        self.assertTrue(all(len(s["subsections"]) >= 2 for s in out))

    def test_hierarchy(self):
        out = make_rule_outline("咖啡")
        self.assertIn("subsections", out[0])
        self.assertIsInstance(out[0]["subsections"][0], str)


class TestNoKey(unittest.TestCase):
    def test_fallback_rule(self):
        r = make_outline("机器学习", use_llm=True)
        self.assertEqual(r["source"], "rule")
        self.assertIsNotNone(r["outline"])

    def test_llm_none_without_key(self):
        self.assertIsNone(outline_with_llm("主题"))

    def test_render(self):
        r = make_outline("旅游", use_llm=False)
        text = render_text(r)
        self.assertIn("# 《旅游》", text)


if __name__ == "__main__":
    unittest.main()
