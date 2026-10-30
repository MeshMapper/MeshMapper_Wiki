# MeshMapper Wiki

Source for [wiki.meshmapper.net](https://wiki.meshmapper.net), the documentation for MeshMapper, built with [Zensical](https://zensical.org/).

## Editing

Pages live in `docs/` and the sidebar is defined by `nav` in `mkdocs.yml`. Link between pages with relative links (e.g. `[Backbone](backbone.md)`) so broken links are caught by the build.

## Building Locally

```bash
pip install zensical
zensical serve                  # preview at http://127.0.0.1:8000
zensical build --clean --strict # same check the deploy runs
```

Pushing to `main` builds and deploys the site to GitHub Pages.
