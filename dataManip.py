import scipy.io.wavfile
import matplotlib.pyplot as plt
import pydub
import numpy as np
import os
from scipy import signal
from scipy.fftpack import fft, fftshift
import librosa


def convert_mp3(usr_input):
    path = "recordings/" + usr_input + "/"
    wav_path = path + "wav files/"
    if not os.path.exists(wav_path):
        os.makedirs(wav_path)
    i = 0
    for file in os.listdir(path):
        if file.endswith('.mp3'):
            mp3 = pydub.AudioSegment.from_mp3(path + file)
            file_name = usr_input.replace(" ", "") + "-" + str(i)
            mp3.export(wav_path + file_name + ".wav", format="wav")
            i += 1


def resample_44k (usr_input):
    path = "recordings/" + usr_input + "/"
    wav_path = path + "wav files/"
    new_path = wav_path + "44k/"
    os.makedirs(new_path)
    for file in os.listdir(wav_path):
        if file.endswith('.wav'):
            audData, rate = librosa.load(wav_path + file, sr=None)
            if rate == 48000:
                ds_rate = 44100
                temp = librosa.resample(audData, rate, ds_rate)
                librosa.output.write_wav(new_path + file, temp, sr=ds_rate)
            if rate == 44100:
                librosa.output.write_wav(new_path + file, audData, sr=rate)


def segment_wav (usr_input):
    path = "recordings/" + usr_input + "/"
    wav_path = path + "wav files/"
    new_path = wav_path + "44k/"
    #split audio file into 500ms segments
    for file in os.listdir(new_path):
        stop = 0
        count = 0
        step = 0
        segment_size = 0          #length of audio file segment in ms
        segment_step_size = 150     #step size of audio file segment in ms
        window_size = 512           #Hann window sample size
        window_step_size = 256      #Hann window step size
        if file.endswith('.wav'):
            call, rate = librosa.load(new_path + file, sr=None)
            segment_size = rate // 2
            int(segment_size)
            call_length = len(call)
            print(call_length)
            print(segment_size)
            stop = (call_length - 500) // segment_step_size
            print(stop)
            while count < stop:
                segment = call[step:segment_size + step]
                f, t, Zxx = scipy.signal.stft(segment, rate, "hann", window_size, window_step_size, nfft = None, boundary = None, padded = False, axis = 0)
                fig = plt.pcolormesh(t, f, np.abs(Zxx))
                plt.axis('off')
                fig.axes.get_xaxis().set_visible(False)
                fig.axes.get_yaxis().set_visible(False)
                plt.savefig(new_path + usr_input + str(count) + ".png", bbox_inches='tight', pad_inches=0)
                step += segment_step_size
                count += 1

usr_input = input("Please enter the species name: ")
#resample_44k (usr_input)
segment_wav (usr_input) 