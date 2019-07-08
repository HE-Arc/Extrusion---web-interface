import queue


class QueueManger:
    def __init__(self, size):
        self.size = size
        self.process_pool = queue.Queue(size)
        self.current_thread = None

    def set_current_thread(self):
        self.current_thread = self.process_pool.get(block=False)

    def delete(self, index):
        with self.process_pool.mutex:
            try:
                del self.process_pool.queue[index]
            except IndexError:
                raise

    def kill_current_seq(self):
        if self.current_thread is not None:
            self.current_thread.kill()
            self.current_thread = None
            return "Current sequence stop"
        return "No sequence running"

    def delete_all(self):
        with self.process_pool.mutex:
            self.process_pool.queue.clear()
            if self.current_thread is not None:
                self.current_thread.kill()
                self.current_thread = None

    def move(self, old_index, new_index):
        with self.process_pool.mutex:
            try:
                old = self.process_pool.queue[old_index]
                del self.process_pool.queue[old_index]
                self.process_pool.queue.insert(new_index, old)
            except IndexError:
                raise

    def get_queue(self):
        with self.process_pool.mutex:
            return self.process_pool.queue

    def nb_seq_in_queue(self):
        with self.process_pool.mutex:
            return len(self.process_pool.queue)

    def insert(self, code, index):
        with self.process_pool.mutex:
            self.process_pool.queue.insert(index, code)
