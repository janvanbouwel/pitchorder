import os
import ffmpy


def index_to_frame(index, sr, length, fps):
    start = int(float(index) * length * fps)
    stop = int(float(index + 1) * length * fps)

    return [i+1 for i in range(start, stop)]


def frames_to_paths(folder, frames):
    out = []
    for frame in frames:
        out.append(os.path.join(folder, f"image{frame:06d}.jpg"))
    return out


def combine(images, audio_path, result, fps):
    ff = ffmpy.FFmpeg(inputs={images: f"-y -r {fps} -f concat -safe 0", audio_path: None},
                      outputs={result: f"-vf fps={fps} -v quiet -c:v h264_nvenc -b:v 5M -b:a 1M"})
    ff.run()