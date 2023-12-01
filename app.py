import os
import time
import json
import boto3
import schedule


def get_instance_information():
    # Set AWS credentials using the hardcoded values
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

    # Return the instance information as a list of dictionaries
    return [
        {'InstanceId': instance['InstanceId'],
         'InstanceName': next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed')}
        for instance in instances]


def print_instance_info():
    instance_info = get_instance_information()

    # Print the instance information as JSON
    print(json.dumps(instance_info, indent=2))


if __name__ == "__main__":
    # Get the interval from the environment variable, defaulting to 5 minutes
    interval_minutes = int(os.environ.get('INTERVAL_MINUTES', 0.1))

    # Schedule the job to run every specified interval
    schedule.every(interval_minutes).minutes.do(print_instance_info)

    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
