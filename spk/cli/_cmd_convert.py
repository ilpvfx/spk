from platform import python_version
import sys
from sys import flags
from typing import Callable, Any
import os
import re
import argparse
from ruamel.yaml import parser
import spfs

import structlog
from colorama import Fore, Style

import spk
import spk.external

from . import _flags

_LOGGER = structlog.get_logger("spk.cli")


def register(
    sub_parsers: argparse._SubParsersAction, **parser_args: Any
) -> argparse.ArgumentParser:

    convert_cmd = sub_parsers.add_parser(
        "convert", help=_convert.__doc__, **parser_args,
    )

    sub_parsers = convert_cmd.add_subparsers(dest="converter", required=True)
    spcomp2_cmd = sub_parsers.add_parser(
        "spcomp2", help="Convert and convert spComp2s as packages", **parser_args
    )
    spcomp2_cmd.add_argument(
        "--target-repo",
        "-r",
        type=str,
        metavar="NAME",
        default="origin",
        help="The repository to publish to. Any configured spfs repository can be named here.",
    )
    spcomp2_cmd.add_argument(
        "--publish",
        default=None,
        action="store_true",
        help="Also publish the packages after convert",
    )
    spcomp2_cmd.add_argument(
        "--no-publish",
        dest="publish",
        action="store_false",
        help="Also publish the packages after convert",
    )
    spcomp2_cmd.add_argument(
        "--force",
        "-f",
        action="store_true",
        default=False,
        help="Forcefully overwrite any existing publishes",
    )
    spcomp2_cmd.add_argument(
        "--no-deps",
        dest="deps",
        action="store_false",
        default=True,
        help="Do not follow and convert dependencies of the requested spComp2s",
    )
    spcomp2_cmd.add_argument(
        "--no-runtime",
        "-nr",
        action="store_true",
        help="Do not build in a new spfs runtime (useful for speed and debugging)",
    )
    _flags.add_option_flags(spcomp2_cmd)
    spcomp2_cmd.add_argument(
        "packages",
        nargs="+",
        metavar="NAME[/VERSION]",
        help="The spcomp2 packages to import (eg: VnP3,  FileSequence/v7)",
    )

    pip_cmd = sub_parsers.add_parser(
        "pip", help="Convert and import packages using pip", **parser_args
    )
    pip_cmd.add_argument(
        "--python-version", default="3.7", help="The version of python to install for",
    )
    pip_cmd.add_argument(
        "--target-repo",
        "-r",
        type=str,
        metavar="NAME",
        default="origin",
        help="The repository to publish to. Any configured spfs repository can be named here.",
    )
    pip_cmd.add_argument(
        "--publish",
        default=None,
        action="store_true",
        help="Also publish the packages after convert",
    )
    pip_cmd.add_argument(
        "--force",
        "-f",
        action="store_true",
        default=False,
        help="Forcefully overwrite any existing publishes",
    )
    pip_cmd.add_argument(
        "--no-deps",
        dest="deps",
        action="store_false",
        default=True,
        help="Do not follow and convert dependencies of the requested spComp2s",
    )
    pip_cmd.add_argument(
        "--no-runtime",
        "-nr",
        action="store_true",
        help="Do not build in a new spfs runtime (useful for speed and debugging)",
    )
    pip_cmd.add_argument(
        "packages",
        nargs="+",
        metavar="NAME[VERSION]",
        help="The pip packages to import (eg: pytest,  PySide2>=5)",
    )

    convert_cmd.set_defaults(func=_convert)
    return convert_cmd


def _convert(args: argparse.Namespace) -> None:
    """Convert a package from an external packaging system for use in spk."""

    if args.converter == "spcomp2":
        _convert_spcomp2s(args)

    elif args.converter == "pip":
        _convert_pip_packages(args)

    else:
        raise NotImplementedError(
            f"Internal Error: no logic for converter: {args.converter}"
        )


def _convert_spcomp2s(args: argparse.Namespace) -> None:

    if not args.no_runtime:
        runtime = spfs.get_config().get_runtime_storage().create_runtime()
        runtime.set_editable(True)
        cmd = spfs.build_command_for_runtime(runtime, *sys.argv, "--no-runtime")
        os.execv(cmd[0], cmd)

    options = _flags.get_options_from_flags(args)

    specs = []
    for name in args.packages:
        if "/" not in name:
            name += "/" + "current"
        name, version = name.split("/")
        specs.extend(
            spk.external.import_spcomp2(
                name, version, options=options, recursive=args.deps
            )
        )

    print("\nThe following packages were converted:\n")
    for spec in specs:
        print(f"  {spk.io.format_ident(spec.pkg)} ", end="")
        print(spk.io.format_options(spec.build.resolve_all_options({})))
    print("")

    print(args.publish)
    if args.publish is None:
        print("These packages are now available in the local repository")
        args.publish = bool(
            input("Do you want to also publish these packages? [y/N]: ").lower()
            in ("y", "yes")
        )

    if args.publish:
        publisher = spk.Publisher().with_target(args.target_repo).force(args.force)
        for spec in specs:
            publisher.publish(spec.pkg)


def _convert_pip_packages(args: argparse.Namespace) -> None:

    if not args.no_runtime:
        runtime = spfs.get_config().get_runtime_storage().create_runtime()
        runtime.set_editable(True)
        cmd = spfs.build_command_for_runtime(runtime, *sys.argv, "--no-runtime")
        os.execv(cmd[0], cmd)

    specs = []
    for name in args.packages:
        version = ""
        match = re.match(r"^(.*)([<>=~]+.*)?$", name)
        if match:
            name, version = match.group(1), match.group(2) or ""

        specs.extend(
            spk.external.import_pip(
                name, version, python_version=args.python_version, recursive=args.deps,
            )
        )

    print("\nThe following packages were converted:\n")
    for spec in specs:
        print(f"  {spk.io.format_ident(spec.pkg)} ", end="")
        print(spk.io.format_options(spec.build.resolve_all_options({})))
    print("")

    if args.publish is None:
        print("These packages are now available in the local repository")
        args.publish = bool(
            input("Do you want to also publish these packages? [y/N]: ").lower()
            in ("y", "yes")
        )

    if args.publish:
        publisher = spk.Publisher().with_target(args.target_repo).force(args.force)
        for spec in specs:
            publisher.publish(spec.pkg)
