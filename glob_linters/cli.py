"""Console script for glob_linters."""
import argparse
import logging
import os
import sys

from glob_linters import linters
from glob_linters.utils import io, settings


def parse_args(args: list[str], configs: settings.Configs) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--target-dir",
        dest="target_dir",
        default=configs.target_dir,
        type=str,
        help="",
    )
    parser.add_argument(
        "-s",
        "--file-suffix",
        dest="target_suffix",
        default=configs.target_suffix,
        nargs="*",
        type=str,
        help="",
    )
    parser.add_argument(
        "-g", "--enable-debug", dest="debug", action="store_true", help=""
    )
    parser.add_argument(
        "--cpplint",
        dest="cpplint_exec",
        default=configs.cpplint_exec,
        type=str,
        help="",
    )
    parser.add_argument(
        "--clang-format",
        dest="clang_format_exec",
        default=configs.clang_format_exec,
        type=str,
        help="",
    )
    return parser.parse_args(args)


def set_config() -> settings.Configuration:
    config = settings.Configuration()
    if os.path.exists(config.configs.DEFAULT_CONFIG_FILE):
        config.configs.has_read_config_file = True
        config.parse_config_file(config.configs.DEFAULT_CONFIG_FILE)
    elif len(sys.argv) > 1:
        args = parse_args(sys.argv[1:], config.configs)
        config.parse_args(args)
    return config


def set_logger(config: settings.Configuration) -> logging.Logger:
    logger = logging.getLogger()
    if config.configs.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    stream.setFormatter(io.CustomFormatter())
    logger.addHandler(stream)
    return logger


def main() -> int:
    """Console script for glob_linters."""
    config = set_config()
    logger = set_logger(config)

    if config.configs.has_read_config_file:
        logger.info("Configuration file found, used that")
    else:
        logger.info("Configuration file not found, used defaults or command arguments")
    logger.debug("Configuration set:")
    for key, value in vars(config.configs).items():
        if key == "DEFAULT_CONFIG_FILE":
            continue
        logger.debug("\t%s: %s", key, value)

    # Scan files
    logger.info("Starting directory scan: %s", config.configs.target_dir)
    logger.info("Target suffix:")
    for suffix in config.configs.target_suffix:
        logger.info("\t%s", suffix)
    target_files = io.scan(config.configs.target_dir, config.configs.target_suffix)
    logger.info("Target file list:")
    for lang, files in target_files.items():
        for file in files:
            logger.info("\t%s - %s", lang, file)

    # Linting
    logger.info("Lint starting...")

    logger.info("Linting .cpp...")
    logger.info("Initializing cpplint...")
    cpp_linter = linters.CppLinter("cpplint")
    for filename in target_files[".cpp"]:
        config.configs.return_code |= cpp_linter.lint(filename)
    logger.info("Initializing clang-format...")
    clang_format_linter = linters.ClangFormatLinter("clang-format")
    for filename in target_files[".cpp"]:
        config.configs.return_code |= clang_format_linter.lint(filename)

    return config.configs.return_code


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
