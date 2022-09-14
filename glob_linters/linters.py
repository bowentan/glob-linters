"""Linters"""
# pylint: disable=subprocess-run-check

import logging
import subprocess

logger = logging.getLogger(__name__)


class Linter:
    """Linter data class to hold common variables"""

    def __init__(self, executable: str) -> None:
        self.executable = executable
        self.lint_options: list[str] = []
        self.cmd_result: subprocess.CompletedProcess
        self.stdout: list[str]
        self.stderr: list[str]

    def lint(self, filename: str) -> int:
        logger.info("Linting with [%s] on file %s", self.executable, filename)
        cmd = [self.executable] + self.lint_options + [filename]
        logger.debug("Linting command: %s", " ".join(cmd))
        self.cmd_result = subprocess.run(cmd, capture_output=True)
        self.stdout = self.cmd_result.stdout.decode().strip().split("\n")
        self.stderr = self.cmd_result.stderr.decode().strip().split("\n")

        logger.debug("Linter output:")
        for out in self.stdout:
            logger.debug("\t%s", out)

        if len(self.stderr) > 0:
            logger.error("Errors found:")
            for err in self.stderr:
                logger.error("\t%s", err)

        return len(self.stderr) | 0


class ClangFormatLinter(Linter):
    def __init__(self, executable: str) -> None:
        super().__init__(executable)
        self.lint_options = ["--dry-run"]


class CppLinter(Linter):
    pass
