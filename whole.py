import threading
import pygame
import cv2 as cv
import numpy as np
import tkinter
import os
import time

import main
from PIL import Image, ImageTk

root = tkinter.Tk()
root.title('智能音乐播放器')
root.geometry('800x800+0+0')
root.resizable(False, False)

ret = []
res = []
num = 0
voice = 0.2
playing = False
pause = False
now_music = ''
folder = './' + 'music'
musics = [folder + '\\' + music for music in os.listdir(folder) if music.endswith(('.mp3', '.wav', '.ogg'))]

canvas = tkinter.Canvas(root, bg='#c4c2c2', height=480, width=640)
canvas.pack()

labelName = tkinter.Label(root, text='音乐列表', anchor='w')
labelName.place(x=80, y=495, width=50, height=15)

for i in musics:
    ret.append(i.split('\\')[1:])
    res.append(i.replace('\\', '/'))
    var2 = tkinter.StringVar()
    var2.set(ret)
    lb = tkinter.Listbox(root, listvariable=var2)
    lb.place(x=80, y=520, width=260, height=130)

musicName = tkinter.StringVar(root, value='暂时没有播放音乐...')
labelName = tkinter.Label(root, textvariable=musicName)
labelName.place(x=130, y=495, width=400, height=15)

labelName0 = tkinter.Label(root, text='   手势0： 暂停     手势1： 继续/播放')
labelName0.place(x=360, y=520, width=200, height=25)

labelName1 = tkinter.Label(root, text='   手势2： 下一首     手势3： 上一首')
labelName1.place(x=360, y=570, width=200, height=25)

labelName2 = tkinter.Label(root, text='  手势4： 音量 +     手势5： 音量 -')
labelName2.place(x=360, y=620, width=200, height=25)


def play():
    global res
    global musicName
    if len(res):
        pygame.mixer.init()
        global num
        while playing:
            if not pygame.mixer.music.get_busy():
                nextMusic = res[num]
                print(nextMusic.split('/')[2:])
                pygame.mixer.music.load(nextMusic.encode())
                # pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(1)
                if len(res) - 1 == num:
                    num = 0
                else:
                    num = num + 1
                nextMusic = nextMusic.split('/')[2:]
                musicName.set('playing....' + str(nextMusic))
            else:
                time.sleep(0.1)


def PlayBegin():
    global playing
    if playing == False:
        playing = True
        t = threading.Thread(target=play)
        t.start()

'''
def plauPlay():
    global playing
    global pause
    if (playing == True) and (pause ==False):
        playing = False
        pause = True
        pygame.mixer.music.pause()


def continuePlay():
    global pause
    global playing
    if (pause == True) and (playing == False):
        pygame.mixer.music.unpause()
'''

def NextPlay():
    global playing
    playing = False
    pygame.mixer.music.stop()
    global num
    if len(res) == num:
        num = 0
    playing = True
    t = threading.Thread(target=play)
    t.start()


def PrevPlay():
    global playing
    playing = False
    pygame.mixer.music.stop()
    global num
    if num == 0:
        num = len(res) - 2
    elif num == len(res) - 1:
        num -= 2
    else:
        num -= 2
    playing = True
    t = threading.Thread(target=play)
    t.start()


def control_voice_add():
    global voice
    voice += 0.4
    if voice > 1:
       voice = 1
       print('音量已调至最大')
    pygame.mixer.music.set_volume(float(voice))


def control_voice_reduce():
    global voice
    voice -= 0.4
    if voice < 0:
        voice = 0
        print('音量已调至最小')
    pygame.mixer.music.set_volume(float(voice))


def do_none():
    pass


def video_demo():
    global pause
    c = 1
    timeF = 60
    camera = cv.VideoCapture(0)
    while camera.isOpened():
        ret, frame = camera.read()
        frame = cv.flip(frame, 1)
        cv.rectangle(frame, (400, 60), (640, 300), (200, 100, 0))
        cov = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        img = Image.fromarray(cov)
        img_file = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor='nw', image=img_file)

        img = frame[60:300, 400:640]
        if c % timeF == 0:
            hand_num = main.recognise(img, True)

            if hand_num == 0:
                print('暂停')
                pygame.mixer.music.pause()
                pause = True

            elif hand_num == 1:
                if pause == True:
                    print('继续')
                    pygame.mixer.music.unpause()
                else:
                    print('播放')
                    PlayBegin()

            elif hand_num == 2:
                print('下一首')
                NextPlay()

            elif hand_num == 3:
                print('上一首')
                PrevPlay()

            elif hand_num == 4:
                print('加大音量')
                control_voice_add()

            elif hand_num == 5:
                print('减小音量')
                control_voice_reduce()

            else:
                do_none()
        c = c+1
        root.update_idletasks()
        root.update()


bt_start = tkinter.Button(root, text='打开摄像头', height=2, width=15, command=video_demo)
bt_start.place(x=600, y=580)

play_begin = tkinter.Button(root, text='点击开始播放', height=2, width=15, command=PlayBegin)
play_begin.place(x=600, y=520)

root.mainloop()
