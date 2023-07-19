import os
import pandas as pd
import boto3
from io import BytesIO
import json
import uuid

s3_client = boto3.client('s3', endpoint_url='http://localhost:4566')
bucket_name = 'game-results'
file_name = 'game-results.parquet'
sqs_client = boto3.client('sqs', endpoint_url='http://localhost:4566')
queue_name = 'game-results.fifo'
queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
file_content = response['Body'].read()
MAX_BATCH_SIZE_QUEUE = 10
MAX_GROUPS_ID = 5
maxBatchSizeQueue = MAX_BATCH_SIZE_QUEUE
maxGroups = MAX_GROUPS_ID
batch_messages = []
df = pd.read_parquet(BytesIO(file_content))
count = 1

for i, row in enumerate(df.itertuples(index=False), 1):
    message = {
        'year': row.ano,
        'champion': row.campeao,
        'runnerUp': row.vice_campeao,
        'result': row.resultado
    }
    batch_messages.append({
        'Id': str(uuid.uuid4()),
        'MessageBody': json.dumps(message),
        'MessageDeduplicationId': f"{message['year']}-{message['champion']}",
        'MessageGroupId': f'GROUP#{(count % maxGroups) + 1}',
    })
    if i % maxBatchSizeQueue == 0 or i == len(df):
        response = sqs_client.send_message_batch(
            QueueUrl=queue_url, Entries=batch_messages)
        batch_messages = []
    count += 1
