#!/bin/bash
if [[ $1 == "restart" ]] ; then
   launchctl unload "$HOME/Library/LaunchAgents/TGFP Discord Bot.plist"
   launchctl load "$HOME/Library/LaunchAgents/TGFP Discord Bot.plist"
elif [[ $1 == "start" ]] ; then
   launchctl load "$HOME/Library/LaunchAgents/TGFP Discord Bot.plist"
elif [[ $1 == "stop" ]] ; then 
   launchctl unload "$HOME/Library/LaunchAgents/TGFP Discord Bot.plist"
elif [[ $1 == "status" ]] ; then
   launchctl list "TGFP Discord Bot"
else
    echo "restart, start, stop, status, log, clear_logs"
fi
