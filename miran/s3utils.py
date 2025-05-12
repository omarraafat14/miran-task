from storages.backends.s3boto3 import S3Boto3Storage


def StaticS3BotoStorage():
    return S3Boto3Storage(location="miran/static")


def MediaS3BotoStorage():
    return S3Boto3Storage(location="miran/media")
