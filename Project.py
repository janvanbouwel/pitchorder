import os
import time
import tempfile
import shutil

import Input
import Processing
import Output

import youtube_dl


def make_all(name, url):
    config = Input.get_config()
    current_dir = os.getcwd()
    save_dir = os.path.abspath(config["save_dir"])
    os.makedirs(save_dir, exist_ok=True)

    temp_dir = tempfile.mkdtemp(prefix=name)
    print(f"temp dir is located at: {temp_dir}")
    os.chdir(temp_dir)

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
    file_path = os.path.join(save_dir, f"{name}_result.mp4")
    Output.combine("images.txt", "sorted.wav", file_path, fps)
    print(f"done, saved to {file_path}")
    os.chdir(current_dir)
    shutil.rmtree(temp_dir)



