import os
import cv2
import glob
import json

h1 = h2 = None
w1 = w2 = None

fs = glob.glob("videos/*.mp4")
for i in fs:
    vi = cv2.VideoCapture(i)
    name = i.replace("\\", "/").split("/")[1][:-4]
    name = name.replace("第", "di").replace("期", "qi").replace("季", "ji")
    if os.path.exists(name+".jpg"): 
        print('continue...', name)
        continue
    # 找到有字幕的一帧
    while True:
        for i in range(2000): res, img = vi.read()
        ret = cv2.imwrite(name+'.jpg', img)
        print(f"输出图片{name}.jpg {ret}，请检查")
        ans = input()
        if ans.lower() == 'ok': break
    while True:
        print(f"shape:{img.shape}")
        h1 = int(input("H1:\n") or 0) or h1
        h2 = int(input("H2:\n") or 0) or h2
        w1 = int(input("w1:") or 0) or w1
        w2 = int(input("w2:") or 0) or w2
        if not w1: w1 = 0
        if not w2: w2 = img.shape[1]
        if not h2: h2 = img.shape[0]
        else: h2 = int(h2)
        img2 = img[h1:h2,w1:w2,:]
        cv2.imwrite(name+'.jpg',img2)
        print(f"输出裁剪后图片{name}.jpg，请检查")
        print(f"裁剪位置为[{h1}:{h2},{w1}:{w2},:]")
        ans = input()
        if ans.lower() == 'ok': break
    if not os.path.exists('pos_dict'): other_pos = dict()
    else: 
        with open("pos_dict",'r',encoding='utf-8')as r: other_pos = json.loads(r.read())
    other_pos[name] = [h1,h2]
    with open("pos_dict",'w',encoding='utf-8')as w:
        w.write(json.dumps(other_pos))