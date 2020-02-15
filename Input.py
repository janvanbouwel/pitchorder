import ffmpy
import os
import random
import json
from subprocess import PIPE


default_config = {"save_dir": "."}


def get_config():
    global default_config
    config = default_config
    try:
        with open("config.json", "r") as config_file:
            config.update(json.loads(config_file.read(-1)))
    except FileNotFoundError:
        pass
    return config


def gen_audio(video_path, audio_name, format=".wav"):
    outputname = audio_name + format
    ff = ffmpy.FFmpeg(inputs={video_path: None}, outputs={outputname: "-y -v quiet"})
    ff.run()
    return outputname


def gen_image_seq(video_path):
    folder = "img_seq"

    if not os.path.isdir(folder):
        os.mkdir(folder)

    ff = ffmpy.FFmpeg(inputs={video_path: None},
                      outputs={os.path.join(folder, "image%06d.jpg"): "-vsync 0 -v quiet -y -qscale:v 2"})
    ff.run()

    ffprobe = ffmpy.FFprobe(inputs={video_path: "-print_format json -v quiet -show_streams"})
    stdout, stderr = ffprobe.run(stdout=PIPE)
    output = json.loads(stdout)
    print(output)
    fps = 0
    for stream in output["streams"]:
        if stream["codec_type"] == "video":
            fps = stream["r_frame_rate"]
            break
    fps = eval(fps)
    return folder, fps
