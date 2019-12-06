# ASCII-art-video-converter

You can convert any image or video to the ASCII art using script `ascii_converter.py`. It takes 5 command line arguments:

1. type_process - type of the file to convert (string, 'video' or 'image')
2. input_file - path to the input video/image
3. height - height of the result ASCII-video/image file (integer from 1 to 2000)
4. width - width of the result ASCII-video/image file (integer from 1 to 2000)
5. output_file - path to the output ASCII-video/image file

For example, to convert file `wave.jpg` into the ASCII-art, you can just run the following command:

`python ascii_converter.py image wave.jpg 60 150 image.txt`

After converting, you can watch your video/image via the special player. In order to do this, just open file `player.html`, select corresponding converted file, and enjoy watching!
