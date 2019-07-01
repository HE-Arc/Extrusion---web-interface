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
            time.sleep(2)
            if self.global_var['sequence']:
                if queue_manager.nb_seq_in_queue() != 0:
                    queue_manager.set_current_thread()
                    time.sleep(2)
                    queue_manager.current_thread.start()
                    queue_manager.current_thread.join()
                    cube.blackout_cube()
                    time.sleep(3)
        return
