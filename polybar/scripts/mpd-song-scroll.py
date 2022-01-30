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
    i = 0

    # Exit if max_len is greater than song length ( no need to scroll)
    if max_len > len(name):
        print(name, flush=True)
        return

    while getattr(t, "do_run", True):
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

    song_name = client.currentsong()['file']
    formatted_song_name = clean_song_name(song_name)

    # if len(song_name) > MAX_LEN:
    #     scroll_song(song_name, MAX_LEN)
    # else:
    #     print(song_name)
    #     return 0

    # Open a thread to scroll through song name
    t = threading.Thread(target=scroll_song,
                         args=(formatted_song_name, MAX_LEN))
    t.start()

    # Listen for player changes
    while True:
        client.idle('player')

        # Change the scrolling song when the mpd song changes
        if client.currentsong()['file'] != song_name:
            t.do_run = False

            song_name = client.currentsong()['file']
            song_name = clean_song_name(song_name)

            t = threading.Thread(target=scroll_song,
                                 args=(song_name, MAX_LEN))
            t.start()


if __name__ == "__main__":
    main()
