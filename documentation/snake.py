import keyboard
from threading import Timer
import time, copy

key = "d"
change = False
from_left = True
from_up = True
add_data = [0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 16, 16, 16, 16, 20, 20, 20]
snake = {"back": [0, 0, 1, 15], "front": [0, 1, 1, 15]}
snake_previous = {"back": [0, 0, 1, 0], "front": [0, 1, 1, 0]}


def start():
    global snake_previous
    global change
    global from_up
    global from_left
    snake["back"] = copy.deepcopy(snake["front"])
    front = [snake["front"][1], snake["front"][2]]
    if key == "d":
        if change:
            if front[1] == 2:
                snake["front"][1] = (front[0] + 1) % 4 + add_data[front[0]]
                if from_up:
                    snake["front"][2] = (front[1] + 1)
                else:
                    snake["front"][2] = (front[1] - 1)
            if front[1] == 0:
                if from_up:
                    snake["front"][2] = (front[1] + 3)
                else:
                    snake["front"][2] = (front[1] + 1)
            from_left = True
            change = False
        else:
            snake["front"][1] = (front[0] + 1) % 4 + add_data[front[0]]

    if key == "a":
        if change:
            if front[1] == 0:
                snake["front"][1] = (front[0] - 1) % 4 + add_data[front[0]]
                if from_up:
                    snake["front"][2] = (front[1] + 3)
                else:
                    snake["front"][2] = (front[1] + 1)
            if front[1] == 2:
                if from_up:
                    snake["front"][2] = (front[1] - 1)
                else:
                    snake["front"][2] = (front[1] + 1)
            from_left = False
            change = False
        else:
            snake["front"][1] = (front[0] - 1) % 4 + add_data[front[0]]

    if key == "w":
        if change:
            if front[1] == 1:
                snake["front"][1] = (front[0] - 4) % 24
                if from_left:
                    snake["front"][2] = (front[1] + 1)
                else:
                    snake["front"][2] = (front[1] - 1)
            if front[1] == 3:
                if from_left:
                    snake["front"][2] = (front[1] - 1)
                else:
                    snake["front"][2] = (front[1] - 3)
            from_up = True
            change = False
        else:
            snake["front"][1] = (front[0] - 4) % 24

    if key == "s":
        if change:
            if front[1] == 3:
                snake["front"][1] = (front[0] + 4) % 24
                if from_left:
                    snake["front"][2] = (front[1] - 1)
                else:
                    snake["front"][2] = (front[1] - 3)
            if front[1] == 1:
                if from_left:
                    snake["front"][2] = (front[1] + 1)
                else:
                    snake["front"][2] = (front[1] - 1)
            from_up = False
            change = False
        else:
            snake["front"][1] = (front[0] + 4) % 24

    print(snake_previous)
    print(snake)
    print(key)
    snake_previous = copy.deepcopy(snake)
    snake_previous["front"][3] = 0
    snake_previous["back"][3] = 0

    __clock = Timer(2, start)
    __clock.daemon = True
    __clock.start()


if __name__ == '__main__':
    print(snake)
    time.sleep(2)
    start()
    while True:
        try:
            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('a'):
                if key != "d":
                    if key != "a":
                        change = True
                    key = "a"
            elif keyboard.is_pressed('s'):
                if key != "w":
                    if key != "s":
                        change = True
                    key = "s"
            elif keyboard.is_pressed('d'):
                if key != "a":
                    if key != "d":
                        change = True
                    key = "d"
            elif keyboard.is_pressed('w'):
                if key != "s":
                    if key != "w":
                        change = True
                    key = "w"
        except:
            pass
