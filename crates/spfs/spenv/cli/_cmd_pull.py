import argparse

from colorama import Fore

import spenv


def register(sub_parsers: argparse._SubParsersAction) -> None:

    config = spenv.get_config()

    pull_cmd = sub_parsers.add_parser("pull", help=_pull.__doc__)
    pull_cmd.add_argument(
        "refs", metavar="REF", nargs="+", help="the references to pull"
    )
    pull_cmd.set_defaults(func=_pull)


def _pull(args: argparse.Namespace) -> None:
    """Pull one or more objects to the local reposotory."""

    for ref in args.refs:
        spenv.pull_ref(ref)
