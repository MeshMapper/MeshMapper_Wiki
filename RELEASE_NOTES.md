# Release notes rules

This file is for the people and tools that write release-notes pages. It sits
at the repo root, outside `docs/`, so it is not published.

App releases and Server roll-ups share one structure. Pages are written by
`tools/release_notes.py`, never by hand.

## Structure

| | App | Server |
|---|---|---|
| Page | `docs/release-notes/app/vX.Y.Z.md` | `docs/release-notes/server/vX.Y.Z.md` |
| Title | `# MeshMapper App vX.Y.Z` | `# MeshMapper Server vX.Y.Z` |
| Line under the title | `*Released Month D, YYYY*` | `*Released Month D, YYYY. Covers vA to vB.*` |
| Menu | Release Notes > App > `vX.Y.Z` | Release Notes > Server > `vX.Y.Z` |

- Body sections are `## ✨ New` and `## 🐛 Fixes`. Leave one out if it would
  be empty, but keep at least one.
- The menu is Release Notes > Overview / App / Server. Each product lists its
  versions newest first, in numeric order (`v1.4.10` sits above `v1.4.9`).
- A Server page is named after the newest tag in its roll-up. The date is that
  tag's release date, and `Covers vA to vB.` names the first and last tag the
  page rolls up.
- Nothing is backfilled. The App list starts at v1.4.1, and the Server list
  starts at the first roll-up after the old pages were cleared.
- The Overview page (`docs/release-notes/index.md`) is hand-written and is not
  touched by the helper.

## Voice

- Write for users: say what they will notice, not what changed in the code.
- Drop anything with no user-visible effect. Internal and admin-only changes
  and deployment steps never go on the wiki.
- Bullets look like `- **Short name:** one or two plain sentences.`
- When a limit comes from radio firmware, name the firmware version that
  fixes it. When a feature is controlled by the server, spell out the rules
  (how often, who can turn it on).
- No em dashes (use a comma, a colon or a new sentence), no sign-off, no role
  mention, no store-timing reminder. Those belong to the Discord post only.
- No tester-level detail such as build numbers or minor fixes nobody would
  notice.

## What the helper refuses

The wiki runs the mkdocs-macros plugin, which executes template syntax in page
text. The helper refuses a notes file that:

- contains `{{`, `{%` or `{#`
- has a line starting with `# ` (the title is added for you)
- contains an em dash
- has neither `## ✨ New` nor `## 🐛 Fixes`

It also refuses a version that is not `vX.Y.Z`, a date that is not
`YYYY-MM-DD`, a page that already exists (unless `--replace`) and a version
the menu already lists.

## Usage

Run it from the repo root with the system `python3` (3.9 is fine, stdlib only).

```bash
# App release
tools/release_notes.py add --product app --version v1.4.1 \
    --date 2026-11-01 --notes-file /tmp/notes.md

# Server roll-up
tools/release_notes.py add --product server --version v1.5.100 \
    --date 2026-11-01 --covers v1.5.10..v1.5.100 --notes-file /tmp/notes.md

# Build the whole site in strict mode into a throwaway folder
tools/release_notes.py check
```

- `add` writes the page and inserts one line into the `Release Notes` block of
  `mkdocs.yml`. The menu is edited as text, never parsed and re-dumped.
- `--covers` is for Server pages only.
- To fix a published page, run `add` again with `--replace`. It rewrites the
  page and leaves the existing menu line alone.
- `check` runs `${MKDOCS:-~/.venvs/mkdocs/bin/mkdocs} build --strict -q` and
  returns its exit code. Run it before every push.

The notes file is only the body, starting at the first `## ` section:

```markdown
## ✨ New
- **Feature name:** what a user can now do, in a sentence or two.

## 🐛 Fixes
- **Problem name:** what was wrong and that it now works.
```

## Committing

- Stage the page and `mkdocs.yml` by name. Never `git add docs/`.
- Subject: `docs(release-notes): MeshMapper App vX.Y.Z` (or `Server`).
- Commit straight to `main`. Pushing `main` publishes the site.

## Tests

```bash
python3 -m unittest discover -s tools/tests -t .
```
