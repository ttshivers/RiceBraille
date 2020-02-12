import tkinter as tk
from tkinter import filedialog as fd
from VideoTracker import VideoTracker

def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))


def start_processing():
    tracker = VideoTracker("./test_images/full_page2.MOV", auto_calibrate=False, show_frame=True)


def callback():
    name = fd.askopenfilenames()
    print(name)


master = tk.Tk()
tk.Label(master,
         text="Page Length(cm)").grid(row=0)
tk.Label(master,
         text="Page Width(cm)").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master,
          text='Manual',
          command=master.quit).grid(row=3,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(master,
          text='Automatic', command=show_entry_fields).grid(row=3,
                                                            column=1,
                                                            sticky=tk.W,
                                                            pady=4)
errmsg = 'Error!'
tk.Button(text='File Open',
          command=callback).grid(row=3,
                                 column=2,
                                 sticky=tk.W,
                                 pady=4)

tk.mainloop()