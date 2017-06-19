#!/bin/bash

find . -type d -exec bash -c 'cd "$0" && gunzip -c *.gz | cut -f 3 >> ../../MonthData.txt' {} \;
