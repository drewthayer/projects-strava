import boto3

if __name__=='__main__':
# connect to s3 bucket with bucket
    bucket = 'strava-project'

    # write to s3
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('scripts/StravaActivity.py', bucket, 'hello.txt')

    # read from s3
    #s3 = boto3.client('s3')
    #all_objects = s3.list_objects(Bucket = bucket)
