from threading import Thread
from package.global_variable.variables import *
import time


class SequenceManager(Thread):
    def __init__(self, global_var):
        Thread.__init__(self)
        self.global_var = global_var
        self.daemon = True

    def run(self):
        while True:
            if process_pool.empty():
                self.global_var['state'] = 'free'
            current_thread[0] = process_pool.get()
            self.global_var['state'] = 'busy'
            time.sleep(2)
            current_thread[0].start()
            current_thread[0].join()
            cube.blackout_cube()
            time.sleep(5)
        return
