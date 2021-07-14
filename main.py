#!/usr/bin/env python3
import os
import shutil

from mp3_tagger import MP3File

from src.partag3.tag_on_page import TagOnPage
from src.partag3.utils import get_config, track_nat_sort


def main():
    config = get_config()

    path = config.pop('path', './')

    artist = config.pop('artist', None)
    year = config.pop('year', None)
    song_selector = config.pop('songs', None)

    # Get original files
    files = [file for file in os.listdir(path) if file.endswith('.mp3')]
    files.sort(key=track_nat_sort)

    # Parse songs
    songs = TagOnPage('song', config['url'], selector=song_selector).list_from_siblings
    # Make dir
    album_path = os.path.join(path, config['album'])
    os.makedirs(album_path)

    # Copy files and set tags
    for i in range(len(files)):
        src = os.path.join(path, files[i])
        track = i + 1
        ext = os.path.splitext(src)[1]
        new_file_name = f'{track} {songs[i]}{ext}'
        dst = os.path.join(album_path, new_file_name)
        print(f'Setting: {new_file_name}')

        mp3 = MP3File(shutil.copy(src, dst))

        if artist is not None:
            mp3.artist = artist
        mp3.album = config['album']
        mp3.track = track
        mp3.song = songs[i]
        if year is not None:
            mp3.year = year

        mp3.save()


if __name__ == '__main__':
    main()
