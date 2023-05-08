import time

class ExecutionQueue:
    LOCK_WAIT = 100
    queue = None
    write_lock = False

    def __init__(self):
        self.queue = []

    def submit(self, task, delay=0.0):
        lock_wait = 0
        self.queue.append((task, time.monotonic() + delay))
        while self.write_lock:
            self.lock_wait += 1
            if self.lock_wait > self.LOCK_WAIT:
                print("ERROR: Lock wait exceeded! Clearing ExecutionQueue lock")
                self.write_lock = False

    def next(self):
        self.lock_wait = True
        tail = []
        task = None
        current_time = time.monotonic()

        while len(self.queue) > 0:
            exec_task, exec_time = self.queue.pop()
            if exec_time > current_time: 
                tail.append((exec_task, exec_time))
            else:
                task = exec_task
                break

        self.queue.extend(reversed(tail))
        self.lock_wait = False
        return task

    def clear(self):
        self.lock_wait = True
        self.queue.clear()
        self.lock_wait = False
        