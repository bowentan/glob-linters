"""IO functions"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


# class CustomFormatter(logging.Formatter):
#     grey = "\x1b[38;20m"
#     yellow = "\x1b[33;20m"
#     cyan = "\x1b[36:20m"
#     red = "\x1b[31;20m"
#     bold_red = "\x1b[31;1m"
#     reset = "\x1b[0m"
#     cformat = "%(asctime)s - [%(levelname)s] : %(message)s"

#     FORMATS = {
#         logging.DEBUG: cyan + cformat + reset,
#         logging.INFO: grey + cformat + reset,
#         logging.WARNING: yellow + cformat + reset,
#         logging.ERROR: red + cformat + reset,
#         logging.CRITICAL: bold_red + cformat + reset,
#     }

#     def format(self, record: logging.LogRecord) -> str:
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)


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
