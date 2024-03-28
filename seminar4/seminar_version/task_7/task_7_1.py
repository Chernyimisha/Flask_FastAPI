from random import randint
from threading import Thread
from time import time

start_time = time()
threads = []

arr = [randint(0, 101) for i in range(1, 1000001)]


def arr_sum(arg):
    res = sum(arg)
    print(f"{res} calculated in {time() - start_time:.2f} seconds")


for i in range(5):
    t = Thread(target=arr_sum, args=[arr], daemon=True)
    threads.append(t)
    t.start()

if __name__ == '__main__':
    for t in threads:
        t.join()
