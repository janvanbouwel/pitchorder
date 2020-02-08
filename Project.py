import os
import time

import Input
import Processing
import Output

import youtube_dl


def make_all(name, url):
    while os.path.isdir(name):
        name += "1"
    os.mkdir(name)
    os.chdir(name)

    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video_path = os.listdir(os.getcwd())[0]
    audioname = "audio"

    audio_path = Input.gen_audio(video_path, audioname)
    print(audio_path)

    interval = 0.05
    indexes, sr = Processing.make_ordered_audio(interval, audio_path, "sorted.wav")

    print("starting image sequence")
    tic = time.clock()
    folder, fps = Input.gen_image_seq(video_path)
    toc = time.clock()
    print(f"image sequence made, took {toc - tic}")
    print(fps)

    out = ""
    for index in indexes:
        for path in Output.frames_to_paths(folder, Output.index_to_frame(index, sr, interval, fps)):
            if os.path.exists(path):
                out += f'file \'{path}\'\n'

    with open("images.txt", "w") as f:
        f.write(out)

    print("combining")
    Output.combine("images.txt", "sorted.wav", "result.mp4", fps)
    print("done, saved to result.mp4")
    os.chdir("..")



