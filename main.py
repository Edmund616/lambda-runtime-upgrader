import argparse
import json
from src.encryptor import list_lambda_functions, generate_report, load_outdated_runtimes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True, help="AWS region to scan")
    parser.add_argument("--dry-run", action="store_true", help="Don't update, just report")
    args = parser.parse_args()

    print(f"\n🔍 Scanning Lambda functions in region: {args.region}")
    functions = list_lambda_functions(args.region)
    print(f"✅ Found {len(functions)} functions")

    outdated_runtimes = load_outdated_runtimes()
    report = generate_report(functions, outdated_runtimes)

    if args.dry_run:
        print(f"📝 Outdated functions found: {len(report)}")
        for item in report:
            print(f" - {item['FunctionName']}: {item['CurrentRuntime']} ➜ {item['RecommendedRuntime']}")
    else:
        print("⚠️ This would perform updates (not implemented yet)")

    # Save the report to file
    with open("data/report.json", "w") as f:
        json.dump(report, f, indent=2)
        print("\n📁 Report written to data/report.json")

if __name__ == "__main__":
    main()

