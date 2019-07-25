from threading import Thread
from package.global_variable.variables import *
import time


class SequenceManager(Thread):
    """Class daemon thread to manage Queue

    """
    def __init__(self, global_var):
        """Constructor of SequenceManager

        :param global_var: global var of API
        """
        Thread.__init__(self)
        self.global_var = global_var
        self.daemon = True

    def run(self):
        """callback function of the thread

         this function manage the queue of the API
        :return: end of daemon thread
        """
        while True:
            time.sleep(2)
            if self.global_var['sequence']:
                if queue_manager.nb_seq_in_queue() != 0:
                    queue_manager.set_current_thread()
                    time.sleep(2)
                    queue_manager.current_thread.start()
                    queue_manager.current_thread.join()
                    time.sleep(2)
                    cube.blackout_cube()
        return
