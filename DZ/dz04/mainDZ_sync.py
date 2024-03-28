# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения
# в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения
# программы.

import sys
import requests
import time


def download(url, start_time):
    response = requests.get(url)
    filename = f"images/{url.split('/')[-1]}"
    with open(filename, 'wb') as f:
        for line in response.iter_content(1000):
            f.write(line)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':

    urls_concole = [
        'https://r4.wallpaperbetter.com/wallpaper/1008/573/262/the-sky-clouds-trees-landscape-wallpaper-dcb4070adceb26342be4e9ebf685ac19.jpg',
        'https://bipbap.ru/wp-content/uploads/2017/09/1585931258_5-p-foni-s-krasivimi-peizazhami-16.jpg',
        'https://gas-kvas.com/uploads/posts/2023-02/1675446642_gas-kvas-com-p-kartinki-na-fonovii-risunok-rabochego-9.jpg',
        'https://mobimg.b-cdn.net/v3/fetch/60/60136e84e7fd3ae2eeb153747c92d786.jpeg',
        'https://fikiwiki.com/uploads/posts/2022-02/1644865303_51-fikiwiki-com-p-skachat-kartinki-khoroshego-kachestva-59.jpg',
        'https://klike.net/uploads/posts/2019-11/1574605343_39.jpg'
        ]

    start_event = time.time()
    if len(sys.argv) == 1:
        urls = urls_concole
    else:
        urls = sys.argv
        del urls[0]

    for url in urls:
        start_iter = time.time()
        download(url, start_iter)

    print(f"Downloaded all URLs in {time.time() - start_event:.2f} seconds")