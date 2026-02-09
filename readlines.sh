#!/usr/bin/env bash

# Ask user for file name
read -p  "path of the file " filepath

if [ -f "$filepath" ];then

   filename=$(basename "$filepath")
   filelines=$(wc -l <  "$filepath")


echo "file name is $filename ;  Number of lines   "$filelines" "

else 
echo "error"

fi


