# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and GitHub Copilot CLI when working in this repository.

This repository builds public Hugging Face datasets of the twenty-four Supreme Court document collections on www.supremecourt.gov, one dataset per column of the site's footer (such as `incrediblecrab/us-scotus-opinions` and `us-scotus-oral-arguments`) and one config per collection, plus `us-scotus-cases`, which joins them by docket. The repository is public. `README.md`, `scotus_products/README.md` and `tests/README.md` describe each part.

## Commands

```bash
.venv/bin/python -m pytest -q                         # offline suite, what test.yml runs on push
.venv/bin/python -m pytest -q tests/test_extract.py -k <name>
.venv/bin/python -m scotus_products {list,run,verify,card,summarize} --dataset <collection|all> --help
.venv/bin/python -m scotus_products.cases {run,verify,card} --help
```

`.venv` links to the shared `~/.venvs/main`; extraction also needs poppler's `pdftotext`, `pdfinfo` and `pdfimages`. Use `--local DIR` for any local build; without it `run` writes to the published datasets, so do not run it that way unless the owner asks. `.github/workflows/pipeline.yml` runs the scheduled sync and publishes through Hugging Face Trusted Publishing. GitHub disables schedules after 60 days without a commit; its `inactivity` job fails at 50 days to warn first and deliberately makes no keepalive commit, which GitHub treats as a Terms violation, so do not add one.

## Rules the data depends on

The datasets are a verbatim record: each row is one listed file, its bytes as served and its text as the extractor printed it. Nothing is corrected, normalized or generated, and there is no OCR or language model anywhere in the pipeline; keep it that way. Requests go at least 1.1 seconds apart because robots.txt sets `Crawl-delay: 1`, use a user agent naming this repository, never follow redirects and never touch a disallowed path; all of that lives in `scotus_products/http.py`, so route every request through it.

## Structure

`scotus_products/sources.py` defines each collection: its pages, parser, partitions, typed fields and which footer column (category, hence dataset) holds it. `markup.py` renders page text and resolves links to file ids; `extract.py` runs `pdftotext -raw`, detects scanned pages, cross-checks with pypdf and confirms MP3 and MP4 files are audio and video without extracting text. `pipeline.py` is the sync loop with retries, delisting, the single-writer lease and a free-disk floor; `store.py` holds the schema and the local and Hub stores, each collection under its own directory of its category's repo. `card.py` renders each collection's card and the category README (one config per collection), and `verify.py` checks partitions, including that every file has the schema's columns the dataset viewer needs. `cases.py` builds `us-scotus-cases` from the document datasets' rows. `tests/test_workflows.py` checks the workflow files themselves.
