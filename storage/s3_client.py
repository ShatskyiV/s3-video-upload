import boto3

# logging.basicConfig(level=logging.DEBUG)
# boto3.set_stream_logger("botocore", level=logging.DEBUG)


class S3Client:
    def __init__(self, **client_kwargs):
        self.client = None
        self.client_kwargs = client_kwargs

    def connect(self):
        if not self.client:
            self.client = boto3.client("s3", **self.client_kwargs)
        return self.client

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
