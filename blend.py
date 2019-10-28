# Script modeled off this Stack answer
# https://stackoverflow.com/questions/12938581/ffmpeg-mux-video-and-audio-from-another-video-mapping-issue

import sys
from subprocess import check_output
import click

@click.command()
@click.option('--input-video', required=True, help='Video from which frames will be ripped and placed in the output video.')
@click.option('--input-audio', required=True, help='Video from which audio will be ripped and placed in the output video.')
@click.option('--output-filepath', default='blend.mp4')
def blend(input_video, input_audio, output_filepath):
    safe_filepath = lambda filepath: filepath.replace(' ', '\\ ')

    desired_visual_video = safe_filepath(input_video)
    desired_audio_video = safe_filepath(input_audio)
    output_path = safe_filepath(output_filepath)

    cross_streams_command = f'/usr/local/bin/ffmpeg -i {desired_visual_video} -i {desired_audio_video} -c copy -map 0:v:0 -map 1:a:0 -shortest {output_path}'
    check_output(cross_streams_command, shell=True)


if __name__ == '__main__':
    blend()
