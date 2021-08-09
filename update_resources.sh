#!/bin/bash

# This will update a git submodule at yalm/resources
git submodule update --remote

# We need to make an empty __init__.py file for every subdirectories
for d in $(find yalm/resources -type d -name "[^_]*"); do
  touch ${d}/__init__.py
done
