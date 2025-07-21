import csv

def generate_report(filepath, report_data):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Function Name", "Region", "Current Runtime", "Target Runtime", "Status"])
        writer.writerows(report_data)
