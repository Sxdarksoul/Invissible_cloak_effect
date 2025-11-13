import cv2
import numpy as np
import threading
import time
import sys
import tkinter as tk
from tkinter import messagebox

# Use winsound on Windows for a clear beep; fallback to terminal bell.
try:
    import winsound
    def beep():
        winsound.Beep(1000, 450)  # frequency, duration (ms)
except Exception:
    def beep():
        sys.stdout.write('\a')
        sys.stdout.flush()

# ---------- Configuration ----------
BG_CAPTURE_FRAMES = 60
CAM_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
COLOR = "red"   # default cloak color; change to "blue" to detect blue
# -----------------------------------

def get_hsv_ranges(color):
    if color == "red":
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        return [(lower1, upper1), (lower2, upper2)]
    elif color == "blue":
        lower = np.array([94, 80, 2])
        upper = np.array([126, 255, 255])
        return [(lower, upper)]
    else:
        raise ValueError("Unsupported color")

class InvisibleCloakApp:
    def __init__(self, root):
        self.root = root
        root.title("Invisible Cloak — UX Demo")
        root.configure(bg="black")
        root.resizable(False, False)

        # Header
        self.header = tk.Label(root,
                               text="Welcome to Invisible Cloak Effect",
                               font=("Helvetica", 16, "bold"),
                               fg="white",
                               bg="black",
                               padx=20, pady=10)
        self.header.pack(fill="x")

        # Buttons frame
        self.buttons_frame = tk.Frame(root, bg="black", pady=12, padx=20)
        self.buttons_frame.pack()

        btn_style = {"width": 20, "height": 2, "font": ("Helvetica", 12, "bold"),
                     "bd": 0, "highlightthickness": 0}

        self.start_btn = tk.Button(self.buttons_frame, text="Start", command=self.start,
                                   bg="white", fg="black", **btn_style)
        self.start_btn.grid(row=0, column=0, padx=10, pady=8)

        self.stop_btn = tk.Button(self.buttons_frame, text="Stop", command=self.stop,
                                  bg="white", fg="black", state="disabled", **btn_style)
        self.stop_btn.grid(row=0, column=1, padx=10, pady=8)

        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = tk.Label(root, textvariable=self.status_var,
                                     font=("Helvetica", 10), fg="white", bg="black", pady=8)
        self.status_label.pack(fill="x")

        # Thread control
        self.thread = None
        self.stop_event = threading.Event()

    def set_status(self, text):
        self.status_var.set(text)

    def start(self):
        # Disable start, enable stop
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.set_status("Starting... Preparing camera.")
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_invisibility, daemon=True)
        self.thread.start()

    def stop(self):
        # Signal the thread to stop
        self.set_status("Stopping...")
        self.stop_event.set()
        self.stop_btn.config(state="disabled")
        # Wait for thread to clean up
        if self.thread is not None:
            self.thread.join(timeout=3.0)
        self.start_btn.config(state="normal")
        self.set_status("Stopped. Ready")

    def _run_invisibility(self):
        hsv_ranges = get_hsv_ranges(COLOR)

        cap = cv2.VideoCapture(CAM_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        if not cap.isOpened():
            self._show_error("Cannot open camera. Check camera index or permissions.")
            self._reset_buttons()
            return

        # Capture background frames
        self.set_status("Capturing background frames. Please step out of the frame or keep cloak out.")
        bg_frames = []
        captured = 0
        while captured < BG_CAPTURE_FRAMES and not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            bg_frames.append(frame)
            captured += 1
            if captured % 10 == 0:
                self.set_status(f"Captured {captured}/{BG_CAPTURE_FRAMES} background frames")
        if self.stop_event.is_set():
            cap.release()
            self._reset_buttons()
            return

        background = np.median(np.array(bg_frames), axis=0).astype(np.uint8)
        self.set_status("Background ready. Starting invisibility effect.")
        beep()  # notify user that background capture is complete

        kernel = np.ones((3,3), np.uint8)

        # Main loop: show only final composed window
        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                self.set_status("Failed to read frame from camera.")
                break
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # create mask
            mask = None
            for (lower, upper) in hsv_ranges:
                m = cv2.inRange(hsv, lower, upper)
                if mask is None:
                    mask = m
                else:
                    mask = cv2.bitwise_or(mask, m)

            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
            mask = cv2.dilate(mask, kernel, iterations=1)
            mask_inv = cv2.bitwise_not(mask)

            part_bg = cv2.bitwise_and(background, background, mask=mask)
            part_fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
            final = cv2.addWeighted(part_bg, 1, part_fg, 1, 0)

            # Show only the final output (single window)
            cv2.imshow("Invisible Cloak Output", final)

            # Wait key with a short delay so GUI remains responsive
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # If user presses q in the OpenCV window, treat as stop
                self.stop_event.set()
                break

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self._reset_buttons()

    def _reset_buttons(self):
        # Called after stopping/ending thread to reset UI state
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.set_status("Ready")

    def _show_error(self, message):
        # Show message box on the main thread
        try:
            messagebox.showerror("Error", message)
        except Exception:
            print("ERROR:", message)

def main():
    root = tk.Tk()
    app = InvisibleCloakApp(root)
    # Center the window on screen (optional)
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    root.geometry(f"+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    main()
