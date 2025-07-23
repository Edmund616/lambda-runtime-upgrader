# Lambda Runtime Upgrader

 Automatically detect and upgrade AWS Lambda functions with outdated runtimes (e.g., Python 3.6 → Python 3.11).

##  Features

- Lists all Lambda functions in a region
- Detects outdated runtimes based on policy file
- Updates to latest supported runtimes
- Dry-run mode (safe simulation)
- Generates CSV report

##  Example Usage

```bash
python src/main.py --region us-east-1 --dry-run
python src/main.py --region us-east-1

An indepth explanation for this project has been given on my mediums post down below
https://medium.com/@divyln20/keeping-your-aws-lambda-runtimes-updated-automatically-0d8a2bf26f59
