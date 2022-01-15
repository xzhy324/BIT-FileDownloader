import requests
import click
import os
from tqdm import tqdm
import logging
from concurrent import futures
import threading
import time


settings = {}  # 配置文件，从settings.txt中加载

# 测试链接
# opus语料库中的一份语料
# https://opus.nlpl.eu/download.php?f=ada83/v1/tmx/en-ru.tmx.gz
# linux内核
# https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.tar.xz
# 随机的一张图片
# https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png


def _download_by_range(lock, url, segment_id, start, end, target_filename):
    """
    :param lock: 对磁盘的互斥读写锁
    :param url:文件链接
    :param segment_id:分段号
    :param start:开始字节
    :param end:结束字节
    :param target_filename:输出路径
    :return: {'cracked':bool [,'segment_id':int] }
    """
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url=url, headers=headers)
    expected_segment_length = end - start + 1
    if not r or len(r.content) != expected_segment_length:
        logging.error("segment[%d]:bytes=%d-%d failed!" % (segment_id, start, end))
        return {'cracked': True}

    lock.aqquire()  # 将内存中下载好的内容保存到磁盘中需要读写锁
    try:
        with open(target_filename, mode='rb+') as fp:
            fp.seek(start)  # 定位到起始字节
            fp.write(r.content)
    except Exception as e:
        logging.error("segment[{}]:bytes={}}-{} failed!,Reason:{}".format(segment_id, start, end, e))
        return {'cracked': True}
    finally:
        lock.release()
    logging.debug("segment[{}]:bytes={}}-{} downloaded!".format(segment_id, start, end))
    return {
        'cracked': False,
        'segment_id': segment_id
    }


@click.command()
@click.option("-u", "--url", prompt='URL', help='URL to download')
@click.option('-o', '--output', default='./', help='Output filename')
@click.option('-n', '--concurrency', default=8, help='Concurrency number (default: 8)')
def entry(url, output, concurrency):
    """
    :param url: URL to download
    :param output: Output filename
    :param concurrency: oncurrency number (default: 8)
    :return: None
    """
    target_filename = os.path.join(output, os.path.basename(url))

    # 判断临时文件是否存在
    if os.path.exists(target_filename):
        logging.error("The File has already been created!")
        return

    # 在头文件中请求一个字节，以测定网站是否满足多线程的下载方式
    r = requests.head(url)
    # 判断是否能够正常连接
    if not r:
        logging.error("Get URL headers failed.Task aborted!")
        return
    file_size = int(r.headers['Content-Length'])
    logging.info("file_size %d Bytes" % file_size)

    if r.status_code == 206:  # 多线程下载
        # 由于 _download_by_range 中使用 rb+ 模式，必须先保证文件存在，所以要先创建指定大小的临时文件 (用0填充)
        mt_chunk_size = int(settings['chunk_size'])  # 加载多线程下载中所使用的分块大小
        with open(target_filename, 'wb') as fp:
            fp.seek(file_size - 1)
            fp.write(b'\0')

        with futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            tmp_part_count, tmp_mod = divmod(file_size, mt_chunk_size)
            segments = tmp_part_count if tmp_mod == 0 else int(tmp_part_count) + 1
            logging.info("chunk_count %d Bytes chunk mod %d" % (tmp_part_count, tmp_mod))

            lock = threading.Lock()  # 创建互斥文件读写锁
            thread_queue = []  # 线程标记队列
            for segment_id in range(segments):
                start_byte = segment_id * mt_chunk_size
                end_byte = start_byte + mt_chunk_size - 1
                # 注意若当前块为最后一块，则结束字节需要重新指定
                if segment_id == segments - 1:
                    end_byte = file_size - 1
                future = executor.submit(_download_by_range, lock, url, segment_id, start_byte, end_byte,
                                         target_filename)
                thread_queue.append(future)

    else:  # 单线程下载
        bar = tqdm(
            unit='B',  # 默认为位，改为字节作为默认单位
            unit_divisor=1024,  # 将传输速率的单位改为存储字节的单位
            unit_scale=True,  # 自动扩展单位
            ascii=True,  # windows下正确显示需要指定显示模式为utf8
            desc=target_filename  # 在进度条前方显示下载的文件名
        )
        single_response = requests.get(url, stream=True)
        single_response.raise_for_status()
        with open(target_filename, 'wb') as fp:
            for chunk in single_response.iter_content(chunk_size=512):
                if chunk:  # chunk的大小不为零，继续下载
                    fp.write(chunk)
                    bar.update(len(chunk))
        logging.info("download completed")


# 加载配置文件并指定控制台日志的级别
def init_settings():
    # default settings
    settings['chunk_size'] = 1024
    settings['logging.level'] = 'INFO'
    # 加载配置文件
    with open('./settings.txt', 'r', encoding='utf8') as fp:
        for line in fp.readlines():
            line = line.split()
            config_name = line[0]
            config_value = line[1]
            settings[config_name] = config_value
    # print(settings)
    logging.basicConfig(level=settings['logging.level'])  # 设置日志的默认响应级别为INFO,按需要更改成为debug，默认等级为warning


if __name__ == '__main__':
    init_settings()

    start_time = time.time()
    entry()
    end_time = time.time()

    print("total time: {}", format(end_time - start_time))
