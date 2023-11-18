import boto3
import schedule
import time
import os

def get_instance_information():
    # Your existing code here...

if __name__ == "__main__":
    # Set up the interval from the environment variable, default to 5 minutes
    interval_minutes = int(os.getenv("INTERVAL_MINUTES", 5))

    # Schedule the function to run every specified interval
    schedule.every(interval_minutes).minutes.do(get_instance_information)

    while True:
        # Run scheduled jobs
        schedule.run_pending()
        time.sleep(1)

        # Check if there is a response with IPs
        if instance_info:
            # Count the number of clusters
            num_clusters = len(instance_info)

            # Log the information in JSON format (modify as needed)
            log_data = {
                "threadName": "MainThread",
                "name": "K8S REPORTS",
                "time": time.strftime("%m/%d/%Y"),
                "Running clusters": num_clusters
            }

            # Log individual cluster information
            for idx, (instance_id, instance_name) in enumerate(instance_info, start=1):
                log_data[f"CLUSTER {idx} IP"] = instance_id
                log_data[f"CLUSTER {idx} NAME"] = instance_name

            log_data["msecs"] = time.time() * 1000
            log_data["message"] = "testing K8S REPORTING"
            log_data["levelname"] = "INFO"

            # Output logs as JSON (modify as needed)
            print(json.dumps(log_data))

        # Reset instance_info after logging
        instance_info = []
