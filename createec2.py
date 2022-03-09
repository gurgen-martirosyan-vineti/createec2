import os
import boto3

AWS_REGION = "us-west-2"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
AMI_ID = 'ami-06cffe063efe892ad'

instances = EC2_RESOURCE.create_instances(
    MinCount = 1,
    MaxCount = 1,
    ImageId=AMI_ID,
    InstanceType='t2.micro',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': os.environ["EC2_NAME_TAG"]
                },
            ]
        },
    ]
)

for instance in instances:
    print(f'EC2 instance "{instance.id}" has been launched')

    instance.wait_until_running()
    print(f'EC2 instance "{instance.id}" has been started')