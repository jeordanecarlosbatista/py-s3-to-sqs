import pyarrow.parquet as pq
import boto3
import psutil
import json
import uuid
import time

def create_message(i, row):
    message_body = {
        'year': row.ano,
        'champion': row.campeao,
        'runnerUp': row.vice_campeao,
        'result': row.resultado
    }
    message = {
       'Id': str(uuid.uuid4()),
        'MessageBody': json.dumps(message_body),
        'MessageDeduplicationId': f"{message_body['year']}-{message_body['champion']}",
        'MessageGroupId': f'GROUP#{(i % maxGroups) + 1}',
    }
    return message

def obter_consumo_memoria():
    print(
        f"Consumo de memória atual: {process.memory_info().rss / (1024 * 1024):.2f} MB")

start = time.time()

process = psutil.Process()
memory_info = process.memory_info()
memory_before = psutil.Process().memory_info().rss

s3_client = boto3.client('s3', endpoint_url='http://localhost:4566')
bucket_name = 'game-results'
file_name = 'game-results.parquet'

sqs_client = boto3.client('sqs', endpoint_url='http://localhost:4566')
queue_name = 'game-results.fifo'
queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']

MAX_BATCH_SIZE_QUEUE = 10
MAX_GROUPS_ID = 5

maxBatchSizeQueue = MAX_BATCH_SIZE_QUEUE
maxGroups = MAX_GROUPS_ID

local_file_path = '/tmp/file.parquet'
s3_client.download_file(bucket_name, file_name, local_file_path)
parquet = pq.ParquetFile(local_file_path)


for batch in parquet.iter_batches(batch_size=maxBatchSizeQueue):
    df = batch.to_pandas()
    batch_messages = [create_message(i, row) for i, row in enumerate(
    df.itertuples(index=False), 1)]
    sqs_client.send_message_batch(QueueUrl=queue_url, Entries=batch_messages)

sqs_client.send_message_batch(
        QueueUrl=queue_url, Entries=batch_messages)

end = time.time()
duration_in_seconds = end - start
duration_in_minutes = round(duration_in_seconds / 60, 2)

memory_after = psutil.Process().memory_info().rss
memory_usage = (memory_after - memory_before) / (1024 * 1024)

obter_consumo_memoria()
print("Duração do processo:", duration_in_minutes, "minutos")
