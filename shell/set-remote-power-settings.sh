#!/bin/sh
#
# Power settings which are sane for secure remote host use.

pmset -a autopoweroff 0
pmset -a powernap 0
pmset -a standby 0
pmset -a proximitywake 0
pmset -a tcpkeepalive 0
pmset -a ttyskeepawake 0
pmset -a womp 1
pmset -a destroyfvkeyonstandby 1
pmset hibernatemode -c 3
pmset hibernatemode -b 25
pmset hibernatemode -u 25
