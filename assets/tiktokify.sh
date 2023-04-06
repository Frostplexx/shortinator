#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 input_file.mp4"
  exit 1
fi

input_file="$1"
output_file="$(basename "$input_file" .mp4)-%d.mp4"
width=1080
height=1920
clip_duration=50

ffmpeg -i "$input_file" -an -filter_complex "[0:v]scale=-1:1920, crop=1080:1920" temp.mp4

ffmpeg -i temp.mp4 -c copy -an -f segment -segment_time $clip_duration -reset_timestamps 1 -map 0 "clips/$output_file"

rm temp.mp4
