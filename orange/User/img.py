import datetime

import pymysql
import os

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDugKv1c2uMeDkYFaOjt4A5JPTPDrUHM9q'  # 替换为用户的 secretId
secret_key = 'mNFzb7Ws791hIo9JG2VowwujMo7B3Pfq'  # 替换为用户的 secretKey
region = 'ap-guangzhou'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
BASE_url = "https://sz-1257470685.cos.ap-guangzhou.myqcloud.com"


def getName(name):
    import uuid
    name = uuid.uuid4().hex + name[name.rfind("."):]
    return name


def SQL(path, type_id):
    connect = pymysql.connect(host="111.230.10.23", user="orange", password="123456", db='orangedb')
    cursor = connect.cursor()

    sql = "insert into mural(path, date, type_id) values(%s,%s, %s)"

    cursor.execute(sql, (path, str(datetime.datetime.now()), type_id,))

    connect.commit()
    print("插入成功")


currdir = r"C:\Users\pqw\Desktop\壁纸\唯美"
filelist = os.listdir(currdir)

for name in filelist:
    currpath = os.path.join(currdir, name)
    type_name = getName(name)
    response = client.upload_file(
        Bucket='sz-1257470685',
        LocalFilePath=currpath,
        Key=type_name,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )

    if response['ETag']:
        path = BASE_url + "/" + type_name
        print(path)
        SQL(path, 6)