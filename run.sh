#!/usr/bin/env bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id --user)/bus
cd ~/.scw
$(which python3) main.py > log.txt
