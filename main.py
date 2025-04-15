import tkinter as tk
import pydirectinput as pdi
import time
import threading
from tkinter import messagebox as mb, simpledialog as sd
import pygetwindow as gw
import keyboard as kb

def req_clicks():
    mb.showinfo("Instructions", "You will now define 6 points on the screen")
    coords.clear()
    for i in range(6):
        mb.showinfo("Point Selection", f"Hover over point {i + 1} and press 'OK' to record")
        x, y = pdi.position()
        coords.append((x, y))
    mb.showinfo(" complete", "all 6 points have been recorded")

def jitter_m(x, y):
    for i in range(3):  # 3 jitters
        pdi.moveTo(x + 2, y + 2)
        time.sleep(0.01)
        pdi.moveTo(x - 2, y - 2)
        time.sleep(0.01)

def perf_actions(num_wins):
    rb_windows = [win for win in gw.getWindowsWithTitle('Roblox')]

    if len(rb_windows) < num_wins:
        mb.showerror("Error", "Not enough Roblox windows detected")
        return

    for w_idx, rb_win in enumerate(rb_windows[:num_wins]):
        rb_win.activate()
        time.sleep(1)  
       
        for x, y in coords:
            jitter_m(x, y)
            pdi.click(x=x, y=y, clicks=1)
            time.sleep(0.5)
            pdi.click(x=x, y=y, clicks=1)

def ml_actions():
    if len(coords) != 6:
        mb.showerror("Error", "record all 6 points")
        return

    try:
        num_wins = int(sd.askstring("Input", "number of Roblox windows to cycle:"))
        if num_wins <= 0:
            mb.showerror("Error", "enter a valid number of windows")
            return
    except (ValueError, TypeError):
        mb.showerror("Error", "invalid input for the number windows")
        return

    global stop_l
    stop_l = False

    def stop_key():
        global stop_l
        kb.wait('q')  # Wait for 'q' key to end
        stop_l = True

    threading.Thread(target=stop_key, daemon=True).start()
   
    if run_inf.get():
        while not stop_l:
            perf_actions(num_wins)
    else:
        try:
            num_rpt = int(sd.askstring("Input", "number of times to run main loop:"))
            if num_rpt <= 0:
                mb.showerror("Error", "enter a valid number of repetitions")
                return
        except (ValueError, TypeError):
            mb.showerror("Error", "invalid input for the number of repetitions")
            return

        for i in range(num_rpt):
            if stop_l:
                break
            perf_actions(num_wins)

root = tk.Tk()
root.title("6 Clicker GUI")

coords = []
run_inf = tk.BooleanVar()
stop_l = False

instr = tk.Label(root, text="Click the buttons below to start")
instr.pack(pady=10)

req_btn = tk.Button(root, text="Define 6 Click Points", command=req_clicks)
req_btn.pack(pady=10)

run_chk = tk.Checkbutton(root, text="Run indefinitely", variable=run_inf)
run_chk.pack(pady=10)

sbutton = tk.Button(root, text="Start Main Loop", command=ml_actions)
sbutton.pack(pady=10)

root.mainloop()
