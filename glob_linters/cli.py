"""Console script for glob_linters."""
import argparse
import logging
import os
import sys

from glob_linters.utils import io, settings

logger = logging.getLogger()


def _parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--target-dirs",
        dest="target_dirs",
        default=settings.Configs.target_dirs,
        nargs="*",
        type=str,
        help="Target directory containing files to be linted",
    )
    parser.add_argument(
        "-s",
        "--target-suffixes",
        dest="target_suffixes",
        default=settings.Configs.target_suffixes,
        nargs="*",
        type=str,
        help="Target file extensions, like '.cpp', '.py'",
    )
    parser.add_argument(
        "-g",
        "--enable-debug",
        dest="debug",
        action="store_true",
        help="Enable debug mode, output debusgging information",
    )
    parser.add_argument(
        "-E",
        "--enable-linters",
        dest="enabled_linters",
        default=None,
        nargs="*",
        type=str,
        help="Enable specific linters to use",
    )
    parser.add_argument(
        "-D",
        "--disable-linters",
        dest="disabled_linters",
        default=None,
        nargs="*",
        type=str,
        help="Disable specific linters to use",
    )
    parser.add_argument(
        "-x",
        "--extra-python-package-requirements",
        dest="extra_python_package_requirements",
        default=None,
        nargs="*",
        type=str,
        help="Extra python requirements file like for mypy extensions",
    )
    parser.add_argument(
        "-c",
        "--linter-settings",
        dest="linter_settings",
        default=None,
        nargs="*",
        type=str,
        help="Set configuration for linters, use `key=value` format and"
        "separate multiple pairs by space",
    )
    parser.add_argument(
        "-C",
        "--config-file",
        dest="config_file",
        default=None,
        type=str,
        help="glob_linters configuration file (glob-linter.ini) path",
    )
    return parser.parse_args(args)


def _parse_config() -> None:
    args = _parse_args(sys.argv[1:])
    if args.config_file is not None:
        if os.path.exists(args.config_file):
            settings.Configs.has_read_config_file = True
            settings.parse_config_file(args.config_file)
    else:
        settings.parse_args(args)


def lint(targets: dict[str, list[str]]) -> None:
    """Linting process

    Parameters
    ----------
    targets : dict[str, list[str]]
        Files as a list to be linted for each file suffix
    """
    for ext, filenames in targets.items():
        for linter_name in settings.Configs.linters_enabled[ext]:
            for filename in filenames:
                logger.info("-" * 120)
                settings.Configs.return_code |= getattr(
                    settings.Configs, linter_name
                ).lint(filename)


def _set_logger() -> None:
    # logger = logging.getLogger()
    if settings.Configs.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    stream.setFormatter(
        logging.Formatter("%(asctime)s - [%(levelname)s] : %(message)s")
    )
    logger.addHandler(stream)


def main() -> int:
    """Console script for glob_linters."""
    _parse_config()
    _set_logger()

    logger.info("=" * 120)
    if settings.Configs.has_read_config_file:
        logger.info("Configuration file found, used that")
    else:
        logger.info("Configuration file not found, used defaults or command arguments")
    io.print_configs()

    # Scan files
    logger.info("Starting directory scan: %s", settings.Configs.target_dirs)
    logger.info("Target suffix:")
    for suffix in settings.Configs.target_suffixes:
        logger.info("\t%s", suffix)
    target_files = io.scan(
        settings.Configs.target_dirs, settings.Configs.target_suffixes
    )
    logger.info("Target file list:")
    for lang, files in target_files.items():
        for file in files:
            logger.info("\t%s - %s", lang, file)

    # Linting
    logger.info("=" * 120)
    logger.info("Lint starting...")
    lint(target_files)

    return settings.Configs.return_code


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
