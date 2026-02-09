#!/usr/bin/env bash

read -p "enter the number" num

if [ "$num" -gt 20 ]; then
   echo "grater than 20"
else
 echo "lesser than 20"

fi

if [ $((num%2)) -eq 0 ]; then
   echo "number is even"
else
 echo "the number is odd"

fi







