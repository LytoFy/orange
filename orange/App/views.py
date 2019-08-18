'''
    图片上传模块
        使用：  Upload().file(file)   # file 为request.post.file('test')
        reuturn 云存储url

'''

class Upload():
    @classmethod
    def file(cls, file):
        '''
            文件上传接口
            :param file: 接收的文件
            :return: 返回上传文件的地址。
        '''


        BASE_url = "https://sz-1257470685.cos.ap-guangzhou.myqcloud.com"



        client = cls().__cloud_setting()
        type_name = cls().__getName(file.name)


        response = client.put_object(
            Bucket='sz-1257470685',
            Body=file.read(),
            Key=type_name,
            StorageClass='STANDARD',
            EnableMD5=False
        )

        if response['ETag']:

            return BASE_url + "/" + type_name
        else:
            raise NotImplementedError()

    def __getName(self, name):

        import uuid
        name = uuid.uuid4().hex + name[name.rfind("."):]
        return str(name)

    def __cloud_setting(self):
        import logging
        from qcloud_cos import CosConfig
        from qcloud_cos import CosS3Client
        import sys

        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        secret_id = 'AKIDugKv1c2uMeDkYFaOjt4A5JPTPDrUHM9q'
        secret_key = 'mNFzb7Ws791hIo9JG2VowwujMo7B3Pfq'
        region = 'ap-guangzhou'
        token = None
        scheme = 'https'
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        client = CosS3Client(config)
        return client
