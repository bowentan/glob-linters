"""Linters"""
# pylint: disable=subprocess-run-check

import logging
import os
import subprocess

logger = logging.getLogger(__name__)

# User-defined linter config directory for GitHub action
USER_DEFIEND_LINTER_CONFIG_ROOT: str = ".github/linter-configs"


class Linter:
    """Linter parent class"""

    def __init__(self, executable: str) -> None:
        self.executable = executable
        self.options: list[str] = []
        self.cmd_result: subprocess.CompletedProcess
        self.stdout: list[str]
        self.stderr: list[str]
        self.config_file: str = ""
        self.use_config_file: bool = False

    def lint(self, filename: str) -> int:
        """General linting method

        Parameters
        ----------
        filename : str
            File path to be linted

        Returns
        -------
        int
            Return code of the linter program
        """
        logger.info("Linting with [%s] on file %s", self.executable, filename)
        cmd = [self.executable] + self.options + [filename]
        logger.debug("Linting command: %s", " ".join(cmd))
        self.cmd_result = subprocess.run(cmd, capture_output=True)
        self.stdout = self.cmd_result.stdout.decode().strip().split("\n")
        self.stderr = self.cmd_result.stderr.decode().strip().split("\n")

        self.process_output()
        return self.cmd_result.returncode

    def set_config_file(self, filepath: str) -> None:
        """Set configuration file

        Parameters
        ----------
        filepath : str, optional
            Path of configuration, by default `.github/linter-configs/.clang-format`
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file or directory: {filepath}")

    def process_output(self) -> None:
        """Process output, since some linters print errors to stdout"""
        logger.debug("Linter stdout:")
        for out in self.stdout:
            logger.debug("\t%s", out)

        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stderr:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


# Linters for c/c++
class ClangFormat(Linter):
    """`clang-format` linter"""

    DEFAULT_CONFIG_FILE_PATH = ".clang-format"

    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--dry-run", "--Werror"]

    def set_config_file(
        self,
        filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, ".clang-format"),
    ) -> None:
        super().set_config_file(filepath)
        if os.path.exists(self.DEFAULT_CONFIG_FILE_PATH):
            os.remove(self.DEFAULT_CONFIG_FILE_PATH)
        os.symlink(filepath, self.DEFAULT_CONFIG_FILE_PATH)
        self.use_config_file = True
        self.config_file = filepath


class Cpplint(Linter):
    """`cpplint` linter"""

    DEFAULT_CONFIG_FILE_PATH = "CPPLINT.cfg"

    def set_config_file(
        self,
        filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, "CPPLINT.cfg"),
    ) -> None:
        super().set_config_file(filepath)
        if os.path.exists(self.DEFAULT_CONFIG_FILE_PATH):
            os.remove(self.DEFAULT_CONFIG_FILE_PATH)
        os.symlink(filepath, self.DEFAULT_CONFIG_FILE_PATH)
        self.use_config_file = True
        self.config_file = filepath


# Linters for Python
class Pylint(Linter):
    """`pylint` linter"""

    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--output-format=parseable"]

    def set_config_file(
        self, filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, ".pylintrc")
    ) -> None:
        super().set_config_file(filepath)
        self.options.extend(["--rcfile", filepath])
        self.use_config_file = True
        self.config_file = filepath

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Flake8(Linter):
    """`flake8` linter"""

    def set_config_file(
        self, filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, ".flake8")
    ) -> None:
        super().set_config_file(filepath)
        self.options.extend(["--config", filepath])
        self.use_config_file = True
        self.config_file = filepath

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Black(Linter):
    """`black` linter"""

    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--check", "--diff"]

    def set_config_file(
        self, filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, ".black")
    ) -> None:
        super().set_config_file(filepath)
        self.options.extend(["--config", filepath])
        self.use_config_file = True
        self.config_file = filepath

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Isort(Linter):
    """`isort` linter"""

    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--check-only", "--diff"]

    def set_config_file(
        self,
        filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, ".isort.cfg"),
    ) -> None:
        super().set_config_file(filepath)
        self.options.extend(["--settings-file", filepath])
        self.use_config_file = True
        self.config_file = filepath

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Mypy(Linter):
    """`mypy` linter"""

    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--pretty", "--show-error-context", "--show-error-codes"]

    def set_config_file(
        self,
        filepath: str = os.path.join(USER_DEFIEND_LINTER_CONFIG_ROOT, ".mypy.ini"),
    ) -> None:
        super().set_config_file(filepath)
        self.options.extend(["--config-file", filepath])
        self.use_config_file = True
        self.config_file = filepath

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
            for err in self.stderr:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")
