import sys

import scipy.io.wavfile
import os
import numpy as np
from tqdm import tqdm


### based partially on https://github.com/mzucker/python-tuner

min_freq = 30

max_freq = 16000


class Chunk:
    @staticmethod
    def freq_to_note_number(freq):
        return int(69 + 12 * np.log2(freq / 440.0))

    def __init__(self, index, data, SR):
        self.index = index
        self.data = data
        self.SR = SR
        self.note = -index

    def calc_note(self):
        mono = (self.data[:, 0] / 2) + (self.data[:, 1] / 2)
        window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, len(mono), False)))
        global min_freq, max_freq
        imax = min(max_freq, len(mono))
        fft = np.fft.rfft(mono * window)
        FREQ_STEP = float(self.SR) / len(mono)
        try:
            freq = (np.abs(fft[min_freq:imax]).argmax() + min_freq) * FREQ_STEP
        except ValueError:
            freq = (np.abs(fft).argmax() + min_freq) * FREQ_STEP
        self.note = self.freq_to_note_number(freq)
        return


def get_audio(audio_path):
    SR, audio = scipy.io.wavfile.read(audio_path)
    return SR, audio


def split_audio(SR, interval, audio, start_n=0):
    n_int = int(interval * SR)
    chunks = []
    i = 0
    while True:
        if (i + 1) * n_int > len(audio):
            chunks.append(Chunk(i, audio[i * n_int:], SR))
            break
        elif (i + 1) * n_int == len(audio):
            break
        else:
            chunks.append(Chunk(i, audio[i * n_int: (i + 1) * n_int], SR))

        i += 1
    return chunks


def calc_note(chunks):
    for chunk in tqdm(chunks):
        chunk.calc_note()


def sort(chunks):
    sorted_chunks = sorted(chunks, key=lambda x: x.note)
    return [chunk.index for chunk in sorted_chunks]


def get_sorted_audio(chunks, length):
    indexes = sort(chunks)

    sorted_audio = []
    for index in tqdm(indexes):
        sorted_audio.extend(chunks[index].data)
    #  print(sorted_audio)
    sorted_audio = np.array(sorted_audio, dtype=chunks[0].data.dtype)
    return indexes, sorted_audio


def make_audio(filename, audio, SR):
    scipy.io.wavfile.write(filename, SR, audio)


def make_ordered_audio(interval, audio_path, audio_out):
    SR, audio = get_audio(audio_path)
    print("audio got")
    chunks = split_audio(SR, interval, audio)
    print("audio split")
    calc_note(chunks)
    print("note got")
    indexes, sorted_audio = get_sorted_audio(chunks, len(audio))
    print("audio sorted")
    make_audio(audio_out, sorted_audio, SR)
    print("audio made")
    return indexes, SR


if __name__ == "__main__":
    os.chdir("project")
    audio_path = "darude.wav"

    if not os.path.isfile(audio_path):
        print("error")
        sys.exit()
    interval=0.2
    make_ordered_audio(interval, audio_path, "reverse.wav")
