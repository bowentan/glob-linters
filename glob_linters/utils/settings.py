"""Configuration"""
# Configuration vairables and defaults
# pylint: disable=subprocess-run-check
import argparse
import configparser
import os
import re
import subprocess
import sys
from asyncio.log import logger
from dataclasses import dataclass
from typing import Callable, ClassVar

from glob_linters import linters


@dataclass
class Configs:
    # Exit code record
    return_code: ClassVar[int] = 0

    # Indicator of reading file
    has_read_config_file: ClassVar[bool] = False

    # Lint targets settings
    target_dir: ClassVar[str] = "."
    target_suffix: ClassVar[list[str]] = [".c", ".cpp", ".py"]

    # Running mode
    debug: ClassVar[bool] = False

    # Linter dict for running
    # Clang Linters
    cpplint: ClassVar[linters.Cpplint] = linters.Cpplint("cpplint")
    clang_format: ClassVar[linters.ClangFormat] = linters.ClangFormat("clang-format")
    # Python
    pylint: ClassVar[linters.Pylint] = linters.Pylint("pylint")
    flake8: ClassVar[linters.Flake8] = linters.Flake8("flake8")
    black: ClassVar[linters.Black] = linters.Black("black")
    isort: ClassVar[linters.Isort] = linters.Isort("isort")
    mypy: ClassVar[linters.Mypy] = linters.Mypy("mypy")

    # Linters needed for each file extension
    linters_needed: ClassVar[dict[str, list[str]]] = {
        ".cpp": ["cpplint", "clang-format"],
        ".py": ["pylint", "flake8", "black", "isort", "mypy"],
    }

    # Available configs
    set_configs: ClassVar[dict[str, dict[str, Callable]]] = {
        "target": {
            "target_dir": lambda x: setattr(Configs, "target_dir", x),
            "target_suffix": lambda x: setattr(
                Configs, "target_suffix", re.split(" ", x)
            ),
        },
        "executable": {
            # Clang
            "cpplint": lambda x: setattr(Configs.cpplint, "executable", x),
            "cpplint.options": lambda x: setattr(
                Configs.cpplint, "options", Configs.cpplint.options + x.split()
            ),
            "clang-format": lambda x: setattr(Configs.clang_format, "executable", x),
            "clang-format.options": lambda x: setattr(
                Configs.clang_format,
                "options",
                Configs.clang_format.options + x.split(),
            ),
            # Python
            "pylint": lambda x: setattr(Configs.pylint, "executable", x),
            "pylint.options": lambda x: setattr(
                Configs.pylint, "options", Configs.pylint.options + x.split()
            ),
            "flake8": lambda x: setattr(Configs.flake8, "executable", x),
            "flake8.options": lambda x: setattr(
                Configs.flake8, "options", Configs.flake8.options + x.split()
            ),
            "black": lambda x: setattr(Configs.black, "executable", x),
            "black.options": lambda x: setattr(
                Configs.black, "options", Configs.black.options + x.split()
            ),
            "isort": lambda x: setattr(Configs.isort, "executable", x),
            "isort.options": lambda x: setattr(
                Configs.isort, "options", Configs.isort.options + x.split()
            ),
            "mypy": lambda x: setattr(Configs.mypy, "executable", x),
            "mypy.options": lambda x: setattr(
                Configs.mypy, "options", Configs.mypy.options + x.split()
            ),
        },
        "env": {
            "debug": lambda x: setattr(Configs, "debug", x),
        },
    }

    # Default config file
    DEFAULT_CONFIG_FILE_PATH: ClassVar[str] = ".github/glob-linters.ini"
    MYPY_PACKAGE_REQUIREMENTS_FILE_PATH: str = ".github/mypy_requirements.txt"


def parse_config_file(config_file: str) -> None:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    for section in config_parser:
        if section == "DEFAULT":
            continue
        if section not in Configs.set_configs:
            raise ValueError(f"No such section supported: {section}")
        for option in config_parser[section]:
            if option not in config_parser[section]:
                raise ValueError(f"No such option supported: {option}")
            Configs.set_configs[section][option](config_parser[section][option])


def parse_args(args: argparse.Namespace) -> None:
    Configs.debug = args.debug
    Configs.target_dir = args.target_dir
    Configs.target_suffix = re.split(" ", args.target_suffix)
    if args.configs is not None:
        for key, value in map(lambda x: re.split("=", x), args.configs):
            if key not in Configs.set_configs["executable"]:
                raise ValueError(f"No such linter supported: {key}")
            if "options" in key:
                Configs.set_configs["executable"][key](value)
            else:
                Configs.set_configs["executable"][key](value)


def install_mypy_package_requirements() -> None:
    if os.path.exists(Configs.MYPY_PACKAGE_REQUIREMENTS_FILE_PATH):
        logger.debug("Not found mypy_requirements.txt, skip package installation")
        return
    logger.info("Install packages for mypy checking...")
    cmd = ["pip", "install", "-r", Configs.MYPY_PACKAGE_REQUIREMENTS_FILE_PATH]
    logger.debug("Install command: %s", " ".join(cmd))
    cmd_result = subprocess.run(cmd, capture_output=True)

    logger.debug("Installation output:")
    for line in cmd_result.stdout.decode().strip().split("\n"):
        logger.debug("\t%s", line)

    if cmd_result.returncode != 0:
        logger.error("Package installaltion failed:")
        for line in cmd_result.stderr.decode().strip().split("\n"):
            logger.error("\t%s", line)
        sys.exit(1)
