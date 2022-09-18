"""IO functions"""

import inspect
import logging
import os
from pathlib import Path

from glob_linters import linters
from glob_linters.utils import settings

logger = logging.getLogger(__name__)


def print_configs() -> None:
    logger.debug("Configuration set:")
    for attr, value in inspect.getmembers(settings.Configs):
        if attr.startswith("__"):
            continue
        if attr in ["return_code", "set_configs", "DEFAULT_CONFIG_FILE_PATH"]:
            continue
        if isinstance(value, linters.Linter):
            logger.debug("\t%s: %s", attr, value.executable)
        else:
            logger.debug("\t%s: %s", attr, value)


def scan(target_dir: str, suffix: list[str]) -> dict[str, list[str]]:
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
    target_files: dict[str, list[str]] = {s: [] for s in suffix}
    target_dir = os.path.abspath(target_dir)
    logger.debug("Scanning directory: %s", target_dir)
    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            f_path = Path(os.path.join(dirpath, filename))
            logger.debug("Found file: %s", f_path)
            if f_path.suffix in suffix:
                logger.debug("Found qualified file: %s", f_path)
                target_files[f_path.suffix].append(str(f_path))
    return target_files
