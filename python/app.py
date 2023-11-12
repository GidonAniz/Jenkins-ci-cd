import boto3
import json

def get_instance_information():
    # Set AWS credentials using the environment variables
    session = boto3.Session(
        aws_access_key_id='AKIA5XC7JSBWTTL763BI',
        aws_secret_access_key='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',
        region_name='us-east-1'
    )
    
    ec2 = session.client('ec2')

    # Use the client to get information about instances
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-code',
                'Values': ['16']
            },
            {
                'Name': 'tag:k8s.io/role/master',
                'Values': ['1']
            }
        ]
    )

    # Extract the instance information from the response
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_details = {
                'InstanceId': instance['InstanceId'],
                'InstanceName': next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed')
            }
            instances.append(instance_details)

    # Return the instance details
    return instances

if __name__ == "__main__":
    instance_info = get_instance_information()

    # Convert the instance information to JSON
    json_info = json.dumps(instance_info, indent=2)
    print(json_info)
