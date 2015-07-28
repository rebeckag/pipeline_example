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
import os
import re
import subprocess
import sys

# Threshold for code to pass the Pylint test. 10 is the highest score Pylint
# will give to any peice of code.
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


def execute_system_cmd(cmd, *args):
    try:
        output = subprocess.check_output(cmd, *args)
    except subprocess.CalledProcessError as e:
        output = e.output

    return output.decode("utf-8")


def indent_output(output):
    return "\n".join(["  " + line for line in output.splitlines()])


def py_files_changed():
    # Run the git command that gets the filenames of every file that has been
    # locally modified since the last commit.
    output = execute_system_cmd("git diff --staged --name-only HEAD".split())

    # Filter out non-python or deleted files.
    changed_files = [f.strip() for f in output.splitlines()]
    changed_py_files = [file
                        for file in changed_files
                        if file.endswith(".py") and os.path.exists(file)]

    return changed_py_files


def run_pylint():
    """Checks your git commit with Pylint."""

    changed_files = py_files_changed()

    # Run Pylint on each file, collect the results, and display them for the
    # user.
    results = {}
    for file in changed_files:
        output = execute_system_cmd("pylint -f text {}".format(file).split())

        results_re = re.compile(r"Your code has been rated at ([\d\.]+)/10")
        results[file] = float(results_re.findall(output)[0])

    # Display a summary of the results (if any files were checked).
    if len(results.values()) > 0:
        print("Pylint results:")
        for file in results:
            result = results[file]
            (grade, color) = (
                "FAIL", Colors.FAIL) if result < PYLINT_PASS_THRESHOLD else (
                "pass", Colors.OKGREEN)
            result_line = "[ {} ] {}: {:.2}/10".format(grade, file, result)
            print(color_text(indent_output(result_line), color))

    # Signal if any of the files failed the Pylint test
    if any(result < PYLINT_PASS_THRESHOLD for result in results.values()):
        print(color_text(
            "Not all files passed the Pylint threshold (>= {}).".format(
                PYLINT_PASS_THRESHOLD), Colors.FAIL))
        return False

    return True


def run_pep8():
    """Checks your git commit with pep8."""

    changed_files = py_files_changed()
    if not changed_files:
        return True

    cmd = ["pep8"]
    cmd.extend(changed_files)

    output = execute_system_cmd(cmd)

    # Signal if any of the files had a PEP8 violation
    if output:
        print(color_text("PEP8 style violations were detected.", Colors.FAIL))
        indented_output = indent_output(output)
        print(indented_output)
        return False

    print(color_text("No PEP8 style violations was detected.", Colors.OKBLUE))
    return True


if __name__ == "__main__":
    if not all([run_pep8(), run_pylint()]):
        print("git: fatal: code analysis failed, commit aborted")
        sys.exit(1)
