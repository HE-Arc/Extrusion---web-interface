import queue


class QueueManger:
    """Class to manage a thread-safe queue

    """
    def __init__(self, size):
        """Constructor of QueueManage

        The Queue is a deque

        :param size: size of queue
        """
        self.size = size
        self.process_pool = queue.Queue(size)
        self.current_thread = None

    def set_current_thread(self):
        """set the current_thread variable with first sequence in the queue

        """
        self.current_thread = self.process_pool.get(block=False)

    def delete(self, index):
        """delete a sequence in th queue

        :param index: index of sequence to delete
        :raise: IndexError
        """
        with self.process_pool.mutex:
            try:
                del self.process_pool.queue[index]
            except IndexError:
                raise

    def kill_current_seq(self):
        """kill the sequence who is in the current_thread variable

        :return: state oof current_thread variable
        """
        if self.current_thread is not None:
            self.current_thread.kill()
            self.current_thread = None
            return "Current sequence stop"
        return "No sequence running"

    def delete_all(self):
        """Erase the whole queue

        """
        with self.process_pool.mutex:
            self.process_pool.queue.clear()
            if self.current_thread is not None:
                self.current_thread.kill()
                self.current_thread = None

    def move(self, old_index, new_index):
        """move a sequence in to queue to a new index

        :param old_index: sequence to move
        :param new_index: new index of sequence
        :raise IndexError
        """
        with self.process_pool.mutex:
            try:
                old = self.process_pool.queue[old_index]
                del self.process_pool.queue[old_index]
                self.process_pool.queue.insert(new_index, old)
            except IndexError:
                raise

    def nb_seq_in_queue(self):
        """get nb sequence in queue

        :return: nb sequence in queue
        """
        with self.process_pool.mutex:
            return len(self.process_pool.queue)

    def insert(self, code, index):
        """Insert a sequence in the queue ar specific index

        :param code: ThreadwithTrace Object
        :param index: index where insert the sequence
        """
        with self.process_pool.mutex:
            self.process_pool.queue.insert(index, code)
