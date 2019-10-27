#!/usr/bin/env python

from subprocess import check_output
import requests
from bs4 import BeautifulSoup
import sys
import youtube_dl

base_url = 'https://www.youtube.com/results?search_query='
search_terms = sys.argv[1:]
creative_commons_filter = '&sp=EgIwAQ%253D%253D'
url = base_url + '+'.join(search_terms) + creative_commons_filter

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
result_videos = soup.select('.yt-lockup-title')
video_urls = []
for result_video in result_videos:
    result_title_element = result_video.find('a')
    title = result_title_element['title']
    href = result_title_element['href']
    video_urls += ['http://www.youtube.com' + href]

    # Download all videos
    ydl = youtube_dl.YoutubeDL({'outtmpl': 'videos/'+title})

    with ydl:
        result = ydl.extract_info(url)

#    ffmpeg_command = f'ffmpeg -i {} -c copy -an example-nosound.mkv'
