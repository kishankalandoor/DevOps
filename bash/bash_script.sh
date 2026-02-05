#!/bin/bash

# Ask the user for their age
read -p "Enter your age: " Age

# Check if the input is a valid number and compare
if [ "$Age" -ge 18 ]; then
    echo "You are $Age years old. You can vote!"
else
    echo "You are only $Age. You cannot vote yet."
fi
