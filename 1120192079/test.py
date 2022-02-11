import sys

import requests
import click
import os
from tqdm import tqdm
import logging
from concurrent import futures
import threading
import time
import os
import exrex

# 测试链接
# opus语料库中的一份语料
# https://opus.nlpl.eu/download.php?f=ada83/v1/tmx/en-ru.tmx.gz
# linux内核
# https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz
# 随机的一张图片
# https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png


if __name__ == '__main__':
    input = 'http://www\.gov\.cn/xinwen/2022-02/11/content_567304[0-9]\.htm'
    urls = list(exrex.generate(input, 100))
    for url in urls:
        print(url)
