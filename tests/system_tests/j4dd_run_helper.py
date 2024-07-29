"""Run j4-dmenu-desktop with set environment and print good error messages."""

from __future__ import annotations

import os  # noqa: I001
import pathlib
import shlex
import subprocess
from typing import Iterable, NamedTuple


class J4ddRunError(Exception):
    """J4-dmenu-desktop couldn't be executed/returned with nonzero exit status."""

    pass


def _assemble_error_message(
    stdout: str,
    stderr: str,
    override_env: dict[str, str],
    args: Iterable[str],
) -> str:
    """Assemble an informative error message about j4-dmenu-desktop execution.

    Error message generated by this function doesn't include the cause of the
    problem, they only describe the environment. Functions should prepend the
    error cause to the returned value.

    Args:
        stdout: stdout contents
        stderr: stderr contents
        override_env: overriden environment variables
        args: commandline executed

    Returns:
        Error message.
    """
    message = ""
    if stdout not in ("", "\n"):
        message += "".join(
            f"    {line}" for line in stdout.splitlines(keepends=True)
        )

    message += "Stderr:\n"

    if stderr not in ("", "\n"):
        message += "".join(
            f"    {line}" for line in stderr.splitlines(keepends=True)
        )

    message += "To reproduce:\n"
    if len(override_env) == 0:
        reproducer = ""
    else:
        reproducer = " ".join(
            f"{key}={shlex.quote(value)}"
            for key, value in override_env.items()
        )
        reproducer += " "

    reproducer += shlex.join(args)

    message += f"    {reproducer}\n"

    return message


class _ProcessedEnvironment(NamedTuple):
    args: list[str]
    env: dict[str, str]


class AsyncJ4ddResult:
    """Result of run_j4dd() with asynchronous=True."""

    def __init__(
        self,
        j4dd_process: subprocess.Popen[str],
        override_env: dict[str, str],
        cmdline: Iterable[str],
        shouldfail: bool,
    ):
        """Internal initor.

        This initor should be only called by run_j4dd().
        """
        self._j4dd_process = j4dd_process
        self._override_env = override_env
        self._cmdline = cmdline
        self._shouldfail = shouldfail

    def wait(self, timeout: None | int | float = None) -> None:
        """Wait for j4-dmenu-desktop to finish.

        Arguments:
            timeout: timeout for the wait

        Raises:
            Same as run_j4dd().
        """
        stdout, stderr = self._j4dd_process.communicate(timeout=timeout)
        if self._shouldfail:
            if self._j4dd_process.returncode == 0:
                raise J4ddRunError(
                    "j4-dmenu-desktop exitted with return code 0!\n"
                    + _assemble_error_message(
                        stdout, stderr, self._override_env, self._cmdline
                    )
                )
        else:
            if self._j4dd_process.returncode != 0:
                raise J4ddRunError(
                    f"j4-dmenu-desktop exitted with return code "
                    f"{self._j4dd_process.returncode}!\n"
                    + _assemble_error_message(
                        stdout, stderr, self._override_env, self._cmdline
                    )
                )


def run_j4dd(
    j4dd_executable_path: pathlib.Path,
    override_env: dict[str, str],
    *j4dd_arguments: str,
    shouldfail: bool = False,
    asynchronous: bool = False,
) -> None | AsyncJ4ddResult:
    """Run j4-dmenu-desktop.

    Args:
        j4dd_executable_path: path to j4-dmenu-desktop executable
        override_env: environment variables to override
        j4dd_arguments: arguments given to j4-dmenu-desktop
        shouldfail: should j4-dmenu-desktop fail? If yes, J4ddRunError will be
            raised if j4-dmenu-desktop exits with zero exit status.
        asynchronous: if true, do not wait for j4-dmenu-desktop to finish
            execution. If true, return an object that can be waited for later.

    Raises:
        J4ddRunErrorr: If j4-dmenu-desktop doesn't exit successfully.

    Returns:
        None if asynchronous is False,
    """
    # This function doesn't accept j4dd_exe as str directly because having the
    # location as a pathlib.Path could be useful in the future (although it
    # isn't currently used in this implementation).
    j4dd_path_string = str(j4dd_executable_path)

    args: list[str]
    if "MESON_EXE_WRAPPER" in os.environ:
        args = (
            shlex.split(os.environ["MESON_EXE_WRAPPER"])
            + [j4dd_path_string]
            + list(j4dd_arguments)
        )
    else:
        args = [j4dd_path_string] + list(j4dd_arguments)

    env = os.environ.copy()
    for key, val in override_env.items():
        env[key] = val

    if not asynchronous:
        result = subprocess.run(args, capture_output=True, text=True, env=env)
        if shouldfail:
            if result.returncode == 0:
                raise J4ddRunError(
                    "j4-dmenu-desktop exitted with return code 0!\n"
                    + _assemble_error_message(
                        result.stdout, result.stderr, override_env, args
                    )
                )
        else:
            if result.returncode != 0:
                raise J4ddRunError(
                    f"j4-dmenu-desktop exitted with return code "
                    f"{result.returncode}!\n"
                    + _assemble_error_message(
                        result.stdout, result.stderr, override_env, args
                    )
                )
    else:
        async_result = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
        )
        return AsyncJ4ddResult(async_result, override_env, args, shouldfail)
    return None
