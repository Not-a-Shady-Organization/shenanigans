#!/usr/bin/env python

from subprocess import check_output
import requests
from bs4 import BeautifulSoup
import sys
import youtube_dl
import click
import argparse



def search_and_download(search_terms, count=1, creative_commons=False, res_4k=False, res_hd=False):
    '''This script searchs for videos Youtube for Creative Commons which match the given terms, then downloads them.'''

    base_url = 'https://www.youtube.com/results?search_query='

    creative_commons_filter = '&sp=EgIwAQ%253D%253D'
    resolution_4k_filter = '&sp=EgJwAQ%253D%253D'
    creative_commons_4k_filter = '&sp=EgQwAXAB'
    resolution_HD_filter = '&sp=EgIgAQ%253D%253D'
    creative_commons_HD_filter = '&sp=EgQgATAB'

    # Create URL for the Youtube video search
    youtube_search_url = ''
    if creative_commons:
        youtube_search_url = base_url + search_terms.replace(' ', '+') + creative_commons_filter
    if res_4k:
        youtube_search_url = base_url + search_terms.replace(' ', '+') + resolution_4k_filter
    if res_hd:
        youtube_search_url = base_url + search_terms.replace(' ', '+') + resolution_HD_filter
    if creative_commons and res_4k:
        youtube_search_url = base_url + search_terms.replace(' ', '+') + creative_commons_4k_filter
    if creative_commons and res_hd:
        youtube_search_url = base_url + search_terms.replace(' ', '+') + creative_commons_HD_filter
    if youtube_search_url == '':
        youtube_search_url = base_url + search_terms.replace(' ', '+')

    # Request the search page from Youtube
    page = requests.get(youtube_search_url)

    # List all video elements on the search results page
    soup = BeautifulSoup(page.content, 'html.parser')
    result_videos = soup.select('.yt-lockup-title')

    if len(result_videos) == 0:
        print('No results!')
        # TODO: Add error here
        return

    downloaded_videos = []
    for result_video in result_videos[:int(count)]:
        # Grab title and link for each video in the results
        result_title_element = result_video.find('a')
        title = result_title_element['title']
        href = result_title_element['href']
        video_url = 'http://www.youtube.com' + href

        logger.print('Video Found: ' + title)

        # Download
        output_subdirectory = search_terms.replace(' ', '_')
        output_video_title = title.replace(' ', '_').replace('"', '').replace("'", '').replace('(', '').replace(')', '').replace('|', '')
        output_video_path = 'videos/' + output_subdirectory + '/' + output_video_title

        ydl = youtube_dl.YoutubeDL({
            'outtmpl': output_video_path,
            'noplaylist': True,
            'logger': logger,
            'progress_hooks': [hook]
        })

        with ydl:
            result = ydl.extract_info(video_url)

        downloaded_videos += [output_video_path]

    return downloaded_videos



def hook(d):
    if d['status'] == 'finished':
        print('Download complete')

import itertools
spinner = itertools.cycle(['-', '/', '|', '\\'])


class Logger(object):
    def print(self, text):
        print(text)

    def debug(self, msg):
        if 'has already been downloaded and merged' in msg:
            print('Video has already been downloaded.')

        elif 'Resuming' in msg:
            print('Resuming download...')

        elif 'Destination' in msg:
            print(msg[11:])

        elif 'Merging' in msg:
            print(msg[9:])

        else:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')



    def warning(self, msg):
        if msg != 'Requested formats are incompatible for merge and will be merged into mkv.':
            print(msg)

    def error(self, msg):
        print(msg)

logger = Logger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('searchterms', nargs='+')
    parser.add_argument('-c', '--count', help='Number of videos to download')
    parser.add_argument('--creative-commons', dest='creative_commons', action='store_true', help='Filter searched videos to Creative Commons only')
    parser.add_argument('--res-4k', dest='res_4k', action='store_true', help='Filter searched videos to 4k resolution only')
    parser.add_argument('--res-HD', dest='res_HD', action='store_true', help='Filter searched videos to HD resolution only')
    args = parser.parse_args()

    search_and_download(
        ' '.join(args.searchterms),
        args.count,
        args.creative_commons,
        args.res_4k,
        args.res_HD
    )
