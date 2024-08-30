import boto3
import os


def aws_config(service="s3", localstack=True):
    return (
        {
            'service_name': service,
            'aws_access_key_id': os.getenv("LOCALSTACK_ACCESS_KEY"),
            'aws_secret_access_key': os.getenv("LOCALSTACK_SECRET_KEY"),
            'endpoint_url': os.getenv("LOCALSTACK_ENDPOINT"),
        }
        if localstack
        else {
            'service_name': service,
            'aws_access_key_id': os.getenv("AWS_ACCESS_KEY"),
            'aws_secret_access_key': os.getenv("AWS_SECRET_KEY"),
        }
    )


def aws_client(config):
    return boto3.client(**config)
