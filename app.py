# encoding:utf-8

import argparse
import config
import psycopg2
from common import log
from multiprocessing import Pool


# 训练LoRA
def trainLoRA_process(config_path):
    try:
        # 若为多进程启动,子进程无法直接访问主进程的内存空间,重新创建config类
        config.load_config(config_path)

        # 执行任务的逻辑
        conn = psycopg2.connect(database="neondb", user="runhuasun", password="isG02XlZAxUL", host="ep-shy-frog-644279.us-east-2.aws.neon.tech", port="5432")

        cur = conn.cursor()
        cur.execute('SELECT "id" FROM "Room"')
        rows = cur.fetchall()

        for row in rows:
            print(row[0])

        conn.close()

    except Exception as e:
        log.error(str(e))


# 主进程
def main():
    try:
        # load config
        config.load_config(args.config)

        # 使用进程池启动其他通道子进程
        pool = Pool(1)

        # 启动脱机处理生成LORA模型的进程
        pool.apply_async(trainLoRA_process, args=[args.config])

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
