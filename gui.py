import random
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import ImageTk, Image
import time
import numpy as np
import mediapipe as mp
from math import floor
import threading
from playsound import playsound
from matplotlib import pyplot as plt
plt.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5)
def get_pose(frame):
    global mp_pose
    global pose
    #RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    RGB=frame
    results = pose.process(RGB)
    lm = results.pose_landmarks
    lmPose = mp_pose.PoseLandmark
    mp_drawing.draw_landmarks(frame,lm, mp_pose.POSE_CONNECTIONS)
    if lm is not None:
        left_thigh = np.sqrt(np.square(lm.landmark[lmPose.LEFT_HIP].x-lm.landmark[lmPose.LEFT_KNEE].x)+
                             np.square(lm.landmark[lmPose.LEFT_HIP].y-lm.landmark[lmPose.LEFT_KNEE].y))
        right_thigh = np.sqrt(np.square(lm.landmark[lmPose.RIGHT_HIP].x - lm.landmark[lmPose.RIGHT_KNEE].x) +
                             np.square(lm.landmark[lmPose.RIGHT_HIP].y - lm.landmark[lmPose.RIGHT_KNEE].y))
        left_calf = np.sqrt(np.square(lm.landmark[lmPose.LEFT_ANKLE].x - lm.landmark[lmPose.LEFT_KNEE].x) +
                             np.square(lm.landmark[lmPose.LEFT_ANKLE].y - lm.landmark[lmPose.LEFT_KNEE].y))
        right_calf = np.sqrt(np.square(lm.landmark[lmPose.RIGHT_ANKLE].x - lm.landmark[lmPose.RIGHT_KNEE].x) +
                             np.square(lm.landmark[lmPose.RIGHT_ANKLE].y - lm.landmark[lmPose.RIGHT_KNEE].y))
        left_leg = np.sqrt(np.square(lm.landmark[lmPose.LEFT_ANKLE].x - lm.landmark[lmPose.LEFT_HIP].x) +
                             np.square(lm.landmark[lmPose.LEFT_ANKLE].y - lm.landmark[lmPose.LEFT_HIP].y))
        right_leg = np.sqrt(np.square(lm.landmark[lmPose.RIGHT_ANKLE].x - lm.landmark[lmPose.RIGHT_HIP].x) +
                             np.square(lm.landmark[lmPose.RIGHT_ANKLE].y - lm.landmark[lmPose.RIGHT_HIP].y))
        left_angle = np.arccos((np.square(left_thigh)+np.square(left_calf)-np.square(left_leg))/(2*left_thigh*left_calf))
        right_angle = np.arccos((np.square(right_thigh)+np.square(right_calf)-np.square(right_leg))/(2*right_thigh*right_calf))
        left = min([left_angle, 2 * np.pi - left_angle])
        right = min([right_angle, 2 * np.pi - right_angle])
        # print(left, right)
        return (frame, "Null", left, right)
    return None

LARGEFONT = ("Verdana", 35)

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

    def get_page(self, page_class):
        return self.frames[page_class]


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
        pose_position = ttk.Label(self, text="Callibrating...", font=LARGEFONT)
        pose_position.grid(row=0, column=0, padx=10, pady=10)
        lmain = ttk.Label(self)
        lmain.grid()
        cap = cv2.VideoCapture(0)
        self.hold = 0
        self.fps =  cap.get(cv2.CAP_PROP_FPS)
        self.thread = threading.Thread()
        self.angles = []
        self.delay = 0
        self.controller = controller
        def ready(delay):
            playsound()
            self.thread.join()
        def video_stream():
            _, frame = cap.read()
            #proess frame here
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for i in range(0,len(cv2image)):
                cv2image[i]=cv2image[i][::-1]
            #cv2image = cv2image[::-1]
            tup = get_pose(cv2image)
            if tup is not None:
                pose_position.configure(text=tup[1]);
                img = Image.fromarray(tup[0])
                imgtk = ImageTk.PhotoImage(image=img)
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
                if tup[2]<100 or tup[3]<100 and self.hold >= 0:
                    self.hold = self.hold + 1
                if self.hold == 1.3*self.fps:
                    self.delay = random.uniform(0,1)
                    self.thread.start(ready(self.delay))
                    self.hold == -1
                if self.hold < 0:
                    self.angles.append(max(tup[2],tup[3])/2)
                    self.hold = self.hold - 1
                if self.hold == -5*self.fps:
                    self.hold = 0
                    self.controller.get_page('Analysis').set_angles(self.angles)

            lmain.after(12, video_stream)

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
        self.angles = []
        label = ttk.Label(self, text="Analysis", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        # prepare data
        data = {
            'Python': 11.27,
            'C': 11.16,
            'Java': 10.46,
            'C++': 7.5,
            'C#': 5.26
        }
        languages = data.keys()
        popularity = data.values()
        figure = Figure(figsize=(6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        NavigationToolbar2Tk(figure_canvas, self)
        plot = figure.add_subplot()
        plot.plot(self.angles)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        button1 = ttk.Button(self, text="Camera",
                             command=lambda: controller.show_frame(Camera))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(Home))

        button2.grid(row=2, column=1, padx=10, pady=10)


    def get_angles(self, angles):
        self.angles = angles

time.sleep(0.1)
app = tkinterApp()
app.title("FasTwitch")
app.mainloop()



