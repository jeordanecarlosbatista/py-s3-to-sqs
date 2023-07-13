# list
aws s3 ls --endpoint-url http://localhost:4566

# create bucket
aws s3api create-bucket --bucket bucket_name --region us-east-1 --endpoint-url http://localhost:4566

# upload
aws s3 cp 500k.parquet s3://bucket_name --endpoint-url http://localhost:4566

# list files on bucket
aws s3 ls s3://bucket_name --endpoint-url http://localhost:4566