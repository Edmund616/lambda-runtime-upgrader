import boto3
import json
import os

def load_outdated_runtimes():
    with open("data/outdated_runtimes.json", "r") as f:
        return json.load(f)

def list_lambda_functions(region):
    client = boto3.client("lambda", region_name=region)
    functions = []
    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        functions.extend(page["Functions"])
    return functions

def generate_report(functions, outdated_runtimes):
    report = []
    for fn in functions:
        fn_name = fn["FunctionName"]
        fn_runtime = fn["Runtime"]
        if fn_runtime in outdated_runtimes:
            report.append({
                "FunctionName": fn_name,
                "CurrentRuntime": fn_runtime,
                "RecommendedRuntime": outdated_runtimes[fn_runtime],
            })
    return report
