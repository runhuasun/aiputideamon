# encoding:utf-8

import argparse
import config
import psycopg2
import time
from common import log
from multiprocessing import Pool

# 连接数据库
def getDBCon(config):
    return psycopg2.connect(database="neondb", user="runhuasun", password="isG02XlZAxUL", host="ep-shy-frog-644279.us-east-2.aws.neon.tech", port="5432")

# 训练LoRA
def trainLoRA_process(config_path):
    try:
        # 若为多进程启动,子进程无法直接访问主进程的内存空间,重新创建config类
        config.load_config(config_path)
        conn = getDBCon(config)
        
        # 执行任务的逻辑


        # 循环查询所有状态为CREATE的模型
        
            # 把模型的状态置为START
            
            # 调用模型生成服务
            
            # 如果模型生成服务返回错误，就把模型状态标记回ERROR，并把模型返回的错误记录到MSG字段
            
        # 等待10秒钟，继续下一次轮询
            
            
        cur = conn.cursor()
        cur.execute('SELECT "id" FROM "Room"')
        rows = cur.fetchall()

        # 
        for row in rows:
            print(row[0])
            time.sleep(1)

        conn.close()

    except Exception as e:
        log.error(str(e))


# 查询并更新LoRA训练状态
def updateLoRA_process(config_path):
    try:
        # 若为多进程启动,子进程无法直接访问主进程的内存空间,重新创建config类
        config.load_config(config_path)

        # 执行任务的逻辑
        conn = getDBCon(config)

        # 循环查询所有状态为START的模型

            # 查询模型生成服务当前模型状态
            
            # 如果生成完毕就把模型的状态置为FINISH
            
            # 如果模型生成服务返回错误，就把模型状态标记回ERROR，并把模型返回的错误记录到MSG字段
            
        # 等待10秒钟，继续下一次轮询
            
            
        cur = conn.cursor()
        cur.execute('SELECT "func" FROM "Room"')
        rows = cur.fetchall()

        # 
        for row in rows:
            print(row[0])
            time.sleep(2)

        conn.close()

    except Exception as e:
        log.error(str(e))

        
        
        
        
# 主进程
def main():
    try:
        # load config
        config.load_config(args.config)

        # 使用进程池启动其他通道子进程
        pool = Pool(2)

        # 启动脱机处理生成LORA模型的进程
        pool.apply_async(trainLoRA_process, args=[args.config])
        pool.apply_async(updateLoRA_process, args=[args.config])

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
