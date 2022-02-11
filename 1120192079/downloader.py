import click
import os
import logging
from core.ftpdownloader import FtpDownloader
from core.httpdownloader import HttpDownloader

settings = {}  # 配置文件，从settings.txt中加载

# 测试链接
# opus语料库中的一份语料
# https://opus.nlpl.eu/download.php?f=ada83/v1/tmx/en-ru.tmx.gz
# linux内核
# https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz
# 随机的一张图片
# https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png




@click.command()
@click.option('-u', '--url', help='URL to download', multiple=True)
@click.option('-o', '--output', default='./', help='Output filename')
@click.option('-n', '--concurrency', default=8, help='Concurrency number (default: 8)')
@click.option('-i', '--input', help='filename with multiple URL')
@click.option('--ftp', help="ftpDownload:true,false[default]", default='false')
# 根据下载url的数量和是否指定了下载文件列表来分发任务
def entry(url, output, concurrency, input, ftp):
    # 初始化配置文件
    http_downloader = HttpDownloader()

    # 批量url下载
    for single_url in url:
        http_downloader.start_single_task(single_url, output, concurrency)
    # 从文件下载
    if input is not None:
        if not os.path.exists(input):
            logging.error("Input file does not exist!")
            with open(input, 'r') as f:
                for single_url in f.readlines():
                    http_downloader.start_single_task(single_url, output, concurrency)
    # 从ftp下载
    # TODO
    if ftp == 'true':
        input_stream = click.get_text_stream('stdin')
        click.echo("please enter ftp host url:", nl=False)
        host = input_stream.readline()[:-1]
        click.echo("username:",nl=False)
        username = input_stream.readline()[:-1]
        click.echo("password:", nl=False)
        password = input_stream.readline()[:-1]
        click.echo("remote file name:", nl=False)
        remotefile = input_stream.readline()[:-1]
        click.echo("local storage path:", nl=False)
        localpath = input_stream.readline()[:-1]

        ftp_downloader = FtpDownloader()
        ftp_downloader.start_task(host, username, password, remotefile, localpath)


if __name__ == '__main__':
    entry()
