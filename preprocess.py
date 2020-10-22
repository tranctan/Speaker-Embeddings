"""
This file preprocesses input, including:
- Resample to 16kHz, convert to mono (single channel)
- Normalize volume
- Convert wav to mel-spectrogram
- Eliminate silence ranges using VAD
This part requires the most domain knowledge of Digital Signal Processing (DSP)
"""

import numpy as np
import webrtcvad
import librosa
import yaml
from scipy.io.wavfile import read
from scipy.ndimage.morphology import binary_dilation

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
    Settings: 
        - 40-channels mel spectrograms
        - 25ms window width
        - 10ms window step
    Note: This is not log-mel as original paper.
    """
    frames = librosa.feature.melspectrogram(
        wav,
        sr=hparams["SAMPLING_RATE"],
        n_fft=int(sampling_rate * hparams["MEL_WINDOW_LENGTH"] / 1000), # length of FFT window
        hop_length=int(sampling_rate * hparams["MEL_WINDOW_STEP"] / 1000)= , # number of samples between successive frames
        n_mels=hparams["N_MEL_CHANNELS"]
    )
    return frames.astype(np.float32)


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
    
    :param wav: raw audio waveform, float numpy array
    :return: the same waveform with silences trimmed away 
    """
    # Compute the voice detection window size - how many samples in VAD_WINDOW_LENGTH milliseconds
    samples_per_window = (hparams["VAD_WINDOW_LENGTH"] * sampling_rate) // 1000

    # Trim the end of audio to make sure the whole signal have a multiple of window size
    wav = wav[:len(wav) - (len(wav) % samples_per_window)]

    # Convert float raw waveforms to 16-bit mono PCM
    pcm_wave = struct.pack("%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16))
    
    # Perform VAD
    voice_flags = []
    vad = webrtcvad.Vad(mode=3) # most aggresive mode
    for window_start in range(0, len(wav), samples_per_window):
        window_end = window_start + samples_per_window
        voice_flags.append(vad.is_speech(pcm_wave[window_start * 2:window_end * 2],
                                         sample_rate=sampling_rate))
    voice_flags = np.array(voice_flags)
    
    # Smooth the voice detection with a moving average
    def moving_average(array, width):
        array_padded = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))
        ret = np.cumsum(array_padded, dtype=float)
        ret[width:] = ret[width:] - ret[:-width]
        return ret[width - 1:] / width

    audio_mask = moving_average(voice_flags, vad_moving_average_width)
    # Binarize after moving average
    audio_mask = np.round(audio_mask).astype(np.bool)

    # Dilate the voiced regions
    audio_mask = binary_dilation(audio_mask, np.ones(hparams["VAD_MAX_SILENCE_LENGTH"]))
    audio_mask = np.repeat(audio_mask, samples_per_window)

    return wav[audio_mask==True]

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