"""IO functions"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


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
