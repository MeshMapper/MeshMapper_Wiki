#!/usr/bin/env python3
"""Write MeshMapper release-notes pages and keep the wiki menu in step.

Stdlib only, runs on the system python3 (3.9). See RELEASE_NOTES.md at the
wiki root for the rules this enforces.

    tools/release_notes.py add --product app|server --version vX.Y.Z \\
        --date YYYY-MM-DD --notes-file FILE [--covers vA..vB] [--replace]
    tools/release_notes.py check

`add` writes docs/release-notes/<product>/<version>.md and inserts one line
into the Release Notes block of mkdocs.yml. The menu is edited as text, never
parsed and re-dumped: mkdocs.yml holds YAML the stdlib cannot read safely and
is edited by hand elsewhere.

`check` runs `mkdocs build --strict` into a throwaway directory.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PRODUCTS = {'app': 'App', 'server': 'Server'}

DEFAULT_MKDOCS = '~/.venvs/mkdocs/bin/mkdocs'

MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December')

SECTIONS = ('## ✨ New', '## 🐛 Fixes')

# The wiki runs mkdocs-macros, which executes these in page text.
MACRO_TOKENS = ('{{', '{%', '{#')

NAV_BLOCK = '  - Release Notes:'
NAV_CHILD_INDENT = 4
NAV_ENTRY_INDENT = 6

_VERSION_RE = re.compile(r'v([0-9]+)\.([0-9]+)\.([0-9]+)')
_COVERS_RE = re.compile(r'(v[0-9]+\.[0-9]+\.[0-9]+)\.\.(v[0-9]+\.[0-9]+\.[0-9]+)')
_ISO_DATE_RE = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
_ENTRY_RE = re.compile(r'^ {%d}- (v[0-9]+\.[0-9]+\.[0-9]+):' % NAV_ENTRY_INDENT)


class DuplicateVersion(ValueError):
    """The menu already lists this version for this product."""


def version_key(v: str) -> tuple[int, int, int]:
    """Numeric sort key for `vX.Y.Z`; anything else raises ValueError."""
    m = _VERSION_RE.fullmatch(v) if isinstance(v, str) else None
    if m is None:
        raise ValueError('version must look like v1.2.3, got %r' % (v,))
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _product_name(product: str) -> str:
    try:
        return PRODUCTS[product]
    except KeyError:
        raise ValueError('product must be one of %s, got %r'
                         % (', '.join(PRODUCTS), product)) from None


def _long_date(d: date) -> str:
    return '%s %d, %d' % (MONTHS[d.month - 1], d.day, d.year)


def page_text(product: str, version: str, released: date, body: str,
              covers: tuple[str, str] | None) -> str:
    """The full page: title, release line, then the notes body."""
    name = _product_name(product)
    version_key(version)
    line = 'Released ' + _long_date(released)
    if covers is not None:
        first, last = covers
        if version_key(first) > version_key(last):
            raise ValueError('covers range runs backwards: %s to %s'
                             % (first, last))
        line += '. Covers %s to %s.' % (first, last)
    body = body.replace('\r\n', '\n').strip()
    return '# MeshMapper %s %s\n\n*%s*\n\n%s\n' % (name, version, line, body)


def check_body(body: str) -> None:
    """Raise ValueError if the notes body is not safe or not in house shape."""
    for token in MACRO_TOKENS:
        if token in body:
            raise ValueError(
                'notes contain %r; the wiki runs mkdocs-macros and would '
                'execute it. Reword it.' % token)
    lines = body.splitlines()
    for n, line in enumerate(lines, 1):
        if line.startswith('# '):
            raise ValueError(
                'line %d starts a title ("# "); the page title is added for '
                'you, use "## " sections' % n)
    if '—' in body:
        raise ValueError('notes contain an em dash; use a comma, colon or '
                         'a new sentence')
    present = {line.rstrip() for line in lines}
    if not any(s in present for s in SECTIONS):
        raise ValueError('notes need a "%s" or "%s" section'
                         % SECTIONS)


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(' '))


def _release_block(lines: list[str]) -> tuple[int, int]:
    """(index of the Release Notes line, index of the block's last line)."""
    start = next((i for i, l in enumerate(lines) if l.rstrip() == NAV_BLOCK),
                 None)
    if start is None:
        raise ValueError('mkdocs.yml has no "%s" block' % NAV_BLOCK.strip())
    last = start
    for i in range(start + 1, len(lines)):
        if not lines[i].strip():
            continue
        if _indent(lines[i]) <= 2:
            break
        last = i
    return start, last


def _section(lines: list[str], start: int, last: int,
             header: str) -> tuple[int, int] | None:
    """[first, end) of a child's header line plus its entries, or None."""
    for i in range(start + 1, last + 1):
        if lines[i].rstrip() != header:
            continue
        j = i + 1
        while j <= last and (not lines[j].strip()
                             or _indent(lines[j]) > NAV_CHILD_INDENT):
            j += 1
        while j > i + 1 and not lines[j - 1].strip():
            j -= 1
        return i, j
    return None


def insert_nav(mkdocs_yml: str, product: str, version: str) -> str:
    """Add `version` to Release Notes > <Product> in the menu, as text only.

    The product subsection is created when missing (App before Server, both
    after Overview). Entries stay in descending numeric version order.
    Raises DuplicateVersion if the product already lists the version.
    """
    name = _product_name(product)
    key = version_key(version)
    lines = mkdocs_yml.split('\n')
    header = ' ' * NAV_CHILD_INDENT + '- %s:' % name

    start, last = _release_block(lines)
    found = _section(lines, start, last, header)
    if found is None:
        at = last + 1
        if product == 'app':
            server = _section(lines, start, last,
                              ' ' * NAV_CHILD_INDENT + '- Server:')
            if server is not None:
                at = server[0]
        lines.insert(at, header)
        start, last = _release_block(lines)
        found = _section(lines, start, last, header)
    assert found is not None
    first, end = found

    insert_at = end
    for i in range(first + 1, end):
        m = _ENTRY_RE.match(lines[i])
        if m is None:
            continue
        existing = version_key(m.group(1))
        if existing == key:
            raise DuplicateVersion('%s is already in the %s menu'
                                   % (version, name))
        if existing < key and insert_at == end:
            insert_at = i
    lines.insert(insert_at, ' ' * NAV_ENTRY_INDENT + '- %s: release-notes/%s/%s.md'
                 % (version, product, version))
    return '\n'.join(lines)


def _fail(message: str) -> int:
    print('error: %s' % message, file=sys.stderr)
    return 1


def _cmd_add(args: argparse.Namespace) -> int:
    try:
        version_key(args.version)
        if not _ISO_DATE_RE.fullmatch(args.date):
            raise ValueError('date must look like 2026-11-01, got %r'
                             % args.date)
        released = date.fromisoformat(args.date)
        covers = None
        if args.covers is not None:
            if args.product != 'server':
                raise ValueError('--covers only applies to --product server')
            m = _COVERS_RE.fullmatch(args.covers)
            if m is None:
                raise ValueError('--covers must look like v1.5.10..v1.5.100, '
                                 'got %r' % args.covers)
            covers = (m.group(1), m.group(2))

        page = ROOT / 'docs' / 'release-notes' / args.product / (args.version + '.md')
        rel = page.relative_to(ROOT)
        if page.exists() and not args.replace:
            raise ValueError('page exists: %s (use --replace to overwrite)'
                             % rel)

        body = Path(args.notes_file).read_bytes().decode('utf-8')
        check_body(body)
        text = page_text(args.product, args.version, released, body, covers)

        yml_path = ROOT / 'mkdocs.yml'
        yml = yml_path.read_bytes().decode('utf-8')
        try:
            new_yml = insert_nav(yml, args.product, args.version)
        except DuplicateVersion:
            if not args.replace:
                raise
            new_yml = yml
    except (ValueError, OSError) as exc:
        return _fail(str(exc))

    try:
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_bytes(text.encode('utf-8'))
        if new_yml != yml:
            yml_path.write_bytes(new_yml.encode('utf-8'))
    except OSError as exc:
        return _fail(str(exc))
    print('wrote %s' % rel)
    print('menu: %s' % ('updated mkdocs.yml' if new_yml != yml
                        else 'already listed, mkdocs.yml unchanged'))
    return 0


def _cmd_check(_args: argparse.Namespace) -> int:
    mkdocs = os.path.expanduser(os.environ.get('MKDOCS') or DEFAULT_MKDOCS)
    env = dict(os.environ)
    env.setdefault('NO_MKDOCS_2_WARNING', '1')
    with tempfile.TemporaryDirectory() as out:
        try:
            proc = subprocess.run(
                [mkdocs, 'build', '--strict', '-q', '-d', out],
                cwd=str(ROOT), env=env)
        except OSError as exc:
            print('error: cannot run %s: %s' % (mkdocs, exc), file=sys.stderr)
            return 127
    return proc.returncode


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='release_notes.py',
        description='Write MeshMapper release-notes pages and menu lines.')
    sub = parser.add_subparsers(dest='command', required=True)

    add = sub.add_parser('add', help='write a page and add it to the menu')
    add.add_argument('--product', required=True, choices=sorted(PRODUCTS))
    add.add_argument('--version', required=True, help='vX.Y.Z')
    add.add_argument('--date', required=True, help='release date, YYYY-MM-DD')
    add.add_argument('--notes-file', required=True,
                     help='markdown body with ## ✨ New / ## 🐛 Fixes')
    add.add_argument('--covers', help='server roll-up range, vA..vB')
    add.add_argument('--replace', action='store_true',
                     help='overwrite an existing page')
    add.set_defaults(func=_cmd_add)

    check = sub.add_parser('check', help='run mkdocs build --strict')
    check.set_defaults(func=_cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
