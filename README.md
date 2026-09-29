# MeshMapper Wiki

Source for [wiki.meshmapper.net](https://wiki.meshmapper.net), the documentation for MeshMapper, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Editing

Pages live in `docs/` and the sidebar is defined by `nav` in `mkdocs.yml`. Link between pages with relative links (e.g. `[Backbone](backbone.md)`) so broken links are caught by the build.

## Building Locally

```bash
pip install mkdocs-material mkdocs-macros-plugin pyyaml mkdocs-glightbox pymdown-extensions
mkdocs serve          # preview at http://127.0.0.1:8000
mkdocs build --strict # same check the deploy runs
```

Pushing to `main` builds and deploys the site to GitHub Pages.
