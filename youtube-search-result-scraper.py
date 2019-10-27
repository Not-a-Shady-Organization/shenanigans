import requests
from bs4 import BeautifulSoup
import sys

base_url = "https://www.youtube.com/results?search_query="
search_terms = sys.argv[1:]
creative_commons_filter = '&sp=EgIwAQ%253D%253D'
url = base_url + "+".join(search_terms) + creative_commons_filter

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
result_videos = soup.select('.yt-lockup-title')
for result_video in result_videos:
    result_title_element = result_video.find('a')
    title = result_title_element['title']
    href = result_title_element['href']
    print(f'T: {title}\nL:{href}\n\n')
