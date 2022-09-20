from pydub import AudioSegment
from pydub.playback import play


with open("aaaa.txt", 'r', encoding='utf-8')as r:
    data=r.readlines()

sound = AudioSegment.from_wav("aaa.wav")

for line in data:
    st,et,txt = line.strip().split(' ', 2)
    st = int(st)
    et = int(et)
    print(st,et)
    print(txt)
    subs = sound[st:et]
    play(subs)
    input()