#!/usr/bin/env fish

complete --do-complete="$argv" | grep -v "^$argv\$" | uniq
