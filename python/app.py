
import boto3

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
            instances.append(instance)

    # Return the instance IDs and instance names
    return [(instance['InstanceId'], next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed')) for instance in instances]

if __name__ == "__main__":
    instance_info = get_instance_information()

    # Print the instance IDs and instance names
    for instance_id, instance_name in instance_info:
        print(f"Instance ID: {instance_id}, Instance Name: {instance_name}")
import boto3

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
            instances.append(instance)

    # Return the instance IDs and instance names
    return [(instance['InstanceId'], next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed')) for instance in instances]

if __name__ == "__main__":
    instance_info = get_instance_information()

    # Print the instance IDs and instance names
    for instance_id, instance_name in instance_info:
        print(f"Instance ID: {instance_id}, Instance Name: {instance_name}")
