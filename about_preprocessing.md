# About preprocessing step

This step requires only pure Python, but with a solid amount of knowledge about DSP or audio manipulation.

This preprocessing step includes:
- `normalize_volume()` - Normalize volume to a target dBFS
- `wav_to_mel()` - Convert wav to mel-spectrogram
- `trim_long_silence()` - Eliminate silence ranges using VAD
- `preprocess_wav()` - Resample to 16kHz, and include the above steps

Below are details about each step.

### `normalize_volumes()`
This function normalizes the input raw audio signal to a target dBFS (Decibels relative to full scale), which is a measurement for amplitude levels in digital systems, such as PCM. The level of 0dBFS is assigned to be the maximum possible digital level. For example, a signal that reaches 50% of the maximum level has a level of −6 dBFS, which is 6 dB below full scale. 

In order to get the dBFS of a raw audio signal array:
For signal values between -1 and 1:
```
valueDBFS = 20*log10(abs(value))
```

If you have values between another range, for example 16bit, then it's:
```
valueDBFS = 20*log10(abs(value)/32768)
```
(because 16bit integer signed has values between -32768 and +32767, e.g. 2^15=32768)

And so the general formula is:
```
valueDBFS = 20*log10(abs(value)/maxValue)
```

After calculate the target dBFS, we revert it back to raw audio signal at the end of the function.

### `wav_to_mel()`
This functions convert raw audio signal to mel-scaled spectrogram, which is a popular feature engineering step for audio/signal processing. A good article on mel-spectrogram is [here](https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53)

The input to the function is the raw audio signals array, and the output is the resulted mel-spectrogram as a numpy array with shape (n_mels, t)

The necessary parameters for the function are:
- y: raw signal array
- sr: sampling rate
- n_fft: length of Fast-Fourier Transform (FFT) window
- hop_length: number of samples between successive frames
- n_mels: number of mel-channels

The above parameters are defined in the paper as follow: 
> The inputs to the model are 40-channels log-mel spectrograms with a 25ms
window width and a 10ms step.

### `trim_long_silence()`
As the authors of Resemblyzer indicated: 
"To avoid segments that are mostly silent when sampling partial utterances from complete utterances, we use the [webrtcvad](https://github.com/wiseman/py-webrtcvad) python package to perform Voice Activity Detection (VAD). This yields a binary flag over the audio corresponding to whether or not the segment is voiced. We perform a **moving average** on this binary flag to smooth out short spikes in the detection, which we then binarize again. Finally, we perform a **dilation** on the flag with a kernel size of $s + 1$, where $s$ is the maximum silence duration tolerated. The audio is then trimmed of the unvoiced parts."

![](https://i.imgur.com/Gc0OpVq.png)

This function seemed to be the most complicated, but let's just break it down:
- In order for the VAD to work, we need to define a VAD window length, which could be 10, 20 or 30 milliseconds. Thus, prior to performing VAD step, we need to calculate how many audio signal samples needed for a certain VAD window length. We then need to trim the redundant part at the end of the audio to make sure the whole signal array has a length of multiple of VAD window lenght. The last step to prepare the input for the VAD is to convert it into 16-bit mono PCM format.
- The VAD step is straightforward, in which we feed the pcm wave and receive the the corresponding voiced-flag arrays.
- In order to remove the short spikes in the detection output (the very short unvoiced parts), we perform a simple moving averge (SMA) step. SMA is a technique usually used to calculate the average of a sequential data (time series, audio signal, etc.) The formula of SMA is $SMA = (p1 + p2 + ... + pn) / N$. The numerator can be achieved by using `numpy.cumsum()`. Since the output of the moving average is a floating point value, we need to binarize it again.
- Final step is to perform the binary dilation, which expands value of 1 or True of the voice flag further.
