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
        "--target-dir",
        dest="target_dir",
        default=settings.Configs.target_dir,
        type=str,
        help="",
    )
    parser.add_argument(
        "-s",
        "--file-suffix",
        dest="target_suffix",
        default=" ".join(settings.Configs.target_suffix),
        nargs="*",
        type=str,
        help="",
    )
    parser.add_argument(
        "-g", "--enable-debug", dest="debug", action="store_true", help=""
    )
    parser.add_argument(
        "-c", "--configs", dest="configs", default=None, nargs="+", help=""
    )
    parser.add_argument(
        "-s",
        "--config-file",
        dest="config_file",
        default=settings.DEFAULT_CONFIG_FILE_PATH,
        help="",
    )
    return parser.parse_args(args)


def _parse_config() -> None:
    if os.path.exists(settings.DEFAULT_CONFIG_FILE_PATH):
        settings.Configs.has_read_config_file = True
        settings.parse_config_file(settings.DEFAULT_CONFIG_FILE_PATH)
    elif len(sys.argv) > 1:
        args = _parse_args(sys.argv[1:])
        settings.parse_args(args)


def lint(targets: dict[str, list[str]]) -> None:
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
    settings.load_linter_configs()
    logger.info("-" * 120)
    settings.install_mypy_package_requirements()

    logger.info("=" * 120)
    if settings.Configs.has_read_config_file:
        logger.info("Configuration file found, used that")
    else:
        logger.info("Configuration file not found, used defaults or command arguments")
    io.print_configs()

    # Scan files
    logger.info("Starting directory scan: %s", settings.Configs.target_dir)
    logger.info("Target suffix:")
    for suffix in settings.Configs.target_suffix:
        logger.info("\t%s", suffix)
    target_files = io.scan(settings.Configs.target_dir, settings.Configs.target_suffix)
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
