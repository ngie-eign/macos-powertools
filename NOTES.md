# Introduction

This file contains a number of other random functions/ideas for how to manage MacOS systems.

# Configure/Enable NFS Server

```shell
sudo nfsd enable
```

# Poke Hole Through Firewall for Mosh

Prior to Sequoia, this is how I was poking holes in the MacOS firewall for
`mosh-server`:

```shell
function Fix-Mosh-Firewall-Rules {
        local fw='/usr/libexec/ApplicationFirewall/socketfilterfw'
        local mosh_sym="$(which mosh-server)"
        local mosh_abs="$(realpath $mosh_sym)"

        sudo "$fw" --setglobalstate off
        sudo "$fw" --add "$mosh_sym"
        sudo "$fw" --unblockapp "$mosh_sym"
        sudo "$fw" --add "$mosh_abs"
        sudo "$fw" --unblockapp "$mosh_abs"
        sudo "$fw" --setglobalstate on
}
```

It's unclear if this works anymore though, based on recent personal experience
with Sequoia.

This code is based on this [StackExchange answer](https://apple.stackexchange.com/a/474803).
