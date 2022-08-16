#!/bin/sh

set -o errexit

exit_handler() {
    if [ $? -ne 0 ]; then
        echo "Failure" >&2
    fi
}

trap exit_handler EXIT

testinfra_tests=$(find molecule/ -name 'test_*.py')

echo "Running ansible-lint..."
ansible-lint

echo "Running pylint..."
pylint ${testinfra_tests}

echo "Running black..."
black --check ${testinfra_tests}

echo "Success"
