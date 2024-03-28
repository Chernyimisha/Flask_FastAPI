from timeit import default_timer, timeit
from random import randint
from multiprocessing import Process

arr = [randint(0, 101) for i in range(1, 1000001)]


def time_it(func):
    def wrapper(numb):
        start_time = default_timer()
        func(numb)
        # правая отсечка времени и результат
        print(default_timer() - start_time)
        # логгирование
        # и любые другие действия

    return wrapper


@time_it
def get_sum(arr):
    return sum(arr)


processes = []

if __name__ == 'main':

    for _ in range(5):
        process = Process(target=get_sum, args=[arr])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()