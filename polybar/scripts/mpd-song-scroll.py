#!/bin/python3

import threading
from time import sleep
from sys import exit
from mpd import MPDClient

MAX_LEN = 36
SLEEP_INTERVAL = 0.8


# Scroll through a song's name left and right like a music player
def scroll_song(name: str, max_len: int):
    t = threading.current_thread()
    t.name = name
    i = 1

    # Exit if max_len is greater than song length ( no need to scroll)
    if max_len > len(name):
        print(name, flush=True)
        return

    output = name[:max_len]
    print(output, flush=True)
    sleep(SLEEP_INTERVAL)

    while t.state != "stop":
        if t.state == "play":
            if i > len(name):
                i = 1

            output = name[i:max_len + i]

            if i + max_len > len(name):
                output += name[0:i]

            output = output[:max_len]

            i += 1
            print(output, flush=True)

        sleep(SLEEP_INTERVAL)


# Clean a song name, removing directory names and file type
def clean_song_name(song: str) -> str:
    # Strip directory names
    song = song.split("/")[-1]

    # Strip file name
    song_list = song.split(".")[:-1]

    #                           Add a space for formatting
    return "".join(song_list) + " "


def main():
    client = MPDClient()
    client.connect("localhost", 6600)

    # Check if a song is playing
    # If so, play the scroll
    # If not, play nothing

    if client.status()["state"] != "stop":
        song_name = client.currentsong().get("file")

        pretty_song_name = clean_song_name(song_name)

    else:
        song_name = ""
        pretty_song_name = ""

    t = threading.Thread(target=scroll_song,
                         args=(pretty_song_name, MAX_LEN))

    t.state = client.status()["state"]
    t.start()

    # Afterwards, check constantly for mpd changes
    # If song changes, change the song title
    # If song stops, print a blank line

    while True:
        client.idle("player")
        t.state = client.status()['state']

        if song_name != client.currentsong().get("file"):
            t.state = "stop"

            if client.status()["state"] != "stop":
                song_name = client.currentsong()["file"]
                pretty_song_name = clean_song_name(song_name)
                t = threading.Thread(target=scroll_song,
                                     args=(pretty_song_name, MAX_LEN))
                t.state = client.status()["state"]
                t.start()
            else:
                print("", flush=True)


if __name__ == "__main__":
    main()
