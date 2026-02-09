#!/usr/bin/env bash


read path 

if [ -e "$path" ]; then
  echo "path exists"
else
   echo "path doesn't exists"
fi


