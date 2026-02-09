#!/usr/bin/env bash

#!/usr/bin/env bash
read -p "Enter the file name " name

if [ -e "$name" ]; then
    if [ -f "$name" ]; then
        echo "$name is a regular file."
    elif [ -d "$name" ]; then
        echo "$name is a repository."
    else
        echo "$name is a other type of file."

    fi
else
echo " file doesn't exist"
fi

