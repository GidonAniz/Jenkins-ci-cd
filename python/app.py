import boto3
import json
from pythonjsonlogger import jsonlogger

# Initialize the JSON logger
logger = jsonlogger.JsonFormatter()
handler = logging.StreamHandler()
handler.setFormatter(logger)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# AWS credentials and region
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
aws_region = 'YOUR_AWS_REGION'

# Initialize the AWS EC2 client
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Check for running K8S clusters
filters = [
    {
        'Name': 'tag:k8s.io/role/master',
        'Values': ['1']
    },
    {
        'Name': 'instance-state-code',
        'Values': ['16']
    }
]

instances = ec2.describe_instances(Filters=filters)
running_clusters = []

for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        running_clusters.append(instance['PublicIpAddress'])

if running_clusters:
    log_data = {
        "threadName": "MainThread",
        "name": "K8S REPORTS",
        "time": "04/08/2020",
        "Running clusters": len(running_clusters),
        "Clusters IPs": running_clusters,
        "Cluster Name": "K8S TESTING",
        "msecs": 506.24799728393555,
        "message": "testing K8S REPORTING",
        "levelname": "INFO"
    }
    logger.info(json.dumps(log_data))
