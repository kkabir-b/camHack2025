import numpy as np
import librosa
import pyperclip
# from AudioSeparate import AudioSeparation


def extract_fft_tones_librosa(y, sr, start_time=0, duration=0.1, num_tones=10, amp_threshold=0.05):
    """
    Perform FFT on a short audio interval and return frequency and amplitude lists,
    keeping constant number of tones and setting amplitudes below threshold to 0.
    """
    start_sample = int(start_time * sr)
    end_sample = int((start_time + duration) * sr)
    segment = y[start_sample:end_sample]

    if len(segment) == 0:
        return [0.0]*num_tones, [0.0]*num_tones

    # Apply Hanning window
    segment *= np.hanning(len(segment))

    # FFT
    fft_vals = np.fft.rfft(segment)
    amps = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(segment), d=1/sr)

    # Normalize safely
    max_amp = np.max(amps)
    if max_amp != 0:
        amps /= max_amp

    # Get top N peaks
    indices = np.argsort(amps)[-num_tones:][::-1]

    # Build frequency and amplitude lists
    freqs_list = [round(freqs[i], 2) for i in indices]
    amps_list = [float(amps[i]) if amps[i] >= amp_threshold else 0.0 for i in indices]

    # Ensure constant length
    while len(freqs_list) < num_tones:
        freqs_list.append(0.0)
        amps_list.append(0.0)

    return freqs_list, amps_list


def analyze_whole_audio_librosa(mp3_path, interval=0.1, num_tones=10, amp_threshold=0.05):
    """
    Analyze entire audio file and return transposed frequency & amplitude tracks
    with constant dimensions for all segments.
    """
    y, sr = librosa.load(mp3_path, sr=None, mono=True)
    duration = min(len(y) / sr , 10.0)

    freqs_all = []
    amps_all = []

    t = 0.0
    while t < duration:
        freqs, amps = extract_fft_tones_librosa(
            y, sr, start_time=t, duration=interval, num_tones=num_tones, amp_threshold=amp_threshold
        )
        freqs_all.append(freqs)
        amps_all.append(amps)
        t += interval
        print(f"Processed {min(t, duration):.2f}s / {duration:.2f}s")

    # Convert to NumPy and transpose: shape [num_tones, num_segments]
    freqs_T = np.array(freqs_all, dtype=float).T.tolist()
    amps_T = np.array(amps_all, dtype=float).T.tolist()

    return freqs_T, amps_T
#gen_copy_and_pate returns the string containing all the latex tones w the right stuff at time t
def gen_copy_paste(path,interval_length,num_tones,name): #name = vocals,drum,bass,other
    vol = f'v_'+'{' + name + '}'
    pitch = f'p_'+'{' + name + '}'
    
    freq,amp = analyze_whole_audio_librosa(path,interval=interval_length,num_tones=num_tones)
    n_amp = [[str(i) + r' \cdot ' + vol for i in j] for j in amp]
    n_freq = [[str(i) for i in j] for j in freq]
 
    print('The number of indices:',len(n_amp[0]))
    tot = []
    for i,j in zip(n_freq,n_amp):
        fr = ", ".join(i)
        am = ", ".join(j)
        tot.append(r'\operatorname{tone}\left(\left[' + str(fr) + r'\right][t],\left[' + str(am) + r'\right][t]\right)')
    return tot
# tot = gen_copy_paste(r'.\examples\example_audios\idol.mp3',0.025,400,'vocals')
# #print(tot)
# pyperclip.copy(str(tot))