#!/usr/bin/env fish

complete --do-complete="$argv" | string match -rv '^'(string escape --style=regex "$argv")'(\s|$)' | uniq
