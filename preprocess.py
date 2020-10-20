"""
This file preprocesses input, including:
- Resample to 16kHz, convert to mono (single channel)
- Normalize volume
- Convert wav to mel-spectrogram
- Eliminate silence ranges using VAD
"""

import numpy as np
import webrtcvad
import librosa
import yaml
from scipy.io.wavfile import read

CONFIG_DIR = './hparams.yaml'
# Read hyper-params from config file
hparams = {}
with open(CONFIG_DIR) as file:
    hparams = yaml.load(file, Loader=yaml.FullLoader)

INT16_MAX = (2 ** 15) - 1

#TODO: Speed up preprocessing using Multiprocessing

def wav_to_mel(wav):
    """
    This function derives a mel-spectrogram 
    ready to be used by the encoder.
    Note: This is not log-mel
    """
    pass


def normalize_volume(wav, target_dBFS, increase_only=False, decrease_only=False):
    """
    This function normalizes volume to a target dBFS
    """
    # Calculate dBFS of raw audio signal
    rms = np.sqrt(np.mean((wav * INT16_MAX) ** 2))
    wave_dBFS = 20 * np.log10(rms / INT16_MAX)

    dBFS_residual = target_dBFS - wave_dBFS

    if dBFS_residual < 0 and increase_only or\
        dBFS_residual > 0 and decrease_only:
        return wav
    return wav * (10 ** (dBFS_residual / 20))


def trim_long_silence(wav):
    """
    This function shortens long silences using VAD
    Ensuring that segments without voice in the waveform 
    remain no longer than a threshold determined by the VAD 
    parameters in config file
    """
    pass


def preprocess_wav(input_dir):
    """
    This function takes wavs from input directory
    And return a processed wav
    """
    sr, wav = read(input_dir)

    # Resampling to 16kHz
    wav = librosa.resample(wav, sr, hparams["SAMPLING_RATE"])

    # Preprocessing: Normalize volume and shorten long silences
    wav = normalize_volume(wav)
    wav = trim_long_silence(wav)

    return wav

preprocess_wav("asd")