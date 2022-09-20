import os
import cv2
import sys
import glob
import tqdm
import json
import difflib
from cnocr import CnOcr
# from aip import AipOcr

# with open('pos_dict','r',encoding='utf-8')as r:
#     pos_dict = json.loads(r.read())
h1rate = 940/1080
h2rate = 1020/1080
w1rate = 320/1920
w2rate = 1500/1920

def tailor_video(fpath, name):
    # 要提取视频的文件名，隐藏后缀
    sourceFileName = name
    # h1,h2 = pos_dict[name]
    # 在这里把后缀接上
    video_path = fpath
    times = 0
    outPutDirName = "frame_img/" + name + '/'
    # outPutDirName = './'+name
    if not os.path.exists(outPutDirName): os.makedirs(outPutDirName)
    camera = cv2.VideoCapture(video_path)
    zs = camera.get(7)
    print(int(zs))
    for _ in range(int(zs)):
        times += 1
        _, image = camera.read()
        if image is None: continue
        height, width, _ = image.shape
        h1 = int(h1rate * height)
        h2 = int(h2rate * height)
        w1 = int(w1rate * width)
        w2 = int(w2rate * width)
        millisecond = int(camera.get(0))
        image = image[h1:h2,w1:w2,:] # 裁剪下面1/4
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = 200
        _, binary = cv2.threshold(imgray, thresh, 255, cv2.THRESH_BINARY) # 输入灰度图，输出二值图
        binary = cv2.bitwise_not(binary) # 取反
        out_name = os.path.join(outPutDirName, sourceFileName+'_'+str(millisecond)+'.jpg')
        out_name = out_name.replace("/", "\\")
        # out_name = str(millisecond)+'.jpg'
        ret = cv2.imwrite(out_name, binary)  #文件目录下将输出的图片名字命名为10.jpg这种形式
        print(ret, out_name)
    print('图片提取结束')

def save(ls, lt, tt, name):
    with open(name,'a',encoding='utf-8')as a:
        a.write(str(lt)+' '+str(tt)+' '+ls+'\n')

def is_same(s1,s2):
    return difflib.SequenceMatcher(None,s1,s2).ratio()

def pic2txt(folder, name, threshold=0.8):
    pics = glob.glob(folder+'/'+name+"/*.jpg")
    pics.sort(key=lambda i: int(i.split("_")[-1].split(".")[0]))
    last_str = ""
    last_time = 0
    ocr = CnOcr()
    for pic in tqdm.tqdm(pics, ncols=50):
        res = ocr.ocr(pic)
        res.sort(key=lambda i: i[1])
        if res:
            txt, sure = res[0]
            if sure >= threshold and is_same(txt, last_str)<0.5:
                this_time = pic.split("_")[-1].split(".")[0]
                if last_str and len(last_str) > 5:
                    save(last_str, last_time, this_time, name)
                last_time = this_time
                last_str = txt
        else:
            this_time = pic.split("_")[-1].split(".")[0]
            if last_str and len(last_str) > 5:
                save(last_str, last_time, this_time, name)
            last_time = this_time
            last_str = ""

fs = glob.glob("videos/*")
fs.sort()
for f in fs:
    print(f)
    name=f.replace("\\", "/").split("/")[1][:-4]
    if os.path.exists(name): 
        print("continue...")
        continue
    tailor_video(f, name)
    pic2txt("frame_img", name)
    # print("removing...")
    # for i in tqdm(glob.glob("frame_img/*")): os.unlink(i)
