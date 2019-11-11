#!/usr/bin/env python

from subprocess import check_output
import requests
import sys
import yaml
import os
import argparse
from search_and_download import search_and_download

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def download(yaml_file, not_blend=False, not_upload=False):
    print_creative_commons_blender()

    try:
        flags = yaml.full_load(yaml_file)
    except:
        with open(yaml_file) as f:
            flags = yaml.full_load(f)

    video_path_dir = os.path.dirname(os.path.realpath(__file__)) + '/videos/' + flags['video']['search_terms'].replace(" ", '_')
    downloaded_videos = search_and_download(
        flags['video']['search_terms'],
        flags['video']['count'],
        flags['video']['creative_commons'],
        flags['video']['res_4k'],
        flags['video']['res_HD']
    )

    filepaths = os.listdir(video_path_dir)
    video_path = video_path_dir + '/' + best_video(filepaths)


    audio_path_dir = os.path.dirname(os.path.realpath(__file__)) + '/videos/' + flags['audio']['search_terms'].replace(" ", '_')
    search_and_download(
        flags['audio']['search_terms'],
        flags['audio']['count'],
        flags['audio']['creative_commons'],
        flags['audio']['res_4k'],
        flags['audio']['res_HD']
    )

    filepaths = os.listdir(audio_path_dir)
    audio_path = audio_path_dir + '/' + best_video(filepaths)


    if not_blend:
        print('Exiting early due to --not-blend flag')
        return

    print('About to blend...')
    title = flags['upload']['title']
    command = f'python3 blend {video_path} {audio_path} --output-filepath "blended-videos/{title}".mkv'
    check_output(command, shell=True)
    print('Blending complete')

    if not_upload:
        print('Exiting early due to --not-upload flag')
        return

    print(f'About to upload as {title}')
    upload_command = f'python3 upload_videos.py --file "blended-videos/{title}.mkv" --title "{title}" --description "{flags["audio"]["search_terms"] + " " + flags["video"]["search_terms"]}"'
    print('Uploading...')
    check_output(upload_command, shell=True)
    print('Upload complete')


def best_video(filepaths):
    for fp in filepaths:
        if '.webm' in fp:
            return fp
        if '.mp4' in fp:
            return fp
        if '.mkv' in fp:
            return fp


def print_creative_commons_blender():
    print('''
       _____                _   _
      / ____|              | | (_)
     | |     _ __ ___  __ _| |_ ___   _____
     | |    | '__/ _ \\/ _` | __| \\ \\ / / _ \\
     | |____| | |  __| (_| | |_| |\\ V |  __/
      \\_____|_|  \\___|\\__,_|\\__|_| \\_/ \\___|
      / ____|
     | |     ___  _ __ ___  _ __ ___   ___  _ __  ___
     | |    / _ \\| '_ ` _ \\| '_ ` _ \\ / _ \\| '_ \\/ __|
     | |___| (_) | | | | | | | | | | | (_) | | | \\__ \\
      __________/|_| |_| |_|__ |_| |_|\\___/|_| |_|___/

                   _______|___|______
                __|__________________|
                \  ]________________[ `---.
                 `.                   ___  |
                  |   _              |   | |
                  | .'_`--.___   __  |   | |
                  |( 'o`   - .`.'_ ) |   | |
                  | `-._      `_`./_ |  / /
                  |   '/\\\\    ( .'/ )|.' /
                  \\ ,__//`---'`-'_   |__/  .'
                   \\/-'        '/  /.'
                    \\            '/'
                     | `.`-. .-'.'|
                     |  `.-'.-'   |
                     |__(__(___)__|
                     /            \\
                    /              \\
                    |______________|
        ''')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file')
    parser.add_option('--not-blend', dest='not_blend', action='store_true')
    parser.add_option('--not-upload', dest='not_upload', action='store_true')
    args = parser.parse_args()

    download(yaml_file, not_blend, not_upload)
