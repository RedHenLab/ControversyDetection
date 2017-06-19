#!/bin/bash

find . -type d -exec bash -c 'cd "$0" && rm *.json.gz' {} \;
