import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Key, Events
from pynput.keyboard import Listener as Kl
from pynput.keyboard import Controller as Kc
from pynput.mouse import Button
from pynput.mouse import Controller as Mc
from pynput.mouse import Listener as Ml
import sys
import time
import threading



root = tk.Tk()
root.title("afk keyboard tool")
root.resizable(False, False)
root.attributes('-topmost', True)
root.update()

frm = ttk.Frame(root, padding=10)
frm.grid()


movements = []

recording_time = -1
start = 0
timing_text = tk.StringVar()


ttk.Label(frm,text=" Welcome to the \nafk keyboard tool").grid(column=2, row=0)
ttk.Label(frm,text="Enter recording time: ").grid(column=1,row=1)
recording_time_entry = ttk.Entry(frm)
recording_time_entry.grid(column=3,row=1)
ttk.Label(frm,text="Enter iterations (-1 for infinite): ").grid(column=1,row=2)
iterations_entry = ttk.Entry(frm)
iterations_entry.grid(column=3,row=2)
timings_label = ttk.Label(frm, textvariable=timing_text)
timings_label.grid(column=3, row=3)
mouse = Mc()
keyboard = Kc()

ttk.Label(frm,text="Don't touch this window\n       When recording").grid(column=2, row=4)


def on_move(x, y):
    movements.append((f"M {mouse.position[0]} {mouse.position[1]}", time.time()-start))

def on_click(x, y, button, pressed):
    pcode = 'P'
    rcode = 'R'
    if button == Button.right:
        pcode = 'O'
        rcode = 'o'
    if pressed:
        movements.append((f"P {x} {y}", time.time()-start))
    else:
        movements.append((f"R {x} {y}", time.time()-start))

def on_scroll(x, y, dx, dy):
    movements.append((f"S {dy}", time.time()-start))

    
def on_press(key):
    movements.append((f"p", time.time()-start, key))

def on_release(key):
    movements.append((f"r", time.time()-start, key))

def move(full_instruct):
    instruction = full_instruct[0].split(" ")
    match instruction[0]:
        case 'M':
            mouse.position = (int(instruction[1]), int(instruction[2]))
        case 'P':
            mouse.press(Button.left)
        case 'R': 
            mouse.release(Button.left)
        case 'O':
            mouse.press(Button.right)
        case 'o': 
            mouse.release(Button.right)
        case 'S':
            mouse.scroll(0, int(instruction[1]))
        case 'p':
            keyboard.press(full_instruct[2])
        case 'r':
            keyboard.release(full_instruct[2])

def record():
    movements.clear()
    wait_time = -1

    print("Once you press enter you will have the ammount of time specified to do your movemnts")
    print("It will begin recording immediatley and will stop after the given time")
    
    try:
        wait_time = float(recording_time_entry.get())
        if wait_time < 0:
            return 0
    except:
        print("please enter a positive number")
        return 0
    global start
    start = time.time()

    # Collect events until released
    keyboard_listener = Kl(
            on_press=on_press,
            on_release=on_release)
    keyboard_listener.start()

    listener = Ml(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
    listener.start()

    for i in range(int(wait_time*100), 0, -1):
        timing_text.set(f"{i/100}s")
        root.update_idletasks()
        time.sleep(1/100)
        root.update()
    keyboard_listener.stop()
    listener.stop()

    print("Recording complete")

def loop():
    iterations = None

    try:
        iterations = int(iterations_entry.get())
    except:
        print("please enter a number")
        return 0


    print("Starting in...")
    time.sleep(0.5)
    for i in range(3*100,0,-1):
        timing_text.set(f"Starting in{i/100}s")
        root.update_idletasks()
        time.sleep(1/100)
        root.update()
    if len(movements) > 0:
        movements.pop(0)

    if iterations < 0:
        while True:
            index = 0
            start = time.time()
            while index < len(movements):
                timing_text.set(f"{index}")
                root.update_idletasks()
                root.update()
                #for event in Events():
                #    if event.key == Key.esc:
                #        print("Thanks for using this tool")
                #        sys.exit()
                current_instruction = movements[index]
                if time.time()-start > current_instruction[1]:
                    index += 1
                    move(current_instruction)
    else:
        for _ in range(iterations):
            index = 0
            start = time.time()
            while index < len(movements):
                timing_text.set(f"{index}")
                root.update_idletasks()
                root.update()
                #for event in Events():
                #    if event.key == Key.esc:
                #        print("Thanks for using this tool")
                #        sys.exit()
                current_instruction = movements[index]
                if time.time()-start > current_instruction[1]:
                    index += 1
                    move(current_instruction)

def play_on_thread():
    loop()
def record_on_thread():
    record()

def destroy():
    root.destroy()
    print("\nthanks for using the tool")
    quit()


ttk.Button(frm, text="Quit", command=destroy).grid(column=2, row=5)
ttk.Button(frm, text="Record", command=record_on_thread).grid(column=1, row=4)
ttk.Button(frm, text="Play", command=play_on_thread).grid(column=3, row=4)


root.mainloop()
