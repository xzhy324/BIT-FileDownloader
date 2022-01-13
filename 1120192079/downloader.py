import requests
import click
import os
from tqdm import tqdm
import logging


# 测试链接 linux内核
# https://opus.nlpl.eu/download.php?f=ada83/v1/tmx/en-ru.tmx.gz
# https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz
@click.command()
@click.option("-u", "--url", prompt='URL', help='URL to download')
@click.option('-o', '--output', default='./', help='Output filename')
@click.option('-n', '--concurrency', default=8, help='Concurrency number (default: 8)')
def entry(url, output, concurrency):

    target_filename = os.path.join(output, os.path.basename(url))
    # print("destination_path : {}".format(target_filename))
    # stream + iter_content指定chunk_size，能够实现分块的流式下载

    bar = tqdm(
        unit='B',  # 默认为位，改为字节作为默认单位
        unit_divisor=1024,  # 将传输速率的单位改为存储字节的单位
        unit_scale=True,  # 自动扩展单位
        ascii=True,  # windows下正确显示需要指定显示模式为utf8
        desc=target_filename  # 在进度条前方显示下载的文件名
        )
    my_response = requests.get(url, stream=True)
    my_response.raise_for_status()
    with open(target_filename, 'wb') as fp:
        for chunk in my_response.iter_content(chunk_size=512):
            if chunk:   # chunk的大小不为零，继续下载
                fp.write(chunk)
                bar.update(len(chunk))
    logging.info("download completed")


if __name__ == '__main__':
    logging.basicConfig(level='INFO')  # 设置日志的默认响应级别为DEbug
    entry()
