import boto3
from botocore.exceptions import ClientError


class DynamoDB:
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def create_table(self):
        try:
            response = self.client.create_table(
                TableName='hosts',
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'},
                    {'AttributeName': 'host_name', 'KeyType': 'RANGE'},
                    {'AttributeName': 'ip_address', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id','AttributeType': 'N'},
                    {'AttributeName': 'host_name', 'AttributeType': 'S'},
                    {'AttributeName': 'ip_address', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            return response
        except ClientError as err:
            raise err

    def delete_table(self):
        try:
            self.client.delete_table(TableName='hosts')
        except ClientError as err:
            raise err
