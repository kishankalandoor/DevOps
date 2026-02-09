#!/usr/bin/env bash
read -p "ENter the directory " BASE_DIR

if [ ! -d "$BASE_DIR" ]; then
echo " directory not found "

exit 1
fi


for dir in "$BASE_DIR"/*;  do
     
   
      file_count=$(find "$BASE_DIR" -maxdepth 1 -type f | wc -l)

         if  [ "$file_count" -gt 5 ]; then 
             
            echo "DIRECTORY: $BASE_DIR  contains $file_count "


         for file in "$BASE_DIR"/*; do
                if [ -f "$file" ];then
                      echo "$(basename " $file")"
                fi
             done
                  echo
          fi
        
  done
               
     

