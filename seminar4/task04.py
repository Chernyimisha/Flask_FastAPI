# Задание №4
# � Создать программу, которая будет производить подсчет
# количества слов в каждом файле в указанной директории и
# выводить результаты в консоль.
# � Используйте потоки.

import threading
import os



def process_file(file_path):
    global count
    with open(file_path, 'r', encoding='latin-1') as f:
        contents = f.read()
        # do some processing with the file contents
        count += len(contents)
        print(f'{f.name} содержит {len(contents)} слов. Всего слов в папке: {count}')


threads = []
dir_path = '../../../PythonCourse/ubuntu'
files = os.listdir(dir_path)
count = 0

for f in files:
    f = os.path.join(dir_path, f)
    if os.path.isfile(f):
        t = threading.Thread(target=process_file, args=(f, ))
        threads.append(t)
        t.start()

for t in threads:
    t.join()

print("Все потоки завершили работу")
