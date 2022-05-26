import tkinter as tk
from tkinter import ttk
import cv2
from PIL import ImageTk, Image
import time
import numpy as np
import mediapipe as mp
from math import floor

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
        left_thigh = np.sqrt(np.square(lm.landmark[lmPose.LEFT_HIP].x)+np.square(lm.landmark[lmPose.LEFT_KNEE].x))
        right_thigh = np.sqrt(np.square(lm.landmark[lmPose.RIGHT_HIP].x)+np.square(lm.landmark[lmPose.RIGHT_KNEE].x))
        left_calf = np.sqrt(np.square(lm.landmark[lmPose.LEFT_ANKLE].x)+np.square(lm.landmark[lmPose.LEFT_KNEE].x))
        right_calf = np.sqrt(np.square(lm.landmark[lmPose.RIGHT_ANKLE].x)+np.square(lm.landmark[lmPose.RIGHT_KNEE].x))
        left_leg = np.sqrt(np.square(lm.landmark[lmPose.LEFT_ANKLE].x)+np.square(lm.landmark[lmPose.LEFT_HIP].x))
        right_leg = np.sqrt(np.square(lm.landmark[lmPose.RIGHT_ANKLE].x)+np.square(lm.landmark[lmPose.RIGHT_HIP].x))
        left_angle = np.square(left_thigh)+np.square(left_calf)-np.square(left_leg)/(2*left_thigh*left_calf)
        left_angle = left_angle - floor(left_angle)
        right_angle = np.square(right_thigh)+np.square(right_calf)-np.square(right_leg)/(2*right_thigh*right_calf)
        right_angle = right_angle - floor(right_angle)
        left = min([left_angle, 360 - left_angle])
        right = min([right_angle, 360 - right_angle])


    return (frame,"Null", left, right)

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

        def video_stream():
            _, frame = cap.read()
            #proess frame here
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for i in range(0,len(cv2image)):
                cv2image[i]=cv2image[i][::-1]
            #cv2image = cv2image[::-1]
            tup = get_pose(cv2image)
            pose_position.configure(text=tup[1]);
            img = Image.fromarray(tup[0])
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            self.hold = self.hold + 1
            if(self.hold == 100):
                doSomething()
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
        label = ttk.Label(self, text="Analysis", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)


        button1 = ttk.Button(self, text="Camera",
                             command=lambda: controller.show_frame(Camera))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(Home))

        button2.grid(row=2, column=1, padx=10, pady=10)

time.sleep(0.1)
app = tkinterApp()
app.title("FasTwitch")
app.mainloop()



