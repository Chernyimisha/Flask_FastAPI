# Задание №6
# � Создать программу, которая будет производить подсчет
# количества слов в каждом файле в указанной директории и
# выводить результаты в консоль.
# � Используйте асинхронный подход.

import asyncio
import os

count = 0


async def process_file(file_path):
    global count
    with open(file_path, 'r', encoding='latin-1') as f:
        contents = f.read().split()
        # do some processing with the file contents
        count += len(contents)
        print(f'{f.name} содержит {len(contents)} слов. Всего слов в папке: {count}')
    await asyncio.sleep(1)


async def main():
    tasks = []
    dir_path = '../../../PythonCourse/ubuntu'
    files = os.listdir(dir_path)
    for f in files:
        f = os.path.join(dir_path, f)
        task = asyncio.create_task(process_file(f))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())

