import os
import time
import boto3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Print logs to the console
        logging.FileHandler("output.log")  # Save logs to a file
    ]
)

def get_instance_information():
    # Set AWS credentials with hardcoded values
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
    return [
        (instance['InstanceId'], next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed'))
        for instance in instances
    ]

if __name__ == "__main__":
    interval_minutes = int(os.environ.get('INTERVAL_MINUTES', 5))

    while True:
        instance_info = get_instance_information()

        # Log the instance IDs and instance names
        for instance_id, instance_name in instance_info:
            logging.info(f"Instance ID: {instance_id}, Instance Name: {instance_name}")

        # Sleep for the specified interval in minutes
        time.sleep(interval_minutes * 60)
