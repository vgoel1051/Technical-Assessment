import os
import csv
import json
import redis
import boto3
from datetime import datetime

# Redis connection setup (adjust with task ElastiCache endpoint)
redis_host = os.getenv('REDIS_HOST', 'task-elasticache-endpoint')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)

# S3 connection setup
s3_bucket = os.getenv('S3_BUCKET', 'task-s3-bucket-name')
s3_key_prefix = os.getenv('S3_KEY_PREFIX', 'redis-dumps')

s3_client = boto3.client('s3')

def fetch_redis_data():
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    keys = r.keys('*')
    data = []
    for key in keys:
        value = r.get(key)
        data.append({'key': key, 'value': value})
    return data

def export_to_s3(data, format='json'):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')
    filename = f"{s3_key_prefix}/redis_export_{timestamp}.{format}"

    if format == 'json':
        file_content = json.dumps(data, indent=2)
    elif format == 'csv':
        file_content = convert_to_csv(data)
    else:
        raise ValueError("Unsupported format. Use 'json' or 'csv'.")

    s3_client.put_object(Bucket=s3_bucket, Key=filename, Body=file_content)
    print(f"Data successfully uploaded to s3://{s3_bucket}/{filename}")

def convert_to_csv(data):
    from io import StringIO
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=['key', 'value'])
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

if __name__ == '__main__':
    redis_data = fetch_redis_data()
    export_format = os.getenv('EXPORT_FORMAT', 'json')
    export_to_s3(redis_data, export_format)
