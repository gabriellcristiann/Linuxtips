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
                    {'AttributeName': 'name', 'KeyType': 'RANGE'},
                    {'AttributeName': 'ip', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'name', 'AttributeType': 'S'},
                    {'AttributeName': 'ip', 'AttributeType': 'S'}
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
