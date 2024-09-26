from pydub import AudioSegment
from pydub.silence import split_on_silence
from typing import Tuple

def remove_silence(audio: AudioSegment, min_silence_len=500, silence_thresh=-40, keep_silence=100) -> AudioSegment:
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    return sum(chunks)

def format_time(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"