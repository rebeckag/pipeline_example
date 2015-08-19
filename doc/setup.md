# One-time setup
* Setup local git hook for running `pep8` and `pylint` before commit:
  * `pip install pep8 pylint`
    * If you're using git in PyCharm, make sure to install the packages
      globally (with `sudo`), even if you are using virtual environments
      (PyCharm does not activate virtual environments in Terminal).

    * If you're using git from the command line and virtual environments with
      `virtualenvwrapper`, add the install command to
      `$VIRTUALENVWRAPPER_HOOK_DIR/postmkvirtualenv` to make sure pep8 and
      pylint is available in all newly created virtual environments).

  * Create a git template directory and add it to the global git configuration:

         ```bash
         mkdir ~/.git_template
         git config --global init.templatedir '~/.git_template'
         ```

  * Make the `githooks/pre-commit.py` script a *pre-commit hook*:

         ```bash
         cp githooks/pre-commit ~/.git_template/hooks/pre-commit
         chmod u+x ~/.git_template/hooks/pre-commit
         ```

  * Re-initialize all local git repositories with `git init`.

  * Now, anytime you run `git commit`, the pre-commit
    script will be invoked and check all staged files for pep8 and pylint
    violations. If you, for some unexplainable reason, want to bypass these
    checks, just do `git commit --no-verify` (but shame on you if you do;
    either fix the issues or configure pep8/pylint properly!).

# For new projects

* Make a project on GitHub and connect it to Travis CI:
  * Go to https://travis-ci.org/profile/.
  * Sync Travis with GitHub (so the new project is visible in the list).
  * Enable Travis for the new project.

* Create a small project skeleton:
  * `README`
  * `.gitignore`
  * `.travis.yml`
  * `tox.ini`
  * `pylintrc`
  * `requirements.txt`
  * any initial code or documentation

* Configure pep8: see `[pep8]` entry in `tox.ini`.

* Configure Pylint: see example `pylintrc`. Use `[MESSAGES CONTROL]` to minimize
the output produced by Pylint. All messages (and their code) can be found at
http://docs.pylint.org/features.html

       ```
       [MESSAGES CONTROL]
       # Only produce global evaluation report (RP0004)
       enable=RP0004
       disable=RP0001,RP0002,RP0003,RP0101,RP0401,RP0402,RP0701,RP0801
       ```

* Start producing awesome stuff
  * Write tests
  * Write code
  * Fix tests
  * Repeat ad absurdum.

# Using the tools
To make the best use of the Travis-GitHub integration I propose the following
steps:

* Use a feature branch to develop.
* Push the branch to GitHub.
* Wait for the result from Travis.
* If the feature is complete and all unit tests pass, make a pull request and
  merge it into the master branch.

Make sure to configure `pylint` and `pep8` appropriately (by disabling some
excessive reporting), making it easier to distinguish important issues.
