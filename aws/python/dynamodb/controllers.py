import boto3
from botocore.exceptions import ClientError


class DynamoDBCore:
    def __init__(self):
        self.client = boto3.client(
            'dynamodb',
            region_name='us-east-1'
        )
        self.table_name: str = 'hosts'

    def get_table(self):
        try:
            self.client.describe_table(
                TableName=self.table_name
            )
            return True

        except ClientError as err:
            return None

    def create_table(self):
        try:
            response = self.client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {'AttributeName': 'name', 'KeyType': 'HASH'},
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
            self.client.delete_table(TableName=self.table_name)
        except ClientError as err:
            raise err


class DynamoDBManager:
    def __init__(self):
        self.client = boto3.client(
            'dynamodb',
            region_name='us-east-1'
        )
        self.table_name: str = 'hosts'

    def get_item(self, name: str, ip: str):

        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                'name': {'S': name},
                'ip': {'S': ip}
            }
        )

        return response

    def create_item(self, data_instance: dict[str, str]):

        name = data_instance.get('name')

        response = self.client.put_item(
            TableName=self.table_name,
            Item={
                'name': {'S': name},
                'ip': {'S': data_instance['ip']},
            }
        )
        print(f'Host "{name} criado com sucesso"')
        return response

    def delete_item(self, data_instance: dict[str, str]):

        name = data_instance.get('name')

        response = self.client.delete_item(
            TableName=self.table_name,
            Key={
                'name': {'S': name},
                'ip': {'S': data_instance['ip']},
            }
        )
        print(f'Host "{name} criado com sucesso"')
        return response
