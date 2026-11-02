"""Tests for tools/release_notes.py. Run from the wiki root:

    python3 -m unittest discover -s tools/tests -t .
"""
from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from tools import release_notes as rn

BODY = '## ✨ New\n- **Thing:** it does a thing.\n\n## 🐛 Fixes\n- **Bug:** fixed.\n'

# What mkdocs.yml looks like right after the wipe (only the part the helper
# touches, plus the neighbours it must leave alone).
POST_WIPE_YML = """\
nav:
  - Support:
    - Troubleshooting: troubleshooting.md
    - Bot Commands: botcommands.md

  - Release Notes:
    - Overview: release-notes/index.md

  - Frequently Asked Questions: faq.md
  - Privacy Policy: privacy.md

# Theme Configuration
theme:
  name: material
"""


def nav_lines(text: str) -> list[str]:
    return text.split('\n')


class PageTextTests(unittest.TestCase):
    def test_app_header(self) -> None:
        text = rn.page_text('app', 'v1.4.1', date(2026, 11, 1), BODY, None)
        self.assertTrue(text.startswith(
            '# MeshMapper App v1.4.1\n\n*Released November 1, 2026*\n\n'))
        self.assertIn('## ✨ New', text)
        self.assertTrue(text.endswith('\n'))
        self.assertFalse(text.endswith('\n\n'))

    def test_server_covers_line(self) -> None:
        text = rn.page_text('server', 'v1.5.100', date(2026, 11, 1), BODY,
                            ('v1.5.10', 'v1.5.100'))
        self.assertTrue(text.startswith('# MeshMapper Server v1.5.100\n\n'))
        self.assertIn(
            '*Released November 1, 2026. Covers v1.5.10 to v1.5.100.*', text)

    def test_day_is_not_zero_padded(self) -> None:
        text = rn.page_text('app', 'v1.4.1', date(2026, 3, 5), BODY, None)
        self.assertIn('*Released March 5, 2026*', text)

    def test_unknown_product_raises(self) -> None:
        with self.assertRaises(ValueError):
            rn.page_text('web', 'v1.0.0', date(2026, 1, 1), BODY, None)


class CheckBodyTests(unittest.TestCase):
    def test_refuses_bad_bodies(self) -> None:
        for bad in ('{{ x }}', '{% if %}', '{# note #}', '# Title',
                    'a — b', '- no sections'):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    rn.check_body(bad)

    def test_macro_text_refused_even_with_sections(self) -> None:
        for token in ('{{', '{%', '{#'):
            with self.subTest(token=token):
                with self.assertRaises(ValueError):
                    rn.check_body('## ✨ New\n- uses ' + token + ' here\n')

    def test_title_line_refused_inside_valid_body(self) -> None:
        with self.assertRaises(ValueError):
            rn.check_body('# Title\n## ✨ New\n- **A:** b.')

    def test_hash_without_space_and_deeper_headings_are_fine(self) -> None:
        rn.check_body('## ✨ New\n- **A:** see #123.\n\n### Detail\n- x\n')

    def test_one_section_is_enough(self) -> None:
        rn.check_body('## ✨ New\n- **A:** b.')
        rn.check_body('## 🐛 Fixes\n- **A:** b.')

    def test_valid_body_passes(self) -> None:
        rn.check_body('## ✨ New\n- **A:** b.')
        rn.check_body(BODY)


class VersionKeyTests(unittest.TestCase):
    def test_rejects_malformed(self) -> None:
        for bad in ('1.4.1', 'v1.4', 'v1.4.1.2', 'v1.4.x', 'v1.4.1\n',
                    ' v1.4.1', 'V1.4.1', ''):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    rn.version_key(bad)

    def test_numeric_order(self) -> None:
        self.assertEqual(rn.version_key('v1.4.10'), (1, 4, 10))
        self.assertTrue(rn.version_key('v1.4.10') > rn.version_key('v1.4.9'))
        self.assertTrue(rn.version_key('v1.10.0') > rn.version_key('v1.9.9'))


class InsertNavTests(unittest.TestCase):
    def test_app_versions_sort_numerically_after_overview(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'app', 'v1.4.9')
        yml = rn.insert_nav(yml, 'app', 'v1.4.10')
        lines = nav_lines(yml)
        i_over = lines.index('    - Overview: release-notes/index.md')
        i_app = lines.index('    - App:')
        i_10 = lines.index('      - v1.4.10: release-notes/app/v1.4.10.md')
        i_9 = lines.index('      - v1.4.9: release-notes/app/v1.4.9.md')
        self.assertTrue(i_over < i_app < i_10 < i_9)
        self.assertNotIn('    - Server:', lines)

    def test_older_version_goes_below_newer(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'app', 'v1.4.10')
        yml = rn.insert_nav(yml, 'app', 'v1.4.9')
        lines = nav_lines(yml)
        self.assertLess(
            lines.index('      - v1.4.10: release-notes/app/v1.4.10.md'),
            lines.index('      - v1.4.9: release-notes/app/v1.4.9.md'))

    def test_middle_version_lands_between(self) -> None:
        yml = POST_WIPE_YML
        for v in ('v1.4.1', 'v1.4.20', 'v1.4.5'):
            yml = rn.insert_nav(yml, 'app', v)
        entries = [l.strip() for l in nav_lines(yml)
                   if l.startswith('      - v')]
        self.assertEqual(entries, [
            '- v1.4.20: release-notes/app/v1.4.20.md',
            '- v1.4.5: release-notes/app/v1.4.5.md',
            '- v1.4.1: release-notes/app/v1.4.1.md',
        ])

    def test_server_lands_after_app_subsection(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'app', 'v1.4.1')
        yml = rn.insert_nav(yml, 'app', 'v1.4.2')
        yml = rn.insert_nav(yml, 'server', 'v1.5.100')
        lines = nav_lines(yml)
        i_last_app = lines.index('      - v1.4.1: release-notes/app/v1.4.1.md')
        i_server = lines.index('    - Server:')
        i_srv_entry = lines.index(
            '      - v1.5.100: release-notes/server/v1.5.100.md')
        self.assertEqual(i_server, i_last_app + 1)
        self.assertEqual(i_srv_entry, i_server + 1)

    def test_app_added_after_server_still_precedes_server(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'server', 'v1.5.100')
        yml = rn.insert_nav(yml, 'app', 'v1.4.1')
        lines = nav_lines(yml)
        self.assertTrue(
            lines.index('    - Overview: release-notes/index.md')
            < lines.index('    - App:') < lines.index('    - Server:'))

    def test_rest_of_file_is_untouched(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'app', 'v1.4.1')
        yml = rn.insert_nav(yml, 'server', 'v1.5.100')
        before = POST_WIPE_YML.split('  - Release Notes:\n')
        after = yml.split('  - Release Notes:\n')
        self.assertEqual(before[0], after[0])
        # The blank line and everything after the block stay as they were.
        tail = '\n  - Frequently Asked Questions: faq.md'
        self.assertEqual(before[1][before[1].index(tail):],
                         after[1][after[1].index(tail):])
        self.assertIn('\n\n  - Frequently Asked Questions', yml)

    def test_same_version_twice_raises(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'app', 'v1.4.1')
        with self.assertRaises(ValueError):
            rn.insert_nav(yml, 'app', 'v1.4.1')

    def test_same_version_in_other_product_is_not_a_duplicate(self) -> None:
        yml = rn.insert_nav(POST_WIPE_YML, 'app', 'v1.4.1')
        rn.insert_nav(yml, 'server', 'v1.4.1')

    def test_bad_inputs_raise(self) -> None:
        with self.assertRaises(ValueError):
            rn.insert_nav(POST_WIPE_YML, 'app', '1.4.1')
        with self.assertRaises(ValueError):
            rn.insert_nav(POST_WIPE_YML, 'web', 'v1.4.1')
        with self.assertRaises(ValueError):
            rn.insert_nav('nav:\n  - Home: index.md\n', 'app', 'v1.4.1')

    def test_release_notes_block_at_end_of_file(self) -> None:
        yml = 'nav:\n  - Release Notes:\n    - Overview: release-notes/index.md\n'
        out = rn.insert_nav(yml, 'app', 'v1.0.0')
        self.assertEqual(out, yml + '    - App:\n'
                         '      - v1.0.0: release-notes/app/v1.0.0.md\n')


class CliTests(unittest.TestCase):
    """Drive main() against a scratch wiki tree."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'docs' / 'release-notes').mkdir(parents=True)
        (self.root / 'mkdocs.yml').write_text(POST_WIPE_YML, encoding='utf-8')
        self.notes = self.root / 'notes.md'
        self.notes.write_text(BODY, encoding='utf-8')
        patcher = mock.patch.object(rn, 'ROOT', self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_cli(self, *argv: str) -> tuple[int, str]:
        err = io.StringIO()
        with contextlib.redirect_stderr(err), \
                contextlib.redirect_stdout(io.StringIO()):
            code = rn.main(list(argv))
        return code, err.getvalue()

    def add(self, product: str = 'app', version: str = 'v1.4.1',
            *extra: str) -> tuple[int, str]:
        return self.run_cli(
            'add', '--product', product, '--version', version,
            '--date', '2026-11-01', '--notes-file', str(self.notes), *extra)

    def page(self, product: str, version: str) -> Path:
        return self.root / 'docs' / 'release-notes' / product / f'{version}.md'

    def test_add_writes_page_and_nav(self) -> None:
        code, _ = self.add()
        self.assertEqual(code, 0)
        text = self.page('app', 'v1.4.1').read_text(encoding='utf-8')
        self.assertTrue(text.startswith(
            '# MeshMapper App v1.4.1\n\n*Released November 1, 2026*\n\n'))
        yml = (self.root / 'mkdocs.yml').read_text(encoding='utf-8')
        self.assertIn('    - App:\n      - v1.4.1: release-notes/app/v1.4.1.md\n',
                      yml)

    def test_add_server_with_covers(self) -> None:
        code, _ = self.add('server', 'v1.5.100', '--covers', 'v1.5.10..v1.5.100')
        self.assertEqual(code, 0)
        text = self.page('server', 'v1.5.100').read_text(encoding='utf-8')
        self.assertIn('Covers v1.5.10 to v1.5.100.*', text)

    def test_existing_page_refused_without_replace(self) -> None:
        self.assertEqual(self.add()[0], 0)
        yml_before = (self.root / 'mkdocs.yml').read_text(encoding='utf-8')
        page_before = self.page('app', 'v1.4.1').read_text(encoding='utf-8')
        self.notes.write_text('## ✨ New\n- **Other:** text.\n', encoding='utf-8')
        code, err = self.add()
        self.assertNotEqual(code, 0)
        self.assertIn('exists', err)
        self.assertEqual(self.page('app', 'v1.4.1').read_text(encoding='utf-8'),
                         page_before)
        self.assertEqual((self.root / 'mkdocs.yml').read_text(encoding='utf-8'),
                         yml_before)

    def test_replace_rewrites_page_and_keeps_one_nav_line(self) -> None:
        self.assertEqual(self.add()[0], 0)
        self.notes.write_text('## ✨ New\n- **Other:** text.\n', encoding='utf-8')
        code, _ = self.add('app', 'v1.4.1', '--replace')
        self.assertEqual(code, 0)
        self.assertIn('**Other:**',
                      self.page('app', 'v1.4.1').read_text(encoding='utf-8'))
        yml = (self.root / 'mkdocs.yml').read_text(encoding='utf-8')
        self.assertEqual(yml.count('v1.4.1: release-notes/app/v1.4.1.md'), 1)

    def test_bad_body_writes_nothing(self) -> None:
        self.notes.write_text('## ✨ New\n- {{ boom }}\n', encoding='utf-8')
        code, err = self.add()
        self.assertNotEqual(code, 0)
        self.assertIn('{{', err)
        self.assertFalse(self.page('app', 'v1.4.1').exists())
        self.assertEqual((self.root / 'mkdocs.yml').read_text(encoding='utf-8'),
                         POST_WIPE_YML)

    def test_bad_arguments_fail(self) -> None:
        self.assertNotEqual(self.add('app', '1.4.1')[0], 0)
        self.assertNotEqual(
            self.run_cli('add', '--product', 'app', '--version', 'v1.4.1',
                         '--date', '01/11/2026', '--notes-file',
                         str(self.notes))[0], 0)
        self.assertNotEqual(
            self.add('server', 'v1.5.100', '--covers', 'v1.5.10-v1.5.100')[0], 0)
        self.assertNotEqual(
            self.add('app', 'v1.4.1', '--covers', 'v1.4.0..v1.4.1')[0], 0)
        self.assertNotEqual(
            self.run_cli('add', '--product', 'app', '--version', 'v1.4.1',
                         '--date', '2026-11-01', '--notes-file',
                         str(self.root / 'missing.md'))[0], 0)

    def test_check_runs_mkdocs_strict_and_returns_its_code(self) -> None:
        seen: dict = {}

        def fake_run(cmd, **kwargs):
            seen['cmd'] = cmd
            seen['cwd'] = kwargs.get('cwd')
            return mock.Mock(returncode=3)

        with mock.patch.dict(os.environ, {'MKDOCS': '/x/mkdocs'}), \
                mock.patch.object(rn.subprocess, 'run', fake_run):
            code, _ = self.run_cli('check')
        self.assertEqual(code, 3)
        self.assertEqual(seen['cmd'][:4], ['/x/mkdocs', 'build', '--strict', '-q'])
        self.assertEqual(seen['cmd'][4], '-d')
        self.assertEqual(seen['cwd'], str(self.root))


if __name__ == '__main__':
    unittest.main()
