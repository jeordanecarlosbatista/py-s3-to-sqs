# create queue fifo
aws sqs create-queue \
    --queue-name game-results.fifo \
    --attributes FifoQueue=true \
    --endpoint-url http://localhost:4566

# list queues
aws sqs list-queues --endpoint-url http://localhost:4566

# list messages
aws sqs receive-message \
    --queue-url http://localhost:4566/000000000000/game-results.fifo \
    --max-number-of-messages 10\
    --endpoint-url http://localhost:4566

aws sqs list-queues \
    --queue-url http://localhost:4566/000000000000/game-results.fifo \
    --output json | jq '.Tags."aws:group-id"' \
    --endpoint-url http://localhost:4566

aws sqs get-queue-attributes \
    --queue-url http://localhost:4566/000000000000/game-results.fifo \
    --attribute-names ApproximateNumberOfMessages \
    --endpoint-url http://localhost:4566

# delete messages
aws sqs purge-queue \
    --queue-url http://localhost:4566/000000000000/game-results.fifo\
    --endpoint-url http://localhost:4566