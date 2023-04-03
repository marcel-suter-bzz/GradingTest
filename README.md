# Python-Template
## Introduction
This is the python template we use for our classes. It contains:
- main.py: Simple script
- main_test.py: A single pytest-case
- .gitignore: Used to exclude PyCharm settings
- requirements.txt: Basic requirements for python and pytest
## Workflows
### autograde.yml
This workflow contains a number of steps for the automation of classroom assignments.
#### grading
Autograding using the tests in /.github/classroom/autograding.json
#### copy-issues
Copy the issues from the template when creating the repository.
See [https://github.com/BZZ-Commons/copy-issues](https://github.com/BZZ-Commons/copy-issues:// "https://github.com/BZZ-Commons/copy-issues")
#### copy-testdata
This steps allows to import individual testdata when creating the repository. This is used to make cheating harder in marked assignments.
See [https://github.com/BZZ-Commons/set-testdata](http:/https://github.com/BZZ-Commons/set-testdata/ "https://github.com/BZZ-Commons/set-testdata")

### copyissues.yml
The workflow to copy the issues with manual trigger.
