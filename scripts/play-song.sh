#!/bin/sh

song=$(mpc ls "$1" | dmenu_gruv -p "Play Music:")
mpc clear
mpc insert "$song"
mpc play
