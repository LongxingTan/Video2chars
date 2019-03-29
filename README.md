# Video2chars
彩色字符画, end2end generate a video whose image is transfered to characters, like this
![result](https://github.com/LongxingTan/Video2chars/blob/master/out.png)

## dependencies
- moviepy
- PIL
- numpy

## usage
it works for both movie and picture
- python run.py
- if movie: video.movie2movie('./data/example.MOV', 'out.mp4')
- if picture: video.frame2frame('./data/example.jpg','out.png') 
