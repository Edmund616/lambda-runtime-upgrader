import argparse
import boto3
import json
import os
from datetime import datetime

from src.encryptor import (
    list_lambda_functions,
    load_outdated_runtimes,
)

def upgrade_runtime(client, function, new_runtime, dry_run):
    log = {
        "FunctionName": function["FunctionName"],
        "OldRuntime": function["Runtime"],
        "NewRuntime": new_runtime,
        "Region": client.meta.region_name,
        "Timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if dry_run:
        log["Status"] = "Dry run - not updated"
    else:
        try:
            client.update_function_configuration(
                FunctionName=function["FunctionName"],
                Runtime=new_runtime,
            )
            log["Status"] = "Updated Successfully"
        except Exception as e:
            log["Status"] = f"Failed to update: {str(e)}"

    # Write to logs
    os.makedirs("runtime_upgraded_logs", exist_ok=True)
    with open(f"runtime_upgraded_logs/{function['FunctionName']}.json", "w") as f:
        json.dump(log, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True, help="AWS region")
    parser.add_argument("--dry-run", action="store_true", help="Simulate upgrade")
    args = parser.parse_args()

    region = args.region
    dry_run = args.dry_run

    print(f"\n🔍 Scanning Lambda functions in region: {region}")

    client = boto3.client("lambda", region_name=region)
    outdated_map = load_outdated_runtimes()

    functions = list_lambda_functions(client)
    print(f"✅ Found {len(functions)} functions")

    outdated = []
    for fn in functions:
        current_runtime = fn["Runtime"]
        if current_runtime in outdated_map:
            new_runtime = outdated_map[current_runtime]
            outdated.append({
                "FunctionName": fn["FunctionName"],
                "CurrentRuntime": current_runtime,
                "SuggestedRuntime": new_runtime,
            })
            upgrade_runtime(client, fn, new_runtime, dry_run)

    print(f"📝 Outdated functions found: {len(outdated)}")
    for fn in outdated:
        print(f" - {fn['FunctionName']}: {fn['CurrentRuntime']} ➜ {fn['SuggestedRuntime']}")

    os.makedirs("data", exist_ok=True)
    with open("data/report.json", "w") as f:
        json.dump(outdated, f, indent=2)

    print("\n📁 Report written to data/report.json")
    if not dry_run:
        print("�� Individual logs saved in runtime_upgraded_logs/")

if __name__ == "__main__":
    main()

