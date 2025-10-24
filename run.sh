#!/bin/bash
read -ra raw_name <<< "$(ls ./*.py 2>/dev/null)"

file_name="${raw_name[*]}"
file_name="${file_name:2}"

command -v poetry >/dev/null 2>&1
is_poetry_exists=$?

command -v python >/dev/null 2>&1
is_python_exists=$?

if [[ is_poetry_exists -eq 0 && is_python_exists -eq 0 ]]; then
    if [[ $file_name != "" ]]; then
        poetry install --no-root
        poetry run python "$file_name"
    else
        echo "Error: No such file or directory"
        exit 1
    fi

    exit 0
elif [[ is_poetry_exists -eq 1 && is_python_exists -eq 0 ]]; then
    echo "Warning: 'poetry' command is not recognized"

    if [[ $file_name != "" ]]; then
        pip install "customtkinter"
        python "$file_name"
    else
        echo "Error: No such file or directory"
        exit 1
    fi

    exit 0
else
    echo "Error: 'python' command is not recognized"
    exit 127
fi