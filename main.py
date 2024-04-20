from tkinter import *
from pygame import mixer
from tkinter import filedialog
import threading
import os
from mutagen.mp3 import MP3
import time

#defining the main window of application
root = Tk()
mixer.init()
root.geometry("680x450")
root.config(background = "black")
root.title("RRmusic")

#bottom frame
statusbar = Label(root, text = "# Submitted by:\n2K20/CO/358 Reuben Mark Elias\n2K20/CO/354 Rajat Singh\nSubmitted to:\nMr. Nipun Bansal",  fg = "white",  background = "black")
statusbar.pack(side = BOTTOM, fill = X)

#default file to be played if no file is selected
filename = "/Users/anil/Desktop/ Way Out Of Here.mp3"

#function to exit the application
def exitroot():
    global ex
    mixer.music.stop()
    root.destroy()

#function to browse a file stored in storage
def browsefile():
    global filename
    filename = filedialog.askopenfilename()

#top frame
menubar = Menu(root)
root.config(menu = menubar)

submenu = Menu(menubar)
menubar.add_cascade(label = "File", menu = submenu)
submenu.add_command(label = "Open", command = browsefile)
submenu.add_command(label = "Exit", command = exitroot)

welcome_txt = Label(root, text = 'Progressive Rock', font = 'Ariel 16', background = "black", fg = "white")
welcome_txt.pack()

#right frame
right = Frame(root)
right.config(background = "black")#right frame
right.pack(side = RIGHT, padx = 10)

#left frame
left = Frame(root)
left.config(background = "black")#left frame
left.pack(side = LEFT, padx = 10)

music_img = PhotoImage(file = "projectImages/music.png")
music_btn = Button(left, image = music_img)
music_btn.grid(row = 0, column = 0, padx = 5)

top = Frame(right)
top.pack(side = TOP)

#function to show total time of media being played
def total(song_time):
    timing = MP3(song_time).info.length
    # print(timing)
    mints, scnds = divmod(timing, 60)
    mints = round(mints)
    scnds = round(scnds)
    if scnds == 60:
        mints += 1
        scnds = 0
    total_len['text'] = "total length : {:02}:{:02}".format(mints, scnds)
    thread = threading.Thread(target=current, args = (timing, ))
    thread.start()

#function to show realtime timing status of media being played
def current(clength):
    global rew
    t = clength
    while clength and mixer.music.get_busy():
        if paused:
            continue
        elif rew == True:
            rew = False
            break
        else:
            mints, scnds = divmod(clength, 60)
            mints = round(mints)
            scnds = round(scnds)
            if scnds == 60:
                mints += 1
                scnds = 0
            current_len['text'] = "current length : {:02}:{:02}".format(mints, scnds)
            time.sleep(1)
            clength -= 1
    if mixer.music.get_busy() == False:
        mints, scnds = divmod(t, 60)
        mints = round(mints)
        scnds = round(scnds)
        if scnds == 60:
            mints += 1
            scnds = 0
        current_len['text'] = "current length : {:02}:{:02}".format(mints, scnds)

#default timings when no media is selected
total_len = Label(top, text = "  total length : --:--  ", background = "black", fg = "white")
total_len.pack()

current_len = Label(top, text = "current length : --:--", background = "black", fg = "white")
current_len.pack()

#middle frame
middle = Frame(right) #middle frame
middle.config(background = "black")
middle.pack()

#function to play the audio file
def playfunc():
    global paused
    global filename
    if paused:
        mixer.music.unpause()
        paused = False
        statusbar['text'] = "playing" + ":" + os.path.basename(filename)
    else:
        mixer.music.load(filename)
        mixer.music.play()
        total(filename)
        statusbar['text'] = "playing" + ":" + os.path.basename(filename)

paused = False
#function to pause the audio file
def pausefunc():
    global paused
    mixer.music.pause()
    paused = True
    statusbar['text'] = "music paused"

#function to stop the audio file
def stopfunc():
    global paused
    mixer.music.stop()
    paused = False
    statusbar['text'] = "music stopped"

rew = False
#function to rewind the audio file
def rewindfunc():

    global rew
    playfunc()
    rew = True

#function to control the volume using scale of the audio file
def volume(value):
    vol = float(value)/100
    mixer.music.set_volume(vol)

muted = False
#function to mute the audio file
def mutefunc():
    global muted
    if muted:
        mute_btn.config(image = mute_img)
        mixer.music.set_volume(0.5)
        vol_scale.set(50)
        muted = False
    else:
        mute_btn.config(image = unmute_img)
        mixer.music.set_volume(0)
        vol_scale.set(0)
        muted = True

#play button
play_img = PhotoImage(file = "projectImages/play.png")
play_btn = Button(middle, image = play_img, command = playfunc)
play_btn.grid(row = 0, column = 0, padx = 5)

#pause button
pause_img = PhotoImage(file = "projectImages/pause.png")
pause_btn = Button(middle, image = pause_img, command = pausefunc)
pause_btn.grid(row = 0, column = 1, pady =5)

#stop button
stop_img = PhotoImage(file = "projectImages/stop.png")
stop_btn = Button(middle, image = stop_img, command = stopfunc)
stop_btn.grid(row = 0, column = 2, padx = 5, pady =5)


bottom = Frame(right)
bottom.config(background = "black")
bottom.pack(side = BOTTOM)  #bottom frame

#mute and unmute button
mute_img = PhotoImage(file = "projectImages/mute.png")
mute_btn = Button(bottom, image = mute_img, command = mutefunc)
mute_btn.grid(row = 0, column = 0,padx = 5, pady =5)

#rewind button
rewind_img = PhotoImage(file = "projectImages/replay.png")
rewind_btn = Button(bottom, image = rewind_img, command = rewindfunc)
rewind_btn.grid(row = 0, column = 1,padx = 5, pady = 5)

unmute_img = PhotoImage(file = "projectImages/volume.png")

vol_scale = Scale(bottom, from_ = 0, to = 100, orient = HORIZONTAL, background = "black", fg = "white", command = volume)
vol_scale.grid(row = 0, column = 2, padx = 10)
vol_scale.set(50)


root.mainloop()
