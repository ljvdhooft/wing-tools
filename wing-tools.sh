#!/bin/bash

# Check if the first argument (Python script name) is provided
if [ -z "$1" ]; then
  echo "Error: Please provide a tool."
  exit 1
fi

python_file="$1"
shift

python3 "/Users/ljvdhooft/Documents/02 DEV - Python/wing-tools/$python_file.py" "$@"