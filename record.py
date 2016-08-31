import pyaudio
import time
import io
import numpy
import threading

class Recorder:
    def __init__(self, device, nChannel, framerate, nFramePerBuffer):
        self.s = io.BytesIO()
        self.p = pyaudio.PyAudio()
        self.device = device
        self.nChannel = nChannel
        self.framerate = framerate
        self.nFramePerBuffer = nFramePerBuffer

    def start(self):
        def _frame(in_data, frame_count, time_info, status):
            self.s.write(in_data)
            return (None, pyaudio.paContinue)

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.nChannel,
            rate=self.framerate,
            input_device_index=self.device,
            input=True,
            output=False,
            frames_per_buffer=self.nFramePerBuffer,
            stream_callback=_frame
        )

    def end(self):
        self.stream.stop_stream()

    def close(self):
        self.stream.close()
        self.p.terminate()
        self.s.flush()
        self.s.seek(0)
        return self.s
