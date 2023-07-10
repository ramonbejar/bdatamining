#/bin/bash
jupyter-nbconvert $1 --to slides --stdout > index.html
