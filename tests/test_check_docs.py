"""Exercise real temporary repositories, including intentionally broken files."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_docs.py"
spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DocumentationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("docs-check.json", '{"inventories": []}')

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def errors(self):
        return checker.check_repository(self.root)

    def test_inline_encoded_nested_and_html_destinations(self):
        self.write("README.md", '[one](<notes/a file.md#part>)\n[two](notes/a%20file.md#part "title")\n[three](notes/a(b).md)\n<img src="diagram.svg"><a href="notes/a(b).md">go</a>')
        self.write("notes/a file.md", '<a id="part"></a>\n# Title')
        self.write("notes/a(b).md", "# Nested name")
        self.write("diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.assertEqual([], self.errors())

    def test_parentheses_inside_titles_and_angle_destinations_are_checked(self):
        cases = [
            '[broken](missing.md "Chapter (draft")',
            '[broken](missing.md "Chapter )draft")',
            "[broken](missing.md 'Chapter (draft')",
            '[broken](<missing(.md>)',
            '![broken](<missing).svg> "Chapter (draft")',
        ]
        for text in cases:
            with self.subTest(text=text):
                self.write("README.md", "# Intro\n" + text)
                errors = self.errors()
                self.assertEqual(1, len(errors), errors)
                self.assertIn("README.md:2: missing target:", errors[0])
        self.write("README.md", '[ok](<notes/a(b.md> "Chapter (draft")')
        self.write("notes/a(b.md", "# OK")
        self.assertEqual([], self.errors())

    def test_quoted_title_does_not_hide_missing_fragment(self):
        self.write("README.md", '[broken](notes.md#missing "Chapter (draft")')
        self.write("notes.md", '<a id="present"></a>')
        errors = self.errors()
        self.assertEqual(1, len(errors), errors)
        self.assertIn("README.md:1: missing fragment: notes.md#missing", errors[0])

    def test_comment_markers_in_fenced_code_do_not_hide_live_links(self):
        self.write("README.md", "```html\n<!--\n```\n[broken](missing.md)\n```html\n-->\n```\n")
        errors = self.errors()
        self.assertEqual(1, len(errors), errors)
        self.assertIn("README.md:4: missing target: missing.md", errors[0])

    def test_comment_markers_in_inline_code_do_not_hide_live_links(self):
        self.write("README.md", "`<!--`\n[broken](missing.md)\n`-->`\n")
        errors = self.errors()
        self.assertEqual(1, len(errors), errors)
        self.assertIn("README.md:2: missing target: missing.md", errors[0])

    def test_real_comments_with_code_markers_do_not_hide_following_links(self):
        self.write("README.md", "<!--\n```\n`\n[hidden](absent.md)\n-->\n[broken](missing.md)\n")
        errors = self.errors()
        self.assertEqual(1, len(errors), errors)
        self.assertIn("README.md:6: missing target: missing.md", errors[0])

    def test_missing_file_image_and_html_report_source_line(self):
        self.write("README.md", '# Intro\n[text](gone.md)\n![plot](gone.svg)\n<img src="gone.png">')
        errors = self.errors()
        self.assertEqual(3, len(errors), errors)
        self.assertTrue(any("README.md:2" in e and "gone.md" in e for e in errors))

    def test_reference_links_collapsed_shortcut_and_missing_definition(self):
        self.write("README.md", '[full][A]\n![A][]\n[A]\n[bad][undefined]\n\n[A]: <notes/ok.md> "A title"')
        self.write("notes/ok.md", "# OK")
        self.assertEqual(1, len(self.errors()), self.errors())
        self.assertIn("undefined reference", self.errors()[0])
        self.write("notes/ok.md", '[broken](missing.md)')
        self.assertTrue(any("notes/ok.md:1" in e for e in self.errors()))

    def test_ignores_fences_inline_code_comments_and_external_urls(self):
        self.write("README.md", '```md\n[x](missing.md)\n```\n~~~\n<img src="no.svg">\n~~~\n`[x](missing.md)` and `` `[x](missing.md)` ``\n<!-- [x](missing.md) -->\n[x](https://example.test/no.md) [m](mailto:a@example.test)')
        self.assertEqual([], self.errors())

    def test_fragments_explicit_ids_plain_headings_and_svg(self):
        self.write("README.md", '[h](notes.md#plain-title) [i](notes.md#stable) [s](plot.svg#point)')
        self.write("notes.md", '# Plain Title\n<a id="stable"></a>')
        self.write("plot.svg", '<svg xmlns="http://www.w3.org/2000/svg"><g id="point"/></svg>')
        self.assertEqual([], self.errors())
        self.write("notes.md", '# Renamed\n<a id="stable"></a>')
        self.assertTrue(any("missing fragment" in e and "plain-title" in e for e in self.errors()))

    def test_rejects_escape_including_symlink(self):
        self.write("README.md", '[outside](../outside.md) [encoded](%2e%2e/outside.md)')
        self.assertEqual(2, len(self.errors()))
        with tempfile.TemporaryDirectory() as other:
            external = Path(other) / "secret.md"
            external.write_text("secret", encoding="utf-8")
            (self.root / "shortcut.md").symlink_to(external)
            self.write("README.md", '[outside](shortcut.md)')
            self.assertTrue(any("outside repository" in e for e in self.errors()))

    def test_invalid_unlinked_svg_fails(self):
        self.write("README.md", "# No image link required")
        self.write("assets/broken.svg", '<svg><g></svg>')
        self.assertTrue(any("invalid SVG" in e for e in self.errors()))

    def test_file_inventory_drift_and_missing_navigation(self):
        config = {"inventories": [{"glob": "entries/*.md", "entries": ["entries/one.md"], "navigation": ["README.md"]}]}
        self.write("docs-check.json", json.dumps(config))
        self.write("entries/one.md", "# One")
        self.write("README.md", "# Index")
        self.assertTrue(any("navigation missing" in e for e in self.errors()))
        self.write("README.md", '[one](entries/one.md)')
        self.assertEqual([], self.errors())
        self.write("entries/two.md", "# Two")
        self.assertTrue(any("inventory differs" in e and "two.md" in e for e in self.errors()))
        (self.root / "entries/one.md").unlink()
        self.assertTrue(any("missing target" in e for e in self.errors()))

    def test_anchor_inventory_detects_unlisted_book_and_navigation(self):
        config = {"inventories": [{"anchor_file": "books.md", "anchor_prefix": "book-", "entries": ["books.md#book-one"], "navigation": ["guide.md"]}]}
        self.write("docs-check.json", json.dumps(config))
        self.write("books.md", '<a id="book-one"></a>')
        self.write("guide.md", '[one](books.md#book-one)')
        self.assertEqual([], self.errors())
        self.write("books.md", '<a id="book-one"></a>\n<a id="book-two"></a>')
        self.assertTrue(any("inventory differs" in e and "book-two" in e for e in self.errors()))

    def test_unused_reference_definition_is_not_navigation(self):
        config = {"inventories": [{"glob": "entries/*.md", "entries": ["entries/one.md"], "navigation": ["README.md"]}]}
        self.write("docs-check.json", json.dumps(config))
        self.write("entries/one.md", "# One")
        self.write("README.md", "[one]: entries/one.md")
        self.assertTrue(any("navigation missing" in e for e in self.errors()))
        self.write("README.md", "[one]\n\n[one]: entries/one.md")
        self.assertEqual([], self.errors())

    def test_reference_target_reports_each_actual_use(self):
        self.write("README.md", "[full][x]\n![x][]\n[x]\n\n[x]: gone.md")
        errors = self.errors()
        self.assertEqual(3, len(errors), errors)
        for line in range(1, 4):
            self.assertTrue(any(f"README.md:{line}:" in e and "gone.md" in e for e in errors))

    def test_invalid_manifest_and_cli_exit_status(self):
        self.write("docs-check.json", "{")
        self.assertTrue(any("manifest" in e for e in self.errors()))
        self.write("docs-check.json", '{"inventories": []}')
        self.write("README.md", '[bad](gone.md)')
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        self.assertIn("gone.md", result.stdout + result.stderr)
        self.write("README.md", "# OK")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
