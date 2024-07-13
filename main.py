from pynput.keyboard import Key, Events
from pynput.keyboard import Listener as Kl
from pynput.keyboard import Controller as Kc
from pynput.mouse import Button
from pynput.mouse import Controller as Mc
from pynput.mouse import Listener as Ml
import sys
import time


mouse = Mc()
keyboard = Kc()

movements = []
wait_time = -1

print("Once you press enter you will have the ammount of time specified to do your movemnts")
print("It will begin recording immediatley and will stop after the given time")
print("It is recommended to add some dead time to the start of your movements so you can ctrl+c the program in an emergency")
while wait_time < 0:
    try: wait_time = int(input("How much time will you need? (s) "))
    except: print("please enter a positive number")

start = time.time()

def on_move(x, y):
    print(len(movements))
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

def exit_listener(key):
    if key == Key.esc:
        print("Thanks for using this tool")
        sys.exit()


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

time.sleep(wait_time)
keyboard_listener.stop()
listener.stop()

print("Recording complete")
print("Starting in...")
time.sleep(0.5)
for i in range(3,0,-1):
    print(f"\t{i}")
    time.sleep(1)
movements.pop(0)

iterations = None

print("How many times do you want to loop this? (negative value for infinite) ")
print("If you would like to stop immediatley then press escape")
while iterations == None:
    try: iterations = int(input("Iterations > "))
    except: print("please enter a number")


keyboard_listener = Kl(
        on_press=exit_listener)
keyboard_listener.start()

if iterations < 0:
    while True:
        index = 0
        start = time.time()
        while index < len(movements):
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
            #for event in Events():
            #    if event.key == Key.esc:
            #        print("Thanks for using this tool")
            #        sys.exit()
            current_instruction = movements[index]
            if time.time()-start > current_instruction[1]:
                index += 1
                move(current_instruction)
    
