from __future__ import annotations
from threading import Lock, Thread
from typing import Optional
import numpy as np
from .square import Square
from package.global_variable import variables


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instance: Optional[Face] = None

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Face:

    def __init__(self, idx_face, universe):
        self.idx = idx_face
        self.universe = universe

    def show(self, brightness):
        bytes_packet = bytearray([brightness] * 512)
        print(bytes_packet)
        [a.set(bytes_packet) for a in variables.artnet_group.listArtNet if a.UNIVERSE in self.universe]
