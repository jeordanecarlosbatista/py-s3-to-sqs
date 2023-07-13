#!/bin/bash

REGION=us-east-1
LOCALSTACK_ENDPOINT_URL=http://localhost:4566
BUCKET=game-results
QUEUE_NAME=game-results.fifo
QUEUE_URL=$LOCALSTACK_ENDPOINT_URL/000000000000/$QUEUE_NAME
PARQUET_BASE_URL=$(pwd)/scripts/parquets

# remove bucket
aws s3 rb s3://$BUCKET --force --endpoint-url $LOCALSTACK_ENDPOINT_URL

# create bucket
aws s3api create-bucket --bucket $BUCKET --region $REGION --endpoint-url $LOCALSTACK_ENDPOINT_URL

# upload parquets
aws s3 cp $PARQUET_BASE_URL/game-results.parquet s3://$BUCKET --endpoint-url $LOCALSTACK_ENDPOINT_URL

# remove queue
aws sqs delete-queue --queue-url $QUEUE_URL --endpoint-url $LOCALSTACK_ENDPOINT_URL

# create queue fifo
aws sqs create-queue \
    --queue-name $QUEUE_NAME \
    --attributes FifoQueue=true \
    --endpoint-url $LOCALSTACK_ENDPOINT_URL