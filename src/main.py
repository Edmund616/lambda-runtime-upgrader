import argparse
import json
import os
from encryptor import list_lambda_functions, generate_report

def main():
    parser = argparse.ArgumentParser(description="Lambda Runtime Upgrader")
    parser.add_argument("--region", required=True, help="AWS region")
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be updated")
    args = parser.parse_args()

    print(f"[INFO] Region set to: {args.region}")
    print(f"[INFO] Dry-run mode: {args.dry_run}")

    # Step 1: List functions
    functions = list_lambda_functions(args.region)
    print(f"[INFO] Retrieved {len(functions)} Lambda functions.")

    # Step 2: Generate report
    report = generate_report(functions, dry_run=args.dry_run)

    # Step 3: Write report
    os.makedirs("data", exist_ok=True)
    with open("data/report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("[INFO] Report written to data/report.json")

if __name__ == "__main__":
    main()
