import keyboard
from threading import Timer
import time, copy, numpy

key = "d"
snake = {"back": {"x": 0, "y": 1, "z": 12, "b": 15}, "front": {"x": 0, "y": 3, "z": 12, "b": 15}}
snake_previous = {"back": {"x": 0, "y": 1, "z": 12, "b": 0}, "front": {"x": 0, "y": 3, "z": 12, "b": 0}}
change = False
add_y, add_z = 2, 0
y_limit_max, y_limit_min = 7, 1
z_limit_max, z_limit_min = 11, 0


def start():
    global snake_previous
    global change
    global add_z, add_y
    snake["back"] = copy.deepcopy(snake["front"])

    if key == "d":
        if change:
            add_y = 1
            add_z = int(numpy.sign(add_z))
            change = False
        else:
            add_y = 3 if snake["front"]["y"] == y_limit_max else 2
            add_z = 0

    if key == "a":
        if change:
            add_y = -1
            add_z = int(numpy.sign(add_z))
            change = False
        else:
            add_y = -3 if snake["front"]["y"] == y_limit_min else -2
            add_z = 0
    if key == "w":
        if change:
            add_y = int(numpy.sign(add_y))
            add_z = 1
            change = False
        else:
            add_y = 0
            add_z = 3 if snake["front"]["z"] == z_limit_max else 2
    if key == "s":
        if change:
            add_y = int(numpy.sign(add_y))
            add_z = -1
            change = False
        else:
            add_z = -3 if snake["front"]["z"] == z_limit_min else -2
            add_y = 0

    snake["front"]["y"] = (snake["front"]["y"] + add_y) % 9
    snake["front"]["z"] = (snake["front"]["z"] + add_z) % 13
    print(snake_previous)
    print(snake)
    print(key)
    snake_previous = copy.deepcopy(snake)
    snake_previous["front"]["b"] = 0
    snake_previous["back"]["b"] = 0

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
