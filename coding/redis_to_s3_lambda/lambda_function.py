from redis_to_s3 import fetch_redis_data, export_to_s3

def lambda_handler(event, context):
    try:
        redis_data = fetch_redis_data()
        export_format = os.getenv('EXPORT_FORMAT', 'json')
        export_to_s3(redis_data, export_format)
        return {
            'statusCode': 200,
            'body': 'Redis data successfully exported to S3.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error exporting Redis data: {str(e)}'
        }
