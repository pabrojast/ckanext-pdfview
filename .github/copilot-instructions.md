# Copilot Instructions for ckanext-pdfview

## Overview

This is a CKAN extension that provides a resource view plugin for rendering PDF files in the browser. It embeds Mozilla's [pdf.js](https://github.com/mozilla/pdf.js) viewer in an iframe. The extension supports CKAN >= 2.7 on Python 2.7 and 3.6+.

## Architecture

The extension is a single CKAN plugin (`PDFView`) registered as `pdf_view` via the `ckan.plugins` entry point in `setup.py`. It implements two CKAN interfaces:

- **`IConfigurer`** – registers custom templates and the `public/` directory (which serves the bundled pdf.js viewer)
- **`IResourceView`** – defines when the view is available (`can_view` checks for `format == "pdf"`), provides the Jinja2 templates, and declares a schema with an optional `pdf_url` field

Templates live in `ckanext/pdfview/theme/templates/`. The view template (`pdf_view.html`) renders an iframe pointing to the bundled pdf.js viewer at `/pdfjs/web/viewer.html`, passing either the custom `pdf_url` or the resource's own URL. The form template (`pdf_form.html`) lets users optionally override the PDF URL.

The `ckanext/pdfview/public/pdfjs/` directory contains a vendored copy of pdf.js. Do not modify these files directly; update them by replacing with a new pdf.js release.

## Build & Test Commands

### Lint

```
flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics --exclude ckan
```

### Tests (requires a running CKAN environment with Postgres, Solr, and Redis)

Run the full test suite:

```
pytest --ckan-ini=test.ini --cov=ckanext.pdfview --disable-warnings ckanext/pdfview/tests
```

Run a single test:

```
pytest --ckan-ini=test.ini ckanext/pdfview/tests/test_view.py::test_view_shown_on_resource_page_with_pdf_url
```

## Conventions

- Tests use `pytest` with the `pytest-ckan` plugin. Test configuration is applied via `@pytest.mark.ckan_config` and `@pytest.mark.usefixtures` decorators, not by subclassing test base classes.
- The CKAN test config file is `test.ini` at the repo root. It references the CKAN core test config and loads `pdf_view` as the only plugin.
- Use `ckan.plugins.toolkit` (imported as `p.toolkit`) for CKAN API access (validators, URL helpers, i18n). Do not import CKAN internals directly.
