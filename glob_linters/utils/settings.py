"""Configuration"""
# Configuration vairables and defaults
# pylint: disable=invalid-name
# Signal control
import argparse
import configparser
import re
from dataclasses import dataclass, field


@dataclass
class Configs:
    # Exit code record
    return_code: int = field(default=0)
    # Executables
    cpplint_exec: str = field(default="cpplint")
    clang_format_exec: str = field(default="clang-format")

    # Lint targets settings
    target_dir: str = field(default=".")
    target_suffix: list[str] = field(default_factory=lambda: [".c", ".cpp", ".py"])

    # Running mode
    debug: bool = field(default=False)

    # Indicator of reading file
    has_read_config_file: bool = field(default=False)

    # Default config file
    DEFAULT_CONFIG_FILE: str = field(default="./glob-linters.ini")


class Configuration:
    def __init__(self) -> None:
        self.configs = Configs()

    def parse_config_file(self, config_file: str) -> None:
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        if "executable" in config_parser:
            exec_parser = config_parser["executable"]
            if "cpplint" in exec_parser:
                self.configs.cpplint_exec = exec_parser["cpplint"]
            if "clang-format" in exec_parser:
                self.configs.clang_format_exec = exec_parser["clang-format"]
        if "target" in config_parser:
            target_parser = config_parser["target"]
            if "target_dir" in target_parser:
                self.configs.target_dir = target_parser["target_dir"]
            if "target_suffix" in target_parser:
                self.configs.target_suffix = re.split(
                    ",| ", target_parser["target_suffix"]
                )
        if "mode" in config_parser:
            mode_parser = config_parser["mode"]
            if "debug" in mode_parser:
                self.configs.debug = True

    def parse_args(self, args: argparse.Namespace) -> None:
        self.configs.debug = args.debug
        self.configs.target_dir = args.target_dir
        self.configs.target_suffix = args.target_suffix
        self.configs.cpplint_exec = args.cpplint_exec
        self.configs.clang_format_exec = args.clang_format_exec
