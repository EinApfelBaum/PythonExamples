import threading

class Human(threading.Thread):
    def run(self):
        for _ in range(100):
            print(threading.current_thread().getName())


first = Human(name='Peter')
second = Human(name='Hans')
first.start()
second.start()
