#!/bin/bash
#
# This script is ran by .xinitrc
#
# Set primary mode if 1 monitor is available
# and extend right mode if 2.
MONS_INFO=$(mons | head -n 1)
MONS_NUM=$(echo "$MONS_INFO" | grep -oP '\d+')

if [ "$MONS_NUM" -eq 1 ]; then
    mons -o
elif [ "$MONS_NUM" -eq 2 ]; then
    mons -e right
else
    echo "Unexpected number of monitors: $MONS_NUM"
fi
