import tkinter as tk
from tkinter import filedialog as fd
from VideoTracker import VideoTracker

def show_entry_fields():
    print("First Field: %s\nLast Field: %s" % (e1.get(), e2.get()))


def start_processing():
    name = fd.askopenfilenames()
    print(name)
    VideoTracker(name[0], auto_calibrate=False, show_frame=show_frames.get(), paper_dims=(float(e1.get()), float(e2.get())))


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
tk.Checkbutton(master, text="Show frames", variable=show_frames).grid(row=3, sticky=tk.W)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master,
          text='Quit',
          command=master.quit).grid(row=4,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(master,
          text='Start', command=start_processing).grid(row=4,
                                                            column=1,
                                                            sticky=tk.W,
                                                            pady=4)
errmsg = 'Error!'
tk.mainloop()