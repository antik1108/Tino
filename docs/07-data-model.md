# 7. Data Model

## 7.1 Storage location

Resolved by `storage/paths.py` using a standard per-user data directory (XDG-style on Linux, `~/Library/Application Support` on macOS), via `pathlib`. Not hardcoded to the current working directory, so `tino` works correctly regardless of where it's launched from.

## 7.2 High score file

```json
{
  "high_score": 0,
  "updated_at": "2026-09-15T12:00:00Z"
}
```

- Read/written exclusively through `storage/highscore.py`'s `HighScoreStore` interface (see [Architecture §3.7](./03-architecture.md)) — nothing else touches this file directly.
- A missing file is treated as `high_score: 0`. A corrupt/unreadable file is treated the same way rather than crashing the app (NFR-2).

## 7.3 Config file (optional)

```json
{
  "keybindings": {
    "jump": "space",
    "quit": "q",
    "restart": "r"
  }
}
```

- Entirely optional — if absent, `config.py` uses in-code defaults. This keeps FR (zero required setup) true while still allowing customization.
- Only recognized keys are read; unknown keys are ignored rather than causing an error, so the file can be extended later without breaking older installs.

## 7.4 Forward-compatibility note

Both files are plain flat JSON on purpose — no versioning field is added in v1 because there's nothing yet to version against. If the schema needs to change later (e.g. once cloud sync is added), a `schema_version` field can be introduced at that point without breaking existing local files (missing version treated as `1`).
