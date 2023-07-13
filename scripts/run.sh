#!/bin/bash
APP=$(pwd)

source $APP/scripts/setup.sh

python3 $APP/app.py

aws sqs receive-message \
    --queue-url http://localhost:4566/000000000000/game-results.fifo \
    --max-number-of-messages 1\
    --endpoint-url http://localhost:4566

echo finished!!!

exit 0
