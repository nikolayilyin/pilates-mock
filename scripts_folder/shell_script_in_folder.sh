#!/bin/bash

full_out_path=$(realpath log_from_shell_script_in_folder.log)
log() {
  echo "$1" | tee -a "$full_out_path"
}

timeout="3s"

log "Shell script in folder executing at $(date "+%Y-%m-%d-%H:%M:%S")"
log "Going to sleep for $timeout" && sleep 3s
log "Shell script in folder executed at $(date "+%Y-%m-%d-%H:%M:%S")"
