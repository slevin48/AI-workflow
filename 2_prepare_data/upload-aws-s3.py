import os
import boto3

s3_client = boto3.client('s3')
s3_bucket = "aiworkflow"

training_dataset = "2021-03-11-2"

training_files = os.listdir("samples/"+training_dataset)

for file in training_files:
    file_name = "samples/"+training_dataset+"/"+file
    object_name = training_dataset+"_"+file
    print(object_name)
    # s3_client.upload_file(file_name, bucket, object_name)
    s3_client.upload_file(file_name, s3_bucket, object_name)