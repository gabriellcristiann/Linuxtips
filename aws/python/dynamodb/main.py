from fastapi import FastAPI

from dynamodb.controllers import DynamoDBCore, DynamoDBManager

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/dynamo")
async def get_item(hostname: str, ip: str):

    item = DynamoDBManager().get_item(name=hostname, ip=ip)

    return {"item": item}

@app.post("/dynamo")
async def create_host(hostname: str, ip: str):

    verify_table_exists = DynamoDBCore().get_table()

    if verify_table_exists is None:
        breakpoint()
        DynamoDBCore().create_table()

    data_instance = {
        'name': hostname,
        'ip': ip
    }

    DynamoDBManager().create_item(data_instance=data_instance)

    return {"message": "Host created successfully!"}


@app.delete("/dynamo")
async def delete_host(hostname: str, ip: str):

    verify_table_exists = DynamoDBCore().get_table()

    if verify_table_exists is None:
        return {"message": "Table does not exist!"}

    data_instance = {
        'name': hostname,
        'ip': ip
    }

    DynamoDBManager().delete_item(data_instance=data_instance)
    DynamoDBCore().delete_table()

    return {"message": "Host deleted successfully!"}
