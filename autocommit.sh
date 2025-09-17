#!/bin/bash
WATCH_DIR="/home/workspaceuser/app"

# Get the current branch name
get_current_branch() {
    git -C "$WATCH_DIR" rev-parse --abbrev-ref HEAD
}

# Loop to monitor file changes
inotifywait -m -r -e modify,create,delete,move "$WATCH_DIR" --exclude ".git" |
while read -r path action file; do
    echo "Detected $action on $file in $path"
    CURRENT_BRANCH=$(get_current_branch)
    cd "$WATCH_DIR"
    git add .
    git commit -m "Auto-commit changes to $CURRENT_BRANCH"
    git push -u github "$CURRENT_BRANCH"
done