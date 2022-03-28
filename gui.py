import tkinter as tk
from tkinter import ttk
import cv2
from PIL import ImageTk, Image

LARGEFONT = ("Verdana", 35)
currentframe = None

class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Home, Camera, Analysis):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Home", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Camera",
                             command=lambda: controller.show_frame(Camera))
        button1.grid(row=1, column=1, padx=10, pady=10)
        button2 = ttk.Button(self, text="Analysis",
                             command=lambda: controller.show_frame(Analysis))
        button2.grid(row=2, column=1, padx=10, pady=10)

class Camera(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Camera", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        lmain = ttk.Label(self)
        lmain.grid()

        cap = cv2.VideoCapture(0)

        def video_stream():
            _, frame = cap.read()
            #proess frame here
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream)

        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(Home))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Analysis",
                             command=lambda: controller.show_frame(Analysis))

        button2.grid(row=2, column=1, padx=10, pady=10)

        video_stream()

class Analysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Analysis", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)


        button1 = ttk.Button(self, text="Camera",
                             command=lambda: controller.show_frame(Camera))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(Home))

        button2.grid(row=2, column=1, padx=10, pady=10)

app = tkinterApp()
app.mainloop()