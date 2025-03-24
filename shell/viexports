#!/bin/sh
#
# Confirm that the exports(5) provided will work before replacing the system
# copy of exports.
#
# This is similar to `crontab -e` or `visudo`.
#
# shellcheck shell=dash

set -eu

PROGNAME="${0##*/}"

log()
{
	local level=$1; shift

	echo "${PROGNAME}: $level: $*"
}

error()
{
	log "ERROR" "$@"
}

: "${EDITOR=vi}"
SYSTEM_EXPORTS="/etc/exports"

exports_tmp=$(mktemp)
trap 'rm -f $exports_tmp' EXIT INT TERM

if [ -e "$SYSTEM_EXPORTS" ]; then
	cp -f "$SYSTEM_EXPORTS" "$exports_tmp"
fi

set +eu

while true; do
	"$EDITOR" "$exports_tmp"
	if nfsd -F "$exports_tmp" checkexports; then
		break
	fi
	while true; do
		read -r -p "Retry edit? [y/n]> " response
		case "$response" in
		[yY])
			break
			;;
		[nN])
			exit 1
			;;
		*)
			error "Bad response: '$response'."
			;;
		esac
	done
done

cmp -s "$exports_tmp" "$SYSTEM_EXPORTS"
exit_code=$?
if [ "$exit_code" -ne 1 ]; then
	exit "$exit_code"
fi
while true; do
	read -r -p "Install edited file? [y/n]> " response
	case "$response" in
	[yY])
		mv -f "$exports_tmp" "$SYSTEM_EXPORTS"
		break
		;;
	[nN])
		exit 1
		;;
	*)
		error "Bad response: '$response'."
		;;
	esac
done
