## ffmpeg splitter
The ffmpeg splitter will take a media file such as a mp3, wav, etc. and split that file into multiple files using a list of timestamps and names.

### How to use the ffmpeg splitter
Say we have a mp3 that contains multiple audio clips that are concatenated together in one large mp3 file. We'll call this file clips.mp3. The splitter can take that mp3 file and split those clips into different files using a timestamp config file.

*timestamps.txt*
```
00:00 one
00:06 two
02:04 three
10:50 four
01:01:40 Last Clip
```

To split clips.mp3 using the splitter, we can run the python script like this.

`py splitter.py -m clips.mp3 -c timestamps.txt`

**Important Note:** This might not work depending on the identifier used for ffmpeg in your shell environment. By default, the splitter uses *ffmpeg* as the identifier. You can change this using `-f` or `--ffmpeg`.

`py splitter.py -m clips.mp3 -c timestamps.txt -f <your_ffmpeg_command>`

Assuming no errors occur, this will produce the following files in the working directory.
```
one.mp3
two.mp3
three.mp3
four.mp3
Last Clip.mp3
```

### Formatting option

I hate spaces and caps in my file names and I always avoid it when I can. If you want the same, you can use `-s` or `--snakecase` to format the output file names to snake case. Using this option will result in a file named *last_clip.mp3* instead of *"Last Clip.mp3"*.

### Output directory option
If you want all of the output files to end up in a different directory, you can use `-d` or `--directory` to do that.
