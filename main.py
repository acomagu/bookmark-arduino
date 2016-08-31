import record
import totext

if __name__ == '__main__':
    rec = record.Recorder(device=2, nChannel=1, framerate=44100, framesPerBuffer=4096)
    text = totext.main(audio, framerate=44100)
    print(text)
