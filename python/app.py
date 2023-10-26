import boto3


ec2 = boto3.client('ec2')

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

# Print the instance IDs and instance names
for instance in instances:
    instance_id = instance['InstanceId']
    instance_name = next((tag['Value']
                          for tag in instance['Tags'] if tag['Key'] == 'Name'), 'Unnamed')
    print("Instance ID: {}, Instance Name: {}".format(instance_id, instance_name))