#! /bin/bash

set -e

flake8 backend
black --check backend
isort backend --check
bandit -r backend
