
from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        Label(frame, text="Filename:").grid(row=0)
        self.file_entry = Entry(frame).grid(row=0, column=1)

        self.is_recording = False
        self.rec_button = Button(frame,
                                 text="Start recording",
                                 fg="green",
                                 command=self._toggle_rec)
        self.rec_button.grid(row=1, column=0)

        self.img_button = Button(frame,
                                 text="Capture image",
                                 fg="blue",
                                 command=self._capture_image)
        self.img_button.grid(row=1, column=1)

        root.mainloop()

    def _toggle_rec(self):    
        if self.is_recording:
            self.rec_button.config(text="Start recording", fg="green")
            self.is_recording = False
        else:
            self.rec_button.config(text="Stop recording", fg="red")
            self.is_recording  = True
        

    def _capture_image(self):
        print "Take an image"

root = Tk()
root.geometry("640x480")

app = App(root)


