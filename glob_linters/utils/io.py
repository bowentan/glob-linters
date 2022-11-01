"""IO functions"""

import logging
import os
from pathlib import Path

from glob_linters.utils import settings

logger = logging.getLogger(__name__)


def print_configs() -> None:
    """Show configuration"""
    attr_names_sorted_logically = [
        "has_read_config_file",
        "debug",
        "linters_enabled",
        "target_dirs",
        "target_suffixes",
    ]
    logger.info("Configuration set:")
    for attr in attr_names_sorted_logically:
        if attr == "linters_enabled":
            for ext in settings.Configs.target_suffixes:
                for linter_name in settings.Configs.linters_enabled[ext]:
                    logger.info(
                        "\t%s - %s executable: %s, use configuration file: %s, "
                        "configuration file: %s",
                        ext,
                        linter_name,
                        getattr(settings.Configs, linter_name).executable,
                        getattr(settings.Configs, linter_name).use_config_file,
                        getattr(settings.Configs, linter_name).config_file
                        if getattr(settings.Configs, linter_name).use_config_file
                        else "NA",
                    )
        else:
            logger.info("\t%s: %s", attr, getattr(settings.Configs, attr))


def scan(target_dirs: list[str], suffixes: list[str]) -> dict[str, list[str]]:
    """Scan directories to obtain target files

    Parameters
    ----------
    target_dirs : list[str]
        Directories to be scanned
    suffix : list[str]
        Expected file suffix

    Returns
    -------
    dict[str, list[str]]
        Absolute paths of target files
    """
    target_files: dict[str, list[str]] = {s: [] for s in suffixes}
    target_dirs = [os.path.abspath(target_dir) for target_dir in target_dirs]
    logger.debug("Scanning directory: %s", target_dirs)
    for target_dir in target_dirs:
        for dirpath, _, filenames in os.walk(target_dir):
            for filename in filenames:
                f_path = Path(os.path.join(dirpath, filename))
                logger.debug("Found file: %s", f_path)
                if f_path.suffix in suffixes:
                    logger.debug("Found qualified file: %s", f_path)
                    target_files[f_path.suffix].append(str(f_path))
    return target_files
