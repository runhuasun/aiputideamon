# encoding:utf-8

import argparse
import config
import psycopg2
from common import log, const
from multiprocessing import Pool


# 启动通道
def start_process(config_path):
    try:
        # 若为多进程启动,子进程无法直接访问主进程的内存空间,重新创建config类
        config.load_config(config_path)

        # 执行任务的逻辑
        
    except Exception as e:
        log.error("进程发生错误", str(e))


def main():
    try:
        # load config
        config.load_config(args.config)



        # 使用进程池启动其他通道子进程
        pool = Pool(len(channel_type))
        for type_item in channel_type:
            log.info("[INIT] Start up: {} on {}", model_type, type_item)
            pool.apply_async(start_process, args=[type_item, args.config])

        if terminal:
            start_process(terminal, args.config)

        # 等待池中所有进程执行完毕
        pool.close()
        pool.join()
    except Exception as e:
        log.error("App startup failed!")
        log.exception(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="config.json path(e.g: ./config.json  or  /usr/local/bot-on-anything/config.json)",type=str,default="./config.json")
    args = parser.parse_args()
    main()
