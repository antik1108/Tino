# 6. CLI

Built with `argparse`. `tino` with no arguments launches the game directly (FR-1) — subcommands are for everything else.

| Command | Effect |
|---------|--------|
| `tino` | Launch the game (default behavior, no subcommand needed). |
| `tino score` | Print the current stored high score and exit — no terminal takeover. |
| `tino reset-score` | Clear the stored high score (with a confirmation prompt). |
| `tino --version` | Print the installed version. |
| `tino --help` | Standard argparse help output. |

## Design notes

- Launching straight into the game with zero arguments (rather than requiring `tino play`) matches how the project is meant to be used — a quick terminal diversion, not a tool with a formal command structure.
- `score` and `reset-score` are deliberately simple, non-interactive-terminal commands (plain stdout), so they work in scripts/pipelines too.
- All CLI parsing lives in `cli.py` and only decides *what to run* — it never contains game logic itself (see [Architecture §3.3](./03-architecture.md)).
