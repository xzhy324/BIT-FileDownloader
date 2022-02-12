import click
import os
import logging
from core.ftpdownloader import FtpDownloader
from core.httpdownloader import HttpDownloader


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
        http_downloader.start_task(url=single_url, output=output, concurrency=concurrency)
    # 从文件下载
    if input is not None:
        if not os.path.exists(input):
            logging.error("Input file does not exist!")
        else:
            with open(input, 'r') as f:
                for single_url in f.readlines():
                    single_url = single_url.strip()  # 注意结尾的回车应该删去
                    if single_url == '':
                        continue  # 空行略过
                    http_downloader.start_task(url=single_url, output=output, concurrency=concurrency)
    # 从ftp下载
    if ftp == 'true':
        input_stream = click.get_text_stream('stdin')
        click.echo("please enter ftp host url:", nl=False)
        host = input_stream.readline()[:-1]
        click.echo("username:", nl=False)
        username = input_stream.readline()[:-1]
        click.echo("password:", nl=False)
        password = input_stream.readline()[:-1]
        click.echo("remote file name:", nl=False)
        remotefile = input_stream.readline()[:-1]
        click.echo("local storage path:", nl=False)
        localpath = input_stream.readline()[:-1]

        ftp_downloader = FtpDownloader()
        ftp_downloader.start_task(host=host,
                                  username=username,
                                  password=password,
                                  remotefile=remotefile,
                                  localpath=localpath)


if __name__ == '__main__':
    entry()
