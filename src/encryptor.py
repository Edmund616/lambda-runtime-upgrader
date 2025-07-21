import boto3
import json
import os
from datetime import datetime

def list_lambda_functions(client):
    functions = []
    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        functions.extend(page["Functions"])
    return functions

def load_outdated_runtimes():
    return {
        "python3.12": "python3.11",
        "nodejs20.x": "nodejs18.x",
        # Add more as needed
    }

def generate_report(functions, outdated_runtimes, dry_run):
    report_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "dry_run": dry_run,
        "updated": [],
    }

    for fn in functions:
        old_runtime = fn["Runtime"]
        new_runtime = outdated_runtimes.get(old_runtime)

        if new_runtime:
            report_data["updated"].append({
                "FunctionName": fn["FunctionName"],
                "OldRuntime": old_runtime,
                "NewRuntime": new_runtime,
            })

    os.makedirs("data", exist_ok=True)
    with open("data/report.json", "w") as f:
        json.dump(report_data, f, indent=2)

    return report_data

