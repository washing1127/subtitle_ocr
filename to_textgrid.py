import textgrid
import glob
import sys
import os

def check_merge(l):
    ret = [l[0]]
    for st,et,txt in l[1:]:
        if st <= ret[-1][1]:
            ret[-1][1] = et
            ret[-1][2] += txt
        else:
            ret.append([st,et,txt])
    for i in range(1,len(ret)):
        s1,e1,t1 = ret[i-1]
        s2,e2,t2 = ret[i]
        if e1 + 1000 <= s2:
            ret[i-1][1] = e1+500
            ret[i][0] = s2-500
    return ret

fs = [i for i in os.listdir(".") if '-' in i]

for f in fs:
    with open(f,'r',encoding='utf-8')as r: l = [i.strip().split(' ',2) for i in r.readlines()]
    for i in l:
        i[0] = int(i[0])
        i[1] = int(i[1])
    l = check_merge(l)
    for i in l:
        i[0] = int(i[0]) / 1000
        i[1] = int(i[1]) / 1000
    tg = textgrid.TextGrid(minTime=0, maxTime=l[-1][1])
    text_tier = textgrid.IntervalTier(name='text', minTime=0, maxTime=l[-1][1])
    spk_tier = textgrid.IntervalTier(name='spk', minTime=0, maxTime=l[-1][1])
    gdr_tier = textgrid.IntervalTier(name='spk2gender', minTime=0, maxTime=l[-1][1])
    for st, et, txt in l:
        interval1 = textgrid.Interval(minTime=st, maxTime=et, mark=txt)
        text_tier.addInterval(interval1)
        interval2 = textgrid.Interval(minTime=st, maxTime=et, mark='')
        spk_tier.addInterval(interval2)
    interval3 = textgrid.Interval(minTime=0, maxTime=l[-1][1], mark='')
    gdr_tier.addInterval(interval3)
    tg.tiers.append(text_tier)
    tg.tiers.append(spk_tier)
    tg.tiers.append(gdr_tier)

    tg.write(f+'.TextGrid')