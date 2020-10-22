# About preprocessing step

This step requires only pure Python, but with a solid amount of knowledge about DSP or audio manipulation.

This preprocessing step includes:
- `normalize_volume()` - Normalize volume to a target dBFS
- `wav_to_mel()` - Convert wav to mel-spectrogram
- `trim_long_silence()` - Eliminate silence ranges using VAD
- `preprocess_wav()` - Resample to 16kHz, and include the above steps

Below are details about each step.

### `normalize_volumes()`

### `wav_to_mel()`

### `trim_long_silence()`