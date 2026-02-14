#!/bin/sh
#
# Suspend a MacOS system.
#
# This requires jumping through some hoops because of how the process is
# started. Ergo, the `nohup` call.

nohup sudo pmset sleepnow
while : ; do
        sleep 5
done
