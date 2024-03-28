# Задание №5
# � Создать программу, которая будет производить подсчет
# количества слов в каждом файле в указанной директории и
# выводить результаты в консоль.
# � Используйте процессы.

import multiprocessing
import os

count = 0


def process_file(file_path):
    global count
    with open(file_path, 'r', encoding='latin-1') as f:
        contents = f.read()
        # do some processing with the file contents
        count += len(contents)
        print(f'{f.name} содержит {len(contents)} слов. Всего слов в папке: {count}')


if __name__ == '__main__':

    processes = []
    dir_path = '../../../PythonCourse/ubuntu'
    files = os.listdir(dir_path)
    for f in files:
        f = os.path.join(dir_path, f)
        p = multiprocessing.Process(target=process_file, args=(f, ))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print("Все процессы завершили работу")


