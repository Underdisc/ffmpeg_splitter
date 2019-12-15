import getopt
import os
import os.path as path
import sys

def print_error(error):
    print("Error: " + str(error))

help_text = """
-= Usage =-
py splitter.py -c <timestamp_config> -m <media_file> [options]

-= Options =-
-h | --help : Print out this help message.
-c | --config : Specify the timestamp config file name.
-m | --media : Specify the media file name.
-f | --ffmpeg : Specify the command identifier for ffmpeg.
-s | --snakecase : Convert all output file names to snake case.
-d | --directory : Specify the directory where all output files will be written.
"""

def print_help():
    print(help_text)

args = sys.argv[1:]
short_options = "hc:m:f:sd:"
long_options = ["help", "config=", "media=", "ffmpeg=", "snakecase", "directory="]

try:
    p_args = getopt.getopt(
        args,
        short_options,
        long_options)
except getopt.error as error:
    print_error(str(error))
    sys.exit(1)

args_vals = p_args[0]
config_name = ""
media_name = ""
ffmpeg_name = "ffmpeg"
snake_case = False
directory = ""
for pair in args_vals:
    if pair[0] in ["-h", "--help"]:
        print_help()
        sys.exit(1)
    elif pair[0] in ["-c", "--config"]:
        config_name = pair[1]
    elif pair[0] in ["-m", "--media"]:
        media_name = pair[1]
    elif pair[0] in ["-f", "--ffmpeg"]:
        ffmpeg_name = pair[1]
    elif pair[0] in ["-s", "--snakecase"]:
        snake_case = True
    elif pair[0] in ["-d", "--directory"]:
        directory = pair[1]

if(config_name == ""):
    print_error("The config file must be specified with -c or --config.")
    sys.exit(1)
if(media_name == ""):
    print_error("The media file must be specified with -m or --media.")
    sys.exit(1)

config_exists = path.exists(config_name)
media_exists = path.exists(media_name)
if(not config_exists):
    print_error(config_name + " does not exist.")
    sys.exit(1)
if(not media_exists):
    print_error(media_name + " does not exist.")
    sys.exit(1)
if(directory != "" and not path.exists(directory)):
    print_error(directory + " directory does not exist")
    sys.exit(1)

config_file = open(config_name, "rt")
lines = config_file.readlines()
config_file.close()

split_texts = []
for line in lines:
    new_split = line.split(" ", 1)
    split_texts.append(new_split)

def find_time_in_seconds(time_text):
    seconds_in_hour = 3600
    seconds_in_minute = 60
    split_time = time_text.split(":")
    second_amount = 0
    if(len(split_time) == 3):
        second_amount = seconds_in_hour
    elif(len(split_time) == 2):
        second_amount = seconds_in_minute 

    time_in_seconds = 0 
    for time_amount_text in split_time:
        time_amount = int(time_amount_text)
        time_in_seconds = time_in_seconds + time_amount * second_amount
        second_amount = second_amount / seconds_in_minute
    return int(time_in_seconds)

def process_split_name(name_text, file_extension):
    if(snake_case):
        name_text = name_text.replace(" ", "_")
        name_text = name_text.lower()
    name_text = name_text.replace("\n", "")
    name = name_text + "." + file_extension
    return name

media_split = media_name.split(".");
if(len(media_split) != 2):
    print_error(media_name + " must end with a file extension.") 
    sys.exit(1)
media_extension = media_split[1]

splits = [] 
for split_text in split_texts:
    if(len(split_text) < 2):
        continue
    time = find_time_in_seconds(split_text[0])
    name = process_split_name(split_text[1], media_extension)
    split = []
    split.append(time)
    split.append(name)
    splits.append(split)

command_prefix = ffmpeg_name + " -hide_banner -loglevel panic -i " + media_name
command_prefix = command_prefix + " -acodec copy"
for i in range(0, len(splits) - 1):
    current_split = splits[i]
    next_split = splits[i + 1]
    start_time = current_split[0]
    end_time = next_split[0]
    duration = end_time - start_time 
    output = current_split[1]
    if(directory != ""):
        output = directory + "/" + output
    command_suffix = " -ss " + str(start_time)
    command_suffix = command_suffix + " -t " + str(duration)
    command_suffix = command_suffix + " \"" + output + "\""
    command = command_prefix + command_suffix
    os.system(command)

last_split = splits[len(splits) - 1]
start_time = last_split[0]
output = last_split[1]
if(directory != ""):
    output = directory + "/" + output
command_suffix = " -ss " + str(start_time) + " \"" + output + "\""
command = command_prefix + command_suffix
os.system(command)

