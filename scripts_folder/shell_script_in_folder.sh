#!/bin/bash -x

full_out_path=$(realpath log_from_shell_script_in_folder.log)

echo "Shell script in folder executing at $(date "+%Y-%m-%d-%H:%M:%S")" >> "$full_out_path"
sleep 3s
echo "Shell script in folder executed at $(date "+%Y-%m-%d-%H:%M:%S")" >> "$full_out_path"