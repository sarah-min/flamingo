## Purpose

This repository is a small Python utility that stores search phrases in a MongoDB Atlas database. These instructions give an AI coding agent the minimal, concrete context needed to work productively here.

## Big picture

- Single Python script: `searchSave.py` is the primary entry point. It loads environment variables, connects to MongoDB Atlas, inserts documents into the `flamingo` database and the `searches` collection.
- Data flow: `.env` -> load with `python-dotenv` -> connection string built as
  `mongodb+srv://{MY_USERNAME}:{MY_PASSWORD}@cluster0.ze8mjac.mongodb.net/` -> write to DB.

## Key files

- `searchSave.py` — shows how credentials are loaded, how `pymongo` is used, and the insert/find pattern. Example behaviors to reference:
  - uses `BASE_DIR = Path(__file__).resolve().parent` and `load_dotenv(BASE_DIR / ".env")`
  - expects env vars: `MY_KEY` (printed), `MY_USERNAME`, `MY_PASSWORD`
  - connects with `pymongo.MongoClient(f"mongodb+srv://{USER}:{PWD}@cluster0.ze8mjac.mongodb.net/")`
  - database: `flamingo`, collection: `searches`; uses `insert_many` and reads `inserted_ids[0]`.
- `README.md` — currently minimal; check before making doc-heavy changes.

## Environment & setup

Assumptions discovered from the code:
- Python 3.x (no explicit constraint in repo).
- Required packages: `pymongo`, `python-dotenv`.

Common setup steps (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pymongo python-dotenv
python .\searchSave.py
```

Create a project `.env` in the repo root (do not commit). Minimal example:

```
MY_KEY=your-key-if-used
MY_USERNAME=yourAtlasUser
MY_PASSWORD=yourAtlasPassword
```

## Project-specific patterns & gotchas

- Credentials are read from a `.env` file located at the repository root because `BASE_DIR` is `Path(__file__).resolve().parent`.
- The connection string uses the Atlas SRV host `cluster0.ze8mjac.mongodb.net` — don't change the host unless you know the target cluster.
- `searchSave.py` uses `insert_many` and then immediately queries the first `inserted_ids[0]` to verify insertion; follow that pattern when editing related code.
- There are no tests, packaging, or CI files — changes should be validated locally against a developer's Atlas test cluster.

## Debugging checklist (concrete steps)

1. If the script fails to connect, confirm `.env` values and that the machine/IP is allowed in Atlas (IP access list).
2. Print environment variables near the top of `searchSave.py` to confirm values are loaded. The script already prints `MY_KEY`.
3. For Mongo issues, try a minimal Python REPL using `pymongo` with the same connection string.
4. If insert doesn't work, check `InsertManyResult.inserted_ids` and confirm indexing.

## What I did / merge notes

- No existing `.github/copilot-instructions.md` or AGENT files were found. This file is a concise, discoverable summary of patterns present in `searchSave.py` and the repo.

If anything important is missing (additional scripts, test commands, CI workflows, or a specific Python version), point me at those files or paste the missing content and I'll update these instructions.
