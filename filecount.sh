#!/usr/bin/env bash


count_files(){

count_files=$(find . -maxdepth 1 -type f |  wc -l)
echo "file count is $count_files"
}
count_files
