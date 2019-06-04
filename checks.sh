pytest
# pylint *.py
mypy --ignore-missing-imports *.py
pycodestyle --exclude=build,dist
