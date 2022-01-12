import requests
import click
import os
from tqdm import tqdm


@click.command()
@click.option("-u", "--url", prompt='URL', help='URL to download')
@click.option('-o', '--output', default='./', help='Output filename')
@click.option('-n', '--concurrency', default=8, help='Concurrency number (default: 8)')
def entry(url, output, concurrency):
    target_filename = output + os.path.basename(url)
    # print("destination_path : {}".format(target_filename))
    # stream + iter_content指定chunk_size，能够实现分块的流式下载
    with tqdm(unit='B',  # 指定基础单位为字节
              unit_scale=True,  # 自动扩展单位
              unit_divisor=1024,  # 按1024计算分块，默认为1000需要修改
              ascii=True,
              desc=target_filename) \
            as bar:  # 打印下载时的进度条，实时显示下载速度
        my_response = requests.get(url, stream=True)
        my_response.raise_for_status()
        with open(target_filename, 'wb') as fp:
            for chunk in my_response.iter_content(chunk_size=512):
                if chunk:
                    fp.write(chunk)
                    bar.update(len(chunk))
    print("complete!")


if __name__ == '__main__':
    entry()
