# Creative Commons Blender
*Or: How we learned to stop downvoting and love the shitpost*

Create very long, very odd videos in minutes using Creative Commons Blender.

## Setup
Download necessary Python3 packages

`pip install -r requirements.txt`

And install [FFMPEG](https://www.ffmpeg.org/download.html)


## Downloading Videos
Creative Commons Youtube videos are downloaded using the `search-and-download` script as

`./search-and-download [SEARCH_TERMS]`

#### Example
`./search-and-download  lil bitty haikus`

Will search for videos matching "lil bitty haikus" and download them to `videos/lil_bitty_haikus/`.


## Blending Videos
Videos are treated as being either a video source or an audio source. To replace a video's audio with an audio source, use

`./blend INPUT_VIDEO INPUT_AUDIO`

#### Example

`./blend "videos/pony_vids/SEXX PO N PONY.mp4" "videos/gangsta_rap/Ice Cube - Gangsta Rap Made Me Do It"`

Will create a new video which has pony visuals set to gangsta rap.
