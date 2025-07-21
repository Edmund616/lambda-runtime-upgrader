import boto3
import logging

def update_lambda_runtime(function_name, region, new_runtime, dry_run=True):
    client = boto3.client("lambda", region_name=region)
    if dry_run:
        logging.info(f"[DRY RUN] Would update {function_name} to {new_runtime}")
        return True

    try:
        client.update_function_configuration(
            FunctionName=function_name,
            Runtime=new_runtime
        )
        logging.info(f"Updated {function_name} to {new_runtime}")
        return True
    except Exception as e:
        logging.error(f"Failed to update {function_name}: {e}")
        return False
