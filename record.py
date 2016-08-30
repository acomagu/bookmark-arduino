import pyaudio
import time
import io
import numpy
import threading

def recordSync(device, length, nChannel, framerate, framesPerBuffer):
    def callback(s):
        nonlocal audio
        audio = s
        e.set()
    audio = None
    e = threading.Event()
    record(device, length, nChannel, framerate, framesPerBuffer, callback=callback)
    e.wait()
    return audio

def record(device, length, nChannel, framerate, framesPerBuffer, callback):
    def frame(in_data, frame_count, time_info, status):
        s.write(in_data)
        return (None, pyaudio.paContinue)

    def finish_record():
        stream.stop_stream()
        stream.close()
        p.terminate()
        s.flush()
        s.seek(0)
        callback(s)

    s = io.BytesIO()
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=nChannel,
        rate=framerate,
        input_device_index=device,
        input=True,
        output=False,
        frames_per_buffer=framesPerBuffer,
        stream_callback=frame
    )

    threading.Timer(length, finish_record).start()

if __name__ == '__main__':
    s = record(2, 5)
    f = open('test.wav', 'wb')
    f.write(s.getvalue())
    f.close()
    s.close()
