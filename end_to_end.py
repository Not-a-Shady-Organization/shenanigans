#!/usr/bin/env python

from subprocess import check_output
import requests
import sys
import click
import yaml
import os




@click.command()
@click.argument('yaml_file')
def download(yaml_file):
    with open(yaml_file) as f:
        flags = yaml.full_load(f)

    print(flags)
    args = ''
    try: 
        flags['video']['search_terms']
        args += flags['video']['search_terms']
    except:
        print("yaml must have search terms")

    if flags['video']['count']:
        args += ' --count ' + str(flags['video']['count'])

    if flags['video']['creative_commons']:
        args += ' --creative-commons'

    if flags['video']['res_4k']:
        args += ' --res-4k'

    if flags['video']['res_HD']:
        args += ' --res-HD'

    video_path_dir = os.path.dirname(os.path.realpath(__file__)) + '/videos/' + flags['video']['search_terms'].replace(" ", '_')

    command = f'python3 search-and-download {args}'
    check_output(command, shell=True)
    filepaths = os.listdir(video_path_dir)

    video_path = ''
    for fp in filepaths:
        if '.webm' in fp:
            video_path = fp
        if '.mkv' in fp:
            video_path = fp
    video_path = video_path_dir + '/' + video_path


    args = ''
    try: 
        flags['audio']['search_terms']
        args += flags['audio']['search_terms']
    except:
        print("yaml must have search terms")

    if flags['audio']['count']:
        args += ' --count ' + str(flags['audio']['count'])

    if flags['audio']['creative_commons']:
        args += ' --creative-commons'

    if flags['audio']['res_4k']:
        args += ' --res-4k'

    if flags['audio']['res_HD']:
        args += ' --res-HD'

    audio_path_dir = os.path.dirname(os.path.realpath(__file__)) + '/videos/' + flags['audio']['search_terms'].replace(" ", '_')

    command = f'python3 search-and-download {args}'
    check_output(command, shell=True)
    filepaths = os.listdir(audio_path_dir)

    audio_path = ''
    for fp in filepaths:
        if '.webm' in fp:
            audio_path = fp
        if '.mkv' in fp:
            audio_path = fp
    audio_path = audio_path_dir + '/' + audio_path

    print(video_path)
    print(audio_path)

    title = flags['upload']['title']
    command = f'python3 blend {video_path} {audio_path} --output-filepath "{title}".mkv'
    check_output(command, shell=True)


if __name__ == '__main__':
    download()