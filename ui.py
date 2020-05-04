#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Code to make a GUI to run the RiceBraille project using wxPython.

We based this off sample code by Jan Bodnar's ZetCode wxPython tutorial.
sample code author: Jan Bodnar
website: www.zetcode.com
last modified: April 2018
"""

import wx
from tkinter import filedialog as fd
from VideoTracker import VideoTracker



class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.auto_page = 0
        self.show_frames = 0
        self.page_length = 0
        self.page_width = 0
        self.InitUI()
        self.Centre()

    def InitUI(self):

        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Page Length (cm)')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        self.page_length = wx.TextCtrl(panel, value="27.94")
        hbox1.Add(self.page_length, proportion=1)
        vbox.Add(hbox1, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Page Width (cm)')
        st2.SetFont(font)
        hbox2.Add(st2, flag=wx.RIGHT, border=8)
        self.page_width = wx.TextCtrl(panel, value="29.21")
        hbox2.Add(self.page_width, proportion=1)
        vbox.Add(hbox2, border=10)


        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.auto_page = wx.CheckBox(panel, label='Automatic Page Calibration')
        self.auto_page.SetFont(font)
        hbox4.Add(self.auto_page)
        self.show_frames = wx.CheckBox(panel, label='Show Frames')
        self.show_frames.SetFont(font)
        hbox4.Add(self.show_frames, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Start', size=(70, 30))
        hbox5.Add(btn1)
        self.Bind(wx.EVT_BUTTON, self.StartProcessing, btn1)

        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.OnQuit, btn2)

        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)

    def OnQuit(self, e):
        self.Close()

    def StartProcessing(self, e):
        name = fd.askopenfilenames()
        print(name)
        VideoTracker(name[0], auto_calibrate=False, auto_page_calibrate=self.auto_page.IsChecked(),
                     show_frame=self.show_frames.IsChecked(), paper_dims=(float(self.page_length.GetValue()), float(self.page_width.GetValue())))
        self.close()


def main():

    app = wx.App()
    ex = Example(None, title='Finger Tracking')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

'''
import tkinter as tk
from tkinter import filedialog as fd
from VideoTracker import VideoTracker

def show_entry_fields():
    print("First Field: %s\nLast Field: %s" % (e1.get(), e2.get()))


def start_processing():
    name = fd.askopenfilenames()
    print(name)
    VideoTracker(name[0], auto_calibrate=False, auto_page_calibrate=auto_page_calibration.get(), show_frame=show_frames.get(), paper_dims=(float(e1.get()), float(e2.get())))


master = tk.Tk()
tk.Label(master,
         text="Page Length(cm)").grid(row=0)
tk.Label(master,
         text="Page Width(cm)").grid(row=1)

e1 = tk.Entry(master)
e1.insert(tk.END, '27.94')
e2 = tk.Entry(master)
e2.insert(tk.END, '29.21')

show_frames = tk.BooleanVar()
auto_page_calibration = tk.BooleanVar()
tk.Checkbutton(master, text="Show frames", variable=show_frames).grid(row=3, sticky=tk.W)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
tk.Checkbutton(master, text="Automatic Page Calibration", variable=auto_page_calibration).grid(row=4, sticky=tk.W)

tk.Button(master,
          text='Quit',
          command=master.quit).grid(row=5,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(master,
          text='Start', command=start_processing).grid(row=5,
                                                            column=1,
                                                            sticky=tk.W,
                                                            pady=4)
errmsg = 'Error!'
tk.mainloop()
'''