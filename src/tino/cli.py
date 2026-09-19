"""CLI argument parser and entry point dispatch for TINO."""

import argparse
import sys

from tino import __version__
from tino.app import run_app
from tino.storage.highscore import JSONHighScoreStore


def cmd_score() -> int:
    """Print the current stored high score to stdout."""
    store = JSONHighScoreStore()
    score = store.load()
    print(f"Current High Score: {score}")
    return 0


def cmd_reset_score(force: bool = False) -> int:
    """Reset the stored high score back to 0."""
    store = JSONHighScoreStore()
    current = store.load()

    if not force:
        try:
            confirm = input(
                f"Are you sure you want to reset your high score of {current}? [y/N]: "
            )
            if confirm.strip().lower() not in ("y", "yes"):
                print("Reset cancelled.")
                return 0
        except (KeyboardInterrupt, EOFError):
            print("\nReset cancelled.")
            return 1

    store.reset()
    print("High score has been reset to 0.")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="tino",
        description="TINO — Terminal Dino Endless Runner",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"tino {__version__}",
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # `tino score`
    subparsers.add_parser(
        "score",
        help="Print the current stored high score and exit",
    )

    # `tino reset-score`
    reset_parser = subparsers.add_parser(
        "reset-score",
        help="Clear the stored high score",
    )
    reset_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Skip confirmation prompt",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "score":
        return cmd_score()
    elif args.subcommand == "reset-score":
        return cmd_reset_score(force=args.force)
    else:
        # Default behavior: launch the game
        try:
            return run_app()
        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    sys.exit(main())
