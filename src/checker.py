import boto3

def list_lambda_functions(region):
    client = boto3.client("lambda", region_name=region)
    paginator = client.get_paginator("list_functions")
    functions = []

    for page in paginator.paginate():
        functions.extend(page["Functions"])

    return functions
