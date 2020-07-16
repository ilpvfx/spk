from typing import Any
import argparse
import os
import subprocess

import structlog

import spfs
import spk

from spk.io import format_decision

_LOGGER = structlog.get_logger("cli")


def register(
    sub_parsers: argparse._SubParsersAction, **parser_args: Any
) -> argparse.ArgumentParser:

    build_cmd = sub_parsers.add_parser("build", help=_build.__doc__, **parser_args)
    build_cmd.add_argument(
        "files", metavar="SPEC_FILE", nargs="+", help="The package(s) to build"
    )
    build_cmd.set_defaults(func=_build)
    return build_cmd


def _build(args: argparse.Namespace) -> None:
    """Runs make-source and then make-binary."""

    common_args = []
    if args.verbose:
        common_args += ["-" + "v" * args.verbose]

    for filename in args.files:
        spec = spk.read_spec_file(filename)

        cmd = ["spk", "make-source", filename, *common_args]
        _LOGGER.info(" ".join(cmd))
        proc = subprocess.Popen(cmd)
        proc.wait()
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)
        cmd = ["spk", "make-binary", filename, *common_args]
        _LOGGER.info(" ".join(cmd))
        proc = subprocess.Popen(cmd)
        proc.wait()
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)
