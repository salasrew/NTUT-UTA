import cv2
import tkinter as tk
import time
from PIL import ImageTk, Image


class VideoCaptureApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.cap = cv2.VideoCapture(0)

        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack(anchor=tk.CENTER, pady=10)

        self.btn_record = tk.Button(self.btn_frame, text="開始錄影", command=self.toggle_record)
        self.btn_record.grid(row=0, column=0, padx=5)

        self.btn_capture = tk.Button(self.btn_frame, text="拍照", command=self.capture)
        self.btn_capture.grid(row=0, column=1, padx=5)

        self.lb_video = tk.Label(window)
        self.lb_video.pack(anchor=tk.CENTER, expand=True)

        self.info_frame = tk.Frame(window)
        self.info_frame.pack(anchor=tk.N, padx=10, pady=10)

        self.lb_count = tk.Label(self.info_frame, text="拍照數量: 0", font=("Arial", 15))
        self.lb_count.grid(row=0, column=0, padx=10)

        self.lb_time = tk.Label(self.info_frame, text="00:00", font=("Arial", 15))
        self.lb_time.grid(row=0, column=1, padx=10)


        self.delay = 10
        self.is_recording = False
        self.start_time = 0
        self.capture_count = 0
        self.update()

        self.window.mainloop()

    def toggle_record(self):
        if self.is_recording:
            self.is_recording = False
            self.btn_record.config(text="開始錄影")
            self.out.release()
        else:
            self.is_recording = True
            self.btn_record.config(text="停止錄影")
            self.start_time = time.time()
            self.capture_count += 1
            current_time = time.strftime("%m%d%H%M%S", time.localtime())
            filename = f"video{self.capture_count}_{current_time}.avi"
            self.out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 20.0, (640, 480))

    def capture(self):
        ret, frame = self.cap.read()
        if ret:
            filename = f"capture{self.capture_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"已拍照：{filename}")
            self.capture_count += 1
            self.lb_count.config(text=f"拍照數量: {self.capture_count}")

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.image = ImageTk.PhotoImage(Image.fromarray(self.frame))
            self.lb_video.configure(image=self.image)

        if self.is_recording:
            self.out.write(frame)
            elapsed_time = time.time() - self.start_time
            self.lb_time.config(text=self.format_time(elapsed_time))

        self.window.after(self.delay, self.update)

    def format_time(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        return time_str


# Create window
window = tk.Tk()

# Create application
app = VideoCaptureApp(window, "視訊捕捉")

# Release the camera resources
app.cap.release()

# Close the window
window.destroy()
