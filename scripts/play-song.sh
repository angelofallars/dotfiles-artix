#!/bin/sh

folder=$(mpc ls | dmenu_gruv "Select Album:")
if [ $? != 0 ]
then
    exit
fi

if [ $1 = "album" ]
then
    mpc clear
    mpc insert "$folder"
    mpc play
    exit 0
fi

song=$(mpc ls "$folder" | dmenu_gruv "Select Song:")
if [ $? != 0 ]
then
    exit
fi

mpc clear
mpc insert "$song"
mpc play
