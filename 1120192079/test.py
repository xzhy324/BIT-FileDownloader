import requests
import click
import os
from tqdm import tqdm
import logging
from concurrent import futures
import threading
import time



# 测试链接
# opus语料库中的一份语料
# https://opus.nlpl.eu/download.php?f=ada83/v1/tmx/en-ru.tmx.gz
# linux内核
# https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz
# 随机的一张图片
# https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png


@click.command()
@click.option("-u", "--url", prompt='URL', help='URL to download',multiple=True)
@click.option('-o', '--output', default='./', help='Output filename')
@click.option('-n', '--concurrency', default=8, help='Concurrency number (default: 8)')
@click.option('-i', '--input', help='filename with multiple URL')
def entry(url, output, concurrency,input):
    if input == None:
        print('input none')

    for single in url:
        print(single)
    pass


if __name__ == '__main__':
    entry()
