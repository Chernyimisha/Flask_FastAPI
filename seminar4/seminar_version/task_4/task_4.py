from os import listdir
from os.path import join, isfile
from threading import Thread
from time import time

directory = '.'
threads = []
start_time = time()


def print_time(func):
    def wrapper(*args):
        start_time = time()
        func(*args)
        print(f'in {time() - start_time:.2f} sec')

    return wrapper


def file_listening(arg):
    f = join(directory, arg)
    words = 0
    if isfile(f):
        with open(f) as file:
            for line in file:
                words += len(line.split())
        print(f'\nFile: {f:>38}  \twords: {words:>5} ')


@print_time
def loop_func():
    for file_path in listdir(directory):
        thread = Thread(target=file_listening, args=[file_path])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


loop_func()
