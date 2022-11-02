"""Configuration"""
# Configuration vairables and defaults
# pylint: disable=subprocess-run-check
# import argparse
import argparse
import configparser
import logging
import os
import re
import subprocess
import sys
from ast import literal_eval
from dataclasses import dataclass
from functools import reduce
from typing import ClassVar

from glob_linters import linters

# Default config file
DEFAULT_CONFIG_FILE_PATH: str = ".github/glob-linters.ini"

# Supported file extension/suffix
SUPPORTED_FILE_SUFFIXES: list[str] = [".cpp", ".py"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream = logging.StreamHandler()
stream.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] : %(message)s"))
logger.addHandler(stream)


@dataclass
class Configs:
    """Class to store configs/settings"""

    # Exit code record
    return_code: ClassVar[int] = 0

    # Indicator of reading file
    has_read_config_file: ClassVar[bool] = False

    # Lint targets settings
    target_dirs: ClassVar[list[str]] = ["."]
    target_suffixes: ClassVar[list[str]] = SUPPORTED_FILE_SUFFIXES.copy()

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
    linters_enabled: ClassVar[dict[str, list[str]]] = {
        ".cpp": ["cpplint", "clang_format"],
        ".py": ["pylint", "flake8", "black", "isort", "mypy"],
    }

    # "suffix:linter_name"
    available_suffix_linters: ClassVar[list[str]] = reduce(
        lambda x, y: x + y,
        map(
            lambda items: list(map(lambda v: f"{items[0]}:{v}", items[1])),
            linters_enabled.items(),
        ),
    )

    available_configs: ClassVar[dict[str, list[str]]] = {
        "DEFAULT": [],
        "target": ["dirs", "suffixes"],
        "env": ["debug", "extra_python_package_requirements"],
    }
    available_configs.update(
        dict(
            zip(
                SUPPORTED_FILE_SUFFIXES,
                [["enabled_linters", "disabled_linters"]]
                * len(SUPPORTED_FILE_SUFFIXES),
            )
        )
    )
    available_configs.update(
        dict(
            zip(
                available_suffix_linters,
                [["executable", "options", "config_file"]]
                * len(available_suffix_linters),
            )
        )
    )


def parse_config_file(config_file: str) -> None:
    """Parse configuration from configparser-like file

    Parameters
    ----------
    config_file : str
        Configuration file path

    Raises
    ------
    ValueError
        Invalid section/option found in config file
    """

    def _target_section(section: str, option: str) -> None:
        if option == "dirs":
            Configs.target_dirs = re.split(r"[,\s]", config_parser[section][option])
        if option == "suffixes":
            diff = set(re.split(r"[,\s]", config_parser[section][option])) - set(
                SUPPORTED_FILE_SUFFIXES
            )
            if len(diff) > 0:
                raise ValueError(f"No such suffixes supported: {diff}")
            Configs.target_suffixes = re.split(r"[,\s]", config_parser[section][option])

    def _env_section(section: str, option: str) -> None:
        if option == "debug":
            Configs.debug = literal_eval(config_parser[section][option])
        if option == "extra_python_package_requirements":
            logger.info("*" * 120)
            for filename in re.split(r"[,\s]", config_parser[section][option]):
                _install_extra_python_package_requirementss(filename)
            logger.info("*" * 120)

    def _lang_section(section: str, option: str) -> None:
        values = re.split(r"[,\s]", config_parser[section][option])
        diff = set(values) - set(Configs.linters_enabled[section])
        if len(diff) > 0:
            raise ValueError(f"No such linters supported: {diff}")
        if option == "enabled_linters":
            Configs.linters_enabled[section] = values
        if option == "disabled_linters":
            Configs.linters_enabled[section] = [
                e for e in Configs.linters_enabled[section] if e not in values
            ]

    def _lang_linter_section(section: str, option: str) -> None:
        _, linter_name = section.split(":")
        if option == "executable":
            getattr(Configs, linter_name).executable = config_parser[section][option]
        if option == "options":
            getattr(Configs, linter_name).options.extend(
                re.split(r"[,\s]", config_parser[section][option])
            )
        if option == "config_file":
            value = config_parser[section][option]
            if value is None or value == "":
                raise ValueError(f"No configuration file given for option {option}")
            getattr(Configs, linter_name).set_config_file(value)

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    for section in config_parser:
        if section not in Configs.available_configs:
            raise ValueError(f"No such section supported: {section}")
        for option in config_parser[section]:
            if option not in Configs.available_configs[section]:
                raise ValueError(f"No such option supported: {section}.{option}")
            if (
                config_parser[section][option] is None
                or config_parser[section][option] == ""
            ):
                raise ValueError(f"Null value found for {section}.{option}")
            # [target] section
            if section == "target":
                _target_section(section, option)
            # [env] section
            elif section == "env":
                _env_section(section, option)
            # [language] section
            elif ":" not in section:
                _lang_section(section, option)
            # [language:linter] section
            else:
                _lang_linter_section(section, option)


def parse_args(args: argparse.Namespace) -> None:
    """Parse command line arguments

    Parameters
    ----------
    args : argparse.Namespace
        Arguments returned by `argparse.parse_args`

    Raises
    ------
    ValueError
        Invalid linter name found
    """

    def _enabled_linters() -> None:
        # Record linters given language by language
        enabled_linters: dict[str, list[str]] = {}
        for val in args.enabled_linters:
            lang, linter_name = val.split(":")
            if lang not in SUPPORTED_FILE_SUFFIXES:
                raise ValueError(f"No such language supported: {lang}")
            if linter_name not in Configs.linters_enabled[lang]:
                raise ValueError(f"No such linter supported: {lang}:{linter_name}")
            if lang in enabled_linters:
                enabled_linters[lang].append(linter_name)
            else:
                enabled_linters.update({lang: [linter_name]})
        # Assign the given linters
        for lang, linter_names in enabled_linters.items():
            Configs.linters_enabled[lang] = linter_names

    def _disabled_linters() -> None:
        disabled_linters: dict[str, list[str]] = {}
        for val in args.disabled_linters:
            lang, linter_name = val.split(":")
            if lang not in SUPPORTED_FILE_SUFFIXES:
                raise ValueError(f"No such language supported: {lang}")
            if linter_name not in Configs.linters_enabled[lang]:
                raise ValueError(f"No such linter supported: {lang}:{linter_name}")
            if lang in disabled_linters:
                disabled_linters[lang].append(linter_name)
            else:
                disabled_linters.update({lang: [linter_name]})
        # Assign the given linters
        for lang, linter_names in disabled_linters.items():
            Configs.linters_enabled[lang] = [
                e for e in Configs.linters_enabled[lang] if e not in linter_names
            ]

    def _linter_settings() -> None:
        for val in args.linter_settings:
            option, values = val.split("=")
            lang, option = option.split(":")
            linter_name, option = option.split(".")
            if lang not in SUPPORTED_FILE_SUFFIXES:
                raise ValueError(f"No such language supported: {lang}")
            if linter_name not in Configs.linters_enabled[lang]:
                raise ValueError(f"No such linter supported: {lang}:{linter_name}")
            if option not in Configs.available_configs[f"{lang}:{linter_name}"]:
                raise ValueError(
                    f"No such option supported: {lang}:{linter_name}.{option}"
                )
            if option == "executable":
                getattr(Configs, linter_name).executable = values
            if option == "options":
                values = re.split(r"[,\s]", values)
                getattr(Configs, linter_name).options.extend(values)
            if option == "config_file":
                getattr(Configs, linter_name).set_config_file(values)

    Configs.debug = args.debug
    Configs.target_dirs = args.target_dirs
    Configs.target_suffixes = args.target_suffixes
    if args.enabled_linters is not None:
        _enabled_linters()
    if args.disabled_linters is not None:
        _disabled_linters()
    if args.linter_settings is not None:
        _linter_settings()


def _install_extra_python_package_requirementss(requirement_file: str) -> None:
    """Install additional packages for linting"""
    if not os.path.exists(requirement_file):
        raise FileNotFoundError(f"No such file or directory: {requirement_file}")
    logger.info("Install extra python packages with %s...", requirement_file)
    cmd = ["pip", "install", "-r", requirement_file]
    logger.info("Install command: %s", " ".join(cmd))
    cmd_result = subprocess.run(cmd, capture_output=True)

    logger.info("Installation output:")
    for line in cmd_result.stdout.decode().strip().split("\n"):
        logger.info("\t%s", line)

    if cmd_result.returncode != 0:
        logger.error("Package installaltion failed:")
        for line in cmd_result.stderr.decode().strip().split("\n"):
            logger.error("\t%s", line)
        sys.exit(1)
