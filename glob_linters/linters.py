"""Linters"""
# pylint: disable=subprocess-run-check

import logging
import subprocess

logger = logging.getLogger(__name__)


class Linter:
    """Linter data class to hold common variables"""

    def __init__(self, executable: str) -> None:
        self.executable = executable
        self.options: list[str] = []
        self.cmd_result: subprocess.CompletedProcess
        self.stdout: list[str]
        self.stderr: list[str]

    def lint(self, filename: str) -> int:
        logger.info("Linting with [%s] on file %s", self.executable, filename)
        cmd = [self.executable] + self.options + [filename]
        logger.debug("Linting command: %s", " ".join(cmd))
        self.cmd_result = subprocess.run(cmd, capture_output=True)
        self.stdout = self.cmd_result.stdout.decode().strip().split("\n")
        self.stderr = self.cmd_result.stderr.decode().strip().split("\n")

        self.process_output()
        return self.cmd_result.returncode

    def process_output(self) -> None:
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
    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--dry-run", "--Werror"]


class Cpplint(Linter):
    pass


# Linters for Python
class Pylint(Linter):
    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--output-format=parseable"]

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Flake8(Linter):
    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Black(Linter):
    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--check", "--diff"]

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Isort(Linter):
    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--check-only", "--diff"]

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")


class Mypy(Linter):
    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.options = ["--pretty", "--show-error-context", "--show-error-codes"]

    def process_output(self) -> None:
        if self.cmd_result.returncode != 0:
            logger.error("Found errors:")
            for err in self.stdout:
                logger.error("\t%s", err)
        else:
            logger.info("Check passed.")
