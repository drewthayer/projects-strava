import boto3

if __name__=='__main__':
# connect to s3 bucket with bucket
    bucket = 'strava-project'

    s3 = boto3.client('s3')
    all_objects = s3.list_objects(Bucket = bucket)
