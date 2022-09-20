import os
import _thread

def del_file(file_list, num=1):
    n = len(file_list) // num
    l = []
    for idx, i in enumerate(file_list):
        if idx // n >= len(l): l.append([])
        l[-1].append(i)
    def del_f(li,idx):
        print(f"Thread {idx} begin.")
        for i in li: os.unlink(i)
        print(f"Thread {idx} over.")

    for idx,subl in enumerate(l):
        try:
            _thread.start_new_thread(del_f, (subl,idx+1))
        except:
            print(f"Thread {idx+1} Error.")