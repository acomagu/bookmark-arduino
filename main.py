import record
import totext

if __name__ == '__main__':
    audio = record.recordSync(device=2, length=4, nChannel=1, framerate=44100, framesPerBuffer=4096)
    text = totext.main(audio, framerate=44100)
    print(text)
