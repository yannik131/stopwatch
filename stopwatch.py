#!/bin/python3

from tkinter import *
from tkinter import _tkinter
from datetime import datetime, timedelta
import time
import os

def strfdelta(delta: timedelta):
    hours, rem = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)

    return f'{hours:02}:{minutes:02}:{seconds:02}'

class Stopwatch:
    def __init__(self):
        self.offsetFilename = 'offset.txt'
        self.reset()
        self.readOffsetFromFile()

    def writeOffsetToFile(self):
        if self.offset is None:
            return
        with open(self.offsetFilename, 'w') as file:
            file.write(str(int(self.offset.total_seconds())))

    def readOffsetFromFile(self):
        if not os.path.isfile(self.offsetFilename):
            return
        with open(self.offsetFilename) as file:
            try:
                seconds = int(file.read())
                self.offset = timedelta(seconds=seconds)
            except:
                pass

    def start(self):
        self.stamp = datetime.now()
        self.isRunning = True
        
    def stop(self):
        self.offset += datetime.now() - self.stamp
        self.writeOffsetToFile()
        self.isRunning = False

    def reset(self):
        self.offset = timedelta()
        self.stamp = None
        self.isRunning = False

    def delete(self):
        with open(self.offsetFilename, 'w') as file:
            file.write('0')
        self.offset = timedelta()
        self.stamp = datetime.now()

    def timeText(self):
        if self.stamp is None:
            return '00:00:00'
        return strfdelta(self.offset + datetime.now() - self.stamp)

class View:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('+0+0')
        self.root.title('')
        self.root.overrideredirect(True)
        self.timeTextVar = StringVar()
        self.position = 0

        self.timeLabel = Label(
            master=self.root,
            textvariable=self.timeTextVar,
            font=('Arial', 25)
        )
        self.timeLabel.pack()
        self.root.update()

        self.root.lift()
        self.root.attributes('-topmost', True)

        self.root.bind('<ButtonPress-3>', lambda x: self.root.destroy())
        self.root.bind('<ButtonPress-1>', lambda x: self.move())

    def move(self):
        screenWidth = self.root.winfo_screenwidth()
        width = self.root.winfo_width()

        positions = {
            0: '+0+0',
            1: f'+{int((screenWidth-width)/2)}+0',
            2: f'+{screenWidth-width}+0',
        }

        self.position += 1
        self.root.geometry(positions[self.position % len(positions)])


def main():
    view = View()
    stopwatch = Stopwatch()
    stopwatch.start()

    while stopwatch.isRunning:
        try:
            view.timeTextVar.set(stopwatch.timeText()) 
            view.root.update()
        except _tkinter.TclError:
	    #TODO: root.protocol('WM_DELETE_WINDOW', callback) -> callback not called?
            stopwatch.stop()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
