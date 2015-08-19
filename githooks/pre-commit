#!/usr/bin/env python

"""
A pre-commit hook for git that uses Pylint for automated code review.

If any python file's rating falls below the ``PYLINT_PASS_THRESHOLD``, this
script will return nonzero and the commit will be rejected.

This script must be located at ``$REPO/.git/hooks/pre-commit`` and be
executable.

Copyright 2009 Nick Fitzgerald - MIT Licensed.
Modified work Copyright 2015 Rebecka Gulliksson - MIT Licensed.
"""
from contextlib import contextmanager
import os
import re
import subprocess
import sys

# Threshold for code to pass the Pylint test. 10 is the highest score Pylint
# will give to any peice of code.
import tempfile
import shutil

PYLINT_PASS_THRESHOLD = 7


class FailedCheck(Exception):
    pass


class Colors(object):
    OKGREEN = '\033[32m'
    OKBLUE = '\033[94m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'


def color_text(text, color):
    return color + text + Colors.ENDC


def execute_system_cmd(cmd):
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        output = e.output

    return output.decode("utf-8")


def indent_output(output):
    return "\n".join(["  " + line for line in output.splitlines()])


def only_py_files(files):
    return [f for f in files if f.endswith(".py")]


def run_pylint(files):
    """Checks your git commit with Pylint."""

    py_files = only_py_files(files)

    # Run Pylint on each file, collect the results, and display them for the
    # user.
    results = {}
    for file in py_files:
        output = execute_system_cmd("pylint -f text {}".format(file).split())

        results_regexp = re.compile(
            r"Your code has been rated at (-?[\d\.]+)/10")
        matches = results_regexp.findall(output)
        if not matches:  # pylint did not give the expected output
            results[file] = float("-inf")  # set -inf to enforce manual check
        else:
            results[file] = float(matches[0])

    # Display a summary of the results (if any files were checked).
    if len(results.values()) > 0:
        print("Pylint results:")
        for file in results:
            result = results[file]
            (grade, color) = (
                "FAIL", Colors.FAIL) if result < PYLINT_PASS_THRESHOLD else (
                "pass", Colors.OKGREEN)
            result_line = "[ {} ] {}: {:.2f}/10".format(grade, file, result)
            print(color_text(indent_output(result_line), color))

    # Signal if any of the files failed the Pylint test
    if any(result < PYLINT_PASS_THRESHOLD for result in results.values()):
        print(color_text(
            "Not all files passed the Pylint threshold (>= {}).".format(
                PYLINT_PASS_THRESHOLD), Colors.FAIL))
        return False

    return True


def run_pep8(files):
    """Checks your git commit with pep8."""

    py_files = only_py_files(files)
    if not py_files:
        return True

    cmd = ["pep8"]
    cmd.extend(py_files)

    output = execute_system_cmd(cmd)

    # Signal if any of the files had a PEP8 violation
    if output:
        print(color_text("PEP8 style violations were detected.", Colors.FAIL))
        indented_output = indent_output(output)
        print(indented_output)
        return False

    print(color_text("No PEP8 style violations was detected.", Colors.OKBLUE))
    return True


@contextmanager
def git_staged_files():
    """Ensure only the staged version of files are used for the checks instead
    of the working copy."""

    tmp_dir = tempfile.mkdtemp()

    # find all added/copied/modified/renamed files in git staging
    files = execute_system_cmd(
        "git diff --staged --name-only --diff-filter=ACMR".split())

    # write the staged file content (not the working copy) to a temporary file
    files = files.splitlines()
    for file in files:
        file = file.strip()
        tmp_filename = os.path.join(tmp_dir, file)

        # make sure any sub directory is created
        cmd = "mkdir -p {}".format(
            os.path.dirname(os.path.abspath(tmp_filename)))
        execute_system_cmd(cmd.split())

        # write the staged file to a temporary file
        cmd = "git show :{}".format(file)
        data = execute_system_cmd(cmd.split())
        # manually write to file since stdout redirect won't work with execute_system_cmd
        with open(tmp_filename, "w") as f:
            f.write(data)

    # change working dir to get prettier file paths in output
    with working_directory(tmp_dir):
        yield files.splitlines()

    shutil.rmtree(tmp_dir)


@contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


if __name__ == "__main__":
    with git_staged_files() as files:
        if not all([run_pep8(files), run_pylint(files)]):
            print("git: fatal: code analysis failed, commit aborted")
            sys.exit(1)
